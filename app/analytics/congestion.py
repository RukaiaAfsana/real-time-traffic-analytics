class TrafficCongestion:
    def __init__(self, low_threshold=10, medium_threshold=20):
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold

    def get_level(self, vehicle_count):
        if vehicle_count <= self.low_threshold:
            return "Low"
        elif vehicle_count <= self.medium_threshold:
            return "Medium"
        