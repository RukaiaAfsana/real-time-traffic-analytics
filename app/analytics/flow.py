class TrafficFlow:
    def __init__(self):
        self.previous_total = 0
        self.crossing_times = []

    def update(self, total_crossings, video_time_seconds):
        if total_crossings > self.previous_total:
            new_crossings = total_crossings - self.previous_total

            for _ in range(new_crossings):
                self.crossing_times.append(video_time_seconds)

        self.previous_total = total_crossings

    def vehicles_per_minute(self, current_time):
        if current_time <= 0:
            return 0

        recent_crossings = [
            t for t in self.crossing_times
            if current_time - t <= 60
        ]

        # First 60 seconds:
        # normalize using the actual elapsed time
        if current_time < 60:
            return round(
                len(recent_crossings) * 60 / current_time
            )

        # After 60 seconds:
        # count crossings in the most recent 60-second window
        return len(recent_crossings)

    def vehicles_per_hour(self, current_time):
        return self.vehicles_per_minute(current_time) * 60