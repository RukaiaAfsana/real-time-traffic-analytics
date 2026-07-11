import cv2
import numpy as np


class TrafficHeatmap:
    def __init__(self, width, height):
        self.heatmap = np.zeros(
            (height, width),
            dtype=np.float32
        )

    def update(self, detections):
        if detections.xyxy is None:
            return

        for x1, y1, x2, y2 in detections.xyxy:
            center_x = int((x1 + x2) / 2)
            bottom_y = int(y2)

            if (
                0 <= center_x < self.heatmap.shape[1]
                and 0 <= bottom_y < self.heatmap.shape[0]
            ):
                cv2.circle(
                    self.heatmap,
                    (center_x, bottom_y),
                    25,
                    1,
                    -1
                )

    def create_overlay(self, frame):
        blurred = cv2.GaussianBlur(
            self.heatmap,
            (0, 0),
            sigmaX=35,
            sigmaY=35
        )

        normalized = cv2.normalize(
            blurred,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        normalized = normalized.astype(np.uint8)

        colored = cv2.applyColorMap(
            normalized,
            cv2.COLORMAP_JET
        )

        return cv2.addWeighted(
            frame,
            0.7,
            colored,
            0.3,
            0
        )