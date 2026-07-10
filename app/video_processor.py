import cv2
import supervision as sv

from app.analytics.line_counter import VehicleLineCounter


class VideoProcessor:
    def __init__(self, input_path, output_path, counting_line=None):
        self.input_path = input_path
        self.output_path = output_path
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

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

            labels = [
                f"ID {tracker_id} Class {class_id}"
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

            writer.write(annotated_frame)
            cv2.imshow("Traffic Analytics", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()