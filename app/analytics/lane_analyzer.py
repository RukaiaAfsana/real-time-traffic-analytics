import cv2
import numpy as np


class LaneAnalyzer:
    def __init__(self, lanes):
        """
        lanes example:

        {
            "Lane 1": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
            "Lane 2": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
        """

        self.lanes = {
            lane_name: np.array(points, dtype=np.int32)
            for lane_name, points in lanes.items()
        }

        self.lane_counts = {
            lane_name: 0
            for lane_name in self.lanes
        }

    def update(self, detections):
        # Reset live counts every frame
        self.lane_counts = {
            lane_name: 0
            for lane_name in self.lanes
        }

        if detections.xyxy is None:
            return

        for xyxy in detections.xyxy:
            x1, y1, x2, y2 = xyxy

            # Bottom-center point of the vehicle box
            point = (
                int((x1 + x2) / 2),
                int(y2)
            )

            for lane_name, polygon in self.lanes.items():
                result = cv2.pointPolygonTest(
                    polygon,
                    point,
                    False
                )

                if result >= 0:
                    self.lane_counts[lane_name] += 1
                    break

    # def annotate(self, frame):
    #     for lane_name, polygon in self.lanes.items():
    #         cv2.polylines(
    #             frame,
    #             [polygon],
    #             isClosed=True,
    #             color=(255, 255, 255),
    #             thickness=2
    #         )

    #         x, y = polygon[0]

    #         cv2.putText(
    #             frame,
    #             f"{lane_name}: {self.lane_counts[lane_name]}",
    #             (int(x), int(y) - 15),
    #             cv2.FONT_HERSHEY_SIMPLEX,
    #             0.8,
    #             (255, 255, 255),
    #             2,
    #             cv2.LINE_AA
    #         )

    #     return frame
    def annotate(self, frame):
        for polygon in self.lanes.values():
            cv2.polylines(
                frame,
                [polygon],
                isClosed=True,
                color=(255, 255, 255),
                thickness=2
            )

        return frame