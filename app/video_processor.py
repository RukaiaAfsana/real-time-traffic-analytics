import cv2
import supervision as sv


class VideoProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def process(self, detector, tracker):
        cap = cv2.VideoCapture(self.input_path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {self.input_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

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

            labels = [
                f"ID {tracker_id}"
                for tracker_id in detections.tracker_id
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

            writer.write(annotated_frame)
            cv2.imshow("Traffic Analytics", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        writer.release()
        cv2.destroyAllWindows()