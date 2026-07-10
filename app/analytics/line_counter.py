import cv2
import supervision as sv


class VehicleLineCounter:
    def __init__(self, start, end):
        self.line_zone = sv.LineZone(
            start=sv.Point(start[0], start[1]),
            end=sv.Point(end[0], end[1])
        )
        self.line_annotator = sv.LineZoneAnnotator(
            thickness=2,
            text_thickness=2,
            text_scale=1
        )
    
    def update(self, detections):
        self.line_zone.trigger(detections=detections)

    def annotate(self, frame):
        return self.line_annotator.annotate(
            frame=frame,
            line_counter=self.line_zone
        )
