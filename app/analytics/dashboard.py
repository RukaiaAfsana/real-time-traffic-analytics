import cv2
import numpy as np
from collections import Counter

from app.analytics.congestion import TrafficCongestion


class TrafficDashboard:
    def __init__(self, class_names, width=600, height=700):
        self.class_names = class_names
        self.congestion = TrafficCongestion()

        self.width = width
        self.height = height

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text_color = (255, 255, 255)
        self.background_color = (25, 25, 25)

    def create(self, detections, line_counter=None,flow_per_minute=0,flow_per_hour=0):
        dashboard = np.full(
            (self.height, self.width, 3),
            self.background_color,
            dtype=np.uint8
        )

        class_counter = Counter()

        if detections.class_id is not None:
            for class_id in detections.class_id:
                class_name = self.class_names[int(class_id)]
                class_counter[class_name] += 1

        total = len(detections)
        traffic_level = self.congestion.get_level(total)

        y = 60

        cv2.putText(
            dashboard,
            "TRAFFIC ANALYTICS",
            (35, y),
            self.font,
            1.2,
            self.text_color,
            3,
            cv2.LINE_AA
        )

        y += 70

        cv2.putText(
            dashboard,
            f"Vehicles in scene: {total}",
            (35, y),
            self.font,
            0.9,
            self.text_color,
            2,
            cv2.LINE_AA
        )

        y += 55

        cv2.putText(
            dashboard,
            "Vehicle classes",
            (35, y),
            self.font,
            0.9,
            self.text_color,
            2,
            cv2.LINE_AA
        )

        y += 45

        for class_name, count in sorted(class_counter.items()):
            cv2.putText(
                dashboard,
                f"{class_name.title():<15} {count}",
                (55, y),
                self.font,
                0.8,
                self.text_color,
                2,
                cv2.LINE_AA
            )
            y += 42

        y += 30

        cv2.putText(
            dashboard,
            f"Traffic level: {traffic_level}",
            (35, y),
            self.font,
            0.9,
            self.text_color,
            2,
            cv2.LINE_AA
        )

        if line_counter is not None:
            y += 65

            cv2.putText(
                dashboard,
                f"IN: {line_counter.in_count}",
                (35, y),
                self.font,
                0.9,
                self.text_color,
                2,
                cv2.LINE_AA
            )

            y += 50

            cv2.putText(
                dashboard,
                f"OUT: {line_counter.out_count}",
                (35, y),
                self.font,
                0.9,
                self.text_color,
                2,
                cv2.LINE_AA
            )
            y += 60

            cv2.putText(
                dashboard,
                f"Flow: {flow_per_minute} veh/min",
                (35, y),
                self.font,
                0.8,
                self.text_color,
                2,
                cv2.LINE_AA
            )

            y += 50

            cv2.putText(
                dashboard,
                f"Hourly rate: {flow_per_hour} veh/hr",
                (35, y),
                self.font,
                0.8,
                self.text_color,
                2,
                cv2.LINE_AA
            )   

        return dashboard