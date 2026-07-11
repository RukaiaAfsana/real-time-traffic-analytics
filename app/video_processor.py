import cv2
import supervision as sv

from app.analytics.line_counter import VehicleLineCounter
from app.analytics.dashboard import TrafficDashboard
from app.analytics.flow import TrafficFlow
from app.analytics.speed_estimator import RelativeSpeedEstimator
from app.analytics.lane_analyzer import LaneAnalyzer
from app.analytics.heatmap import TrafficHeatmap

class VideoProcessor:
    def __init__(self, input_path, output_path, detector_class_names,counting_line=None,lanes=None):
        self.input_path = input_path
        self.output_path = output_path
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.dashboard = TrafficDashboard(detector_class_names)
        self.traffic_flow = TrafficFlow()
        self.speed_estimator = RelativeSpeedEstimator()



        self.line_counter = None
        if counting_line is not None:
            self.line_counter = VehicleLineCounter(
                start=counting_line["start"],
                end=counting_line["end"]
            )
        
        self.lane_analyzer = None

        if lanes is not None:
            self.lane_analyzer = LaneAnalyzer(lanes)
        
        # Create and resize display windows
        cv2.namedWindow("Traffic Analytics", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Traffic Analytics", 405, 720)

        cv2.namedWindow("Dashboard", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Dashboard", 500, 750)

        cv2.namedWindow("Traffic Heatmap", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Traffic Heatmap", 405, 720)

    def process(self, detector, tracker):
        cap = cv2.VideoCapture(self.input_path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {self.input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video resolution: {width} x {height}")
        self.heatmap = TrafficHeatmap(width=width, height=height)

        writer = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )
        flow_per_minute = 0
        flow_per_hour = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.detect(frame)
            detections = tracker.update(result)
            video_time_seconds = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)

            #heat-map
            self.heatmap.update(detections)
            

            

            #speed estimator
            self.speed_estimator.update(
                    detections,
                    video_time_seconds
                )
            
            # Lane occupancy
            if self.lane_analyzer is not None:
             self.lane_analyzer.update(detections)
            
            #Lane counting and flow
            if self.line_counter is not None:
                self.line_counter.update(detections)

                total_crossings = (
                    self.line_counter.in_count
                    + self.line_counter.out_count
                )

                self.traffic_flow.update(
                    total_crossings,
                    video_time_seconds
                )

                flow_per_minute = self.traffic_flow.vehicles_per_minute(
                    video_time_seconds
                )

                flow_per_hour = self.traffic_flow.vehicles_per_hour(
                    video_time_seconds
                )

                labels = [
                    (
                        f"ID {tracker_id} | "
                        f"{detector.class_names[int(class_id)]} | "
                        f"{self.speed_estimator.get_speed(tracker_id):.1f} px/s"
                    )
                    for tracker_id, class_id in zip(
                        detections.tracker_id,
                        detections.class_id
                    )
                ]


            annotated_frame = self.box_annotator.annotate(
                scene=frame.copy(),
                detections=detections
            )

            annotated_frame = self.label_annotator.annotate(
                scene=annotated_frame,
                detections=detections,
                labels=labels
            )
            
            #if self.line_counter is not None:
                #annotated_frame = self.line_counter.annotate(annotated_frame)

            if self.lane_analyzer is not None:
                annotated_frame = self.lane_analyzer.annotate(annotated_frame)  
            lane_counts = None

            if self.lane_analyzer is not None:
                lane_counts = self.lane_analyzer.lane_counts    
            
            heatmap_frame = self.heatmap.create_overlay(annotated_frame.copy() )

            dashboard_frame = self.dashboard.create(
                detections=detections,
                line_counter=self.line_counter,
                flow_per_minute=flow_per_minute,
                flow_per_hour=flow_per_hour,
                lane_counts=lane_counts
            )


            writer.write(annotated_frame)
            cv2.imshow("Traffic Analytics", annotated_frame)
            cv2.imshow("Dashboard", dashboard_frame)
            cv2.imshow("Traffic Heatmap", heatmap_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


        cap.release()
        writer.release()
        cv2.destroyAllWindows()