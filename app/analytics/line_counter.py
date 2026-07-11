import supervision as sv


class VehicleLineCounter:
    def __init__(self, start, end):
        self.line_zone = sv.LineZone(
            start=sv.Point(start[0], start[1]),
            end=sv.Point(end[0], end[1])
        )

        self.line_annotator = sv.LineZoneAnnotator(
            thickness=1,
            text_thickness=1,
            text_scale=.5
        )

    def update(self, detections):
        self.line_zone.trigger(detections=detections)

    def annotate(self, frame):
        return self.line_annotator.annotate(
            frame=frame,
            line_counter=self.line_zone
        )

    @property
    def in_count(self):
        return self.line_zone.in_count

    @property
    def out_count(self):
        return self.line_zone.out_count