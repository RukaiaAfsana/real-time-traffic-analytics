from app.utils.config_loader import load_config
from app.detection.yolo_detector import YOLOVehicleDetector
from app.tracking.byte_tracker import ByteTrackVehicleTracker
from app.video_processor import VideoProcessor
import app.video_processor
print(app.video_processor.__file__)

config = load_config()

detector = YOLOVehicleDetector(
    model_path=config["model"]["yolo_model"],
    confidence=config["model"]["confidence"],
    vehicle_classes=config["model"]["vehicle_classes"]
)

tracker = ByteTrackVehicleTracker()


processor = VideoProcessor(
    input_path=config["video"]["input_path"],
    output_path=config["video"]["output_path"]
)
import inspect

print(inspect.signature(processor.process))
processor.process(detector, tracker)

print("Vehicle tracking completed.")