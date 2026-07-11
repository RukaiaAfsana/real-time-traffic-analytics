import cv2
import supervision as sv

from app.analytics.line_counter import VehicleLineCounter
from app.analytics.dashboard import TrafficDashboard
from app.analytics.flow import TrafficFlow
from app.analytics.speed_estimator import RelativeSpeedEstimator

class VideoProcessor:
    def __init__(self, input_path, output_path, detector_class_names,counting_line=None):
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

    def process(self, detector, tracker):
        cap = cv2.VideoCapture(self.input_path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {self.input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Video resolution: {width} x {height}")

        writer = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.detect(frame)
            detections = tracker.update(result)

            
            if self.line_counter is not None:
                self.line_counter.update(detections)

                video_time_seconds = (
                    cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                )
                self.speed_estimator.update(
                    detections,
                    video_time_seconds
                )

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
                f"ID {tracker_id} | {detector.class_names[int(class_id)]}"
                f"{self.speed_estimator.get_speed(tracker_id):.1f} px/s"
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
            if self.line_counter is not None:
                annotated_frame = self.line_counter.annotate(annotated_frame)
            
            dashboard_frame = self.dashboard.create(
                detections,
                self.line_counter,
                flow_per_minute,
                flow_per_hour
            )


            writer.write(annotated_frame)
            cv2.imshow("Traffic Analytics", annotated_frame)
            cv2.imshow("Dashboard", dashboard_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()