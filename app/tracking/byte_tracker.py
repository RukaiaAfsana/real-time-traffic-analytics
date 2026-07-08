import supervision as sv


class ByteTrackVehicleTracker:
    def __init__(self):
        self.tracker = sv.ByteTrack()

    def update(self, result):
        detections = sv.Detections.from_ultralytics(result)
        tracked_detections = self.tracker.update_with_detections(detections)
        return tracked_detections