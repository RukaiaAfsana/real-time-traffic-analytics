import math


class RelativeSpeedEstimator:
    def __init__(self):
        self.previous_positions = {}
        self.previous_times = {}
        self.speeds = {}

    def update(self, detections, video_time_seconds):
        if detections.tracker_id is None:
            return

        for xyxy, tracker_id in zip(
            detections.xyxy,
            detections.tracker_id
        ):
            tracker_id = int(tracker_id)

            x1, y1, x2, y2 = xyxy

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            current_position = (center_x, center_y)

            if (
                tracker_id in self.previous_positions
                and tracker_id in self.previous_times
            ):
                previous_position = self.previous_positions[tracker_id]
                previous_time = self.previous_times[tracker_id]

                distance_pixels = math.dist(
                    previous_position,
                    current_position
                )

                time_difference = (
                    video_time_seconds - previous_time
                )

                if time_difference > 0:
                    speed = distance_pixels / time_difference
                    self.speeds[tracker_id] = speed

            self.previous_positions[tracker_id] = current_position
            self.previous_times[tracker_id] = video_time_seconds

    def get_speed(self, tracker_id):
        return self.speeds.get(int(tracker_id), 0.0)