from ultralytics import YOLO


class YOLOVehicleDetector:
    def __init__(self, model_path: str, confidence: float, vehicle_classes: list[int]):
        self.model = YOLO(model_path)
        self.confidence = confidence
        self.vehicle_classes = vehicle_classes
    @property
    def class_names(self):
        return self.model.names

    def detect(self, frame):
        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            classes=self.vehicle_classes,
            verbose=False
        )
        return results[0]