import cv2
import numpy as np
from collections import Counter

from app.analytics.congestion import TrafficCongestion


class TrafficDashboard:
    def __init__(self, class_names, width=640, height=900):
        self.class_names = class_names
        self.congestion = TrafficCongestion()

        self.width = width
        self.height = height

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.background_color = (18, 18, 18)
        self.card_color = (30, 30, 30)
        self.border_color = (65, 65, 65)

        self.primary_text = (240, 240, 240)
        self.secondary_text = (170, 170, 170)

    def draw_card(self, dashboard, top, height):
        cv2.rectangle(
            dashboard,
            (25, top),
            (self.width - 25, top + height),
            self.card_color,
            -1
        )

        cv2.rectangle(
            dashboard,
            (25, top),
            (self.width - 25, top + height),
            self.border_color,
            1
        )

    def draw_label_value(
        self,
        dashboard,
        label,
        value,
        y,
        label_x=50,
        value_x=430
    ):
        cv2.putText(
            dashboard,
            label,
            (label_x, y),
            self.font,
            0.62,
            self.secondary_text,
            1,
            cv2.LINE_AA
        )

        cv2.putText(
            dashboard,
            str(value),
            (value_x, y),
            self.font,
            0.68,
            self.primary_text,
            2,
            cv2.LINE_AA
        )

    def create(
        self,
        detections,
        line_counter=None,
        flow_per_minute=0,
        flow_per_hour=0,
        lane_counts=None
    ):
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

        # Header
        cv2.putText(
            dashboard,
            "TRAFFIC ANALYTICS",
            (30, 55),
            self.font,
            0.95,
            self.primary_text,
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            dashboard,
            "REAL-TIME MONITORING",
            (32, 82),
            self.font,
            0.45,
            self.secondary_text,
            1,
            cv2.LINE_AA
        )

        # Summary card
        self.draw_card(dashboard, 110, 135)

        self.draw_label_value(
            dashboard,
            "Vehicles in scene",
            total,
            150
        )

        self.draw_label_value(
            dashboard,
            "Traffic level",
            traffic_level,
            195
        )

        # Vehicle classes card
        class_card_height = max(
            120,
            60 + len(class_counter) * 38
        )

        class_top = 265

        self.draw_card(
            dashboard,
            class_top,
            class_card_height
        )

        cv2.putText(
            dashboard,
            "VEHICLE CLASSES",
            (45, class_top + 35),
            self.font,
            0.52,
            self.secondary_text,
            1,
            cv2.LINE_AA
        )

        y = class_top + 75

        for class_name, count in sorted(class_counter.items()):
            self.draw_label_value(
                dashboard,
                class_name.title(),
                count,
                y
            )
            y += 38

        # Flow card
        flow_top = class_top + class_card_height + 20

        self.draw_card(
            dashboard,
            flow_top,
            190
        )

        cv2.putText(
            dashboard,
            "TRAFFIC FLOW",
            (45, flow_top + 35),
            self.font,
            0.52,
            self.secondary_text,
            1,
            cv2.LINE_AA
        )

        if line_counter is not None:
            self.draw_label_value(
                dashboard,
                "IN",
                line_counter.in_count,
                flow_top + 75
            )

            self.draw_label_value(
                dashboard,
                "OUT",
                line_counter.out_count,
                flow_top + 110
            )

        self.draw_label_value(
            dashboard,
            "Flow",
            f"{flow_per_minute} veh/min",
            flow_top + 145
        )

        self.draw_label_value(
            dashboard,
            "Hourly rate",
            f"{flow_per_hour} veh/hr",
            flow_top + 180
        )

        # Lane card
        if lane_counts is not None:
            lane_top = flow_top + 210

            lane_card_height = 65 + len(lane_counts) * 36

            self.draw_card(
                dashboard,
                lane_top,
                lane_card_height
            )

            cv2.putText(
                dashboard,
                "LANE OCCUPANCY",
                (45, lane_top + 35),
                self.font,
                0.52,
                self.secondary_text,
                1,
                cv2.LINE_AA
            )

            y = lane_top + 75

            for lane_name, count in lane_counts.items():
                self.draw_label_value(
                    dashboard,
                    lane_name,
                    count,
                    y
                )
                y += 36

        return dashboard