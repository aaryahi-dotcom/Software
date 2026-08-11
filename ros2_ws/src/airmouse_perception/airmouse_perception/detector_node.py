"""
Role 3 — Perception & Detection
Webcam (stand-in for Orbbec Gemini 335) → YOLOv8n → temporal confirmation →
publishes vision_msgs/Detection2DArray on /detections.

Prototype phase: uses laptop webcam via cv2.VideoCapture.
Hardware phase: subscribes to camera image topic instead.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy

from sensor_msgs.msg import Image
from vision_msgs.msg import (
    Detection2D,
    Detection2DArray,
    ObjectHypothesisWithPose,
)
from cv_bridge import CvBridge

import cv2
import numpy as np
from collections import defaultdict

# Ultralytics is imported lazily in on_configure so the node can still
# be instantiated in environments where the weight file isn't present.
YOLO = None


class DetectorNode(Node):
    """YOLOv8n person detector with temporal confirmation."""

    def __init__(self):
        super().__init__("detector_node")

        # --------------- parameters ---------------
        self.declare_parameter("model_path", "yolov8n.pt")
        self.declare_parameter("confidence_threshold", 0.45)
        self.declare_parameter("person_class_id", 0)          # COCO class 0 = person
        self.declare_parameter("temporal_window", 3)           # frames an ID must persist
        self.declare_parameter("camera_index", 0)              # /dev/video0
        self.declare_parameter("use_camera_topic", False)      # True → subscribe to image topic
        self.declare_parameter("camera_topic", "/camera/color/image_raw")
        self.declare_parameter("publish_rate", 10.0)           # Hz when using webcam directly
        self.declare_parameter("iou_match_threshold", 0.3)     # IoU for cross-frame matching

        self._model_path = self.get_parameter("model_path").value
        self._conf = self.get_parameter("confidence_threshold").value
        self._person_cls = self.get_parameter("person_class_id").value
        self._temporal_window = self.get_parameter("temporal_window").value
        self._cam_idx = self.get_parameter("camera_index").value
        self._use_topic = self.get_parameter("use_camera_topic").value
        self._cam_topic = self.get_parameter("camera_topic").value
        self._rate = self.get_parameter("publish_rate").value
        self._iou_thresh = self.get_parameter("iou_match_threshold").value

        # --------------- state ---------------
        self._bridge = CvBridge()
        self._model = None
        self._cap = None
        # track_id → consecutive‐frame count
        self._track_counts: dict[int, int] = defaultdict(int)
        self._seen_ids: set[int] = set()

        # --------------- pub / sub ---------------
        self._det_pub = self.create_publisher(
            Detection2DArray, "/detections", 10
        )

        if self._use_topic:
            self.create_subscription(
                Image,
                self._cam_topic,
                self._image_cb,
                QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT),
            )
            self.get_logger().info(f"Subscribed to {self._cam_topic}")
        else:
            self._cap = cv2.VideoCapture(self._cam_idx)
            if not self._cap.isOpened():
                self.get_logger().error(
                    f"Cannot open camera index {self._cam_idx}"
                )
            period = 1.0 / self._rate
            self.create_timer(period, self._timer_cb)
            self.get_logger().info(
                f"Using webcam {self._cam_idx} at {self._rate} Hz"
            )

        self._load_model()

    # ------------------------------------------------------------------ model
    def _load_model(self):
        global YOLO
        try:
            from ultralytics import YOLO as _YOLO
            YOLO = _YOLO
        except ImportError:
            self.get_logger().fatal(
                "ultralytics not installed — run: pip3 install ultralytics"
            )
            return

        self.get_logger().info(f"Loading YOLOv8 model: {self._model_path}")
        self._model = YOLO(self._model_path)
        self.get_logger().info("Model loaded.")

    # --------------------------------------------------------- input callbacks
    def _timer_cb(self):
        """Grab a frame from the webcam and run detection."""
        if self._cap is None or not self._cap.isOpened():
            return
        ret, frame = self._cap.read()
        if ret:
            self._detect(frame)

    def _image_cb(self, msg: Image):
        """Receive a frame from a ROS image topic."""
        frame = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self._detect(frame)

    # --------------------------------------------------------- core detection
    def _detect(self, frame: np.ndarray):
        if self._model is None:
            return

        results = self._model.predict(
            frame,
            conf=self._conf,
            classes=[self._person_cls],
            verbose=False,
        )

        det_array = Detection2DArray()
        det_array.header.stamp = self.get_clock().now().to_msg()
        det_array.header.frame_id = "camera_link"

        if len(results) == 0 or results[0].boxes is None:
            self._det_pub.publish(det_array)
            return

        boxes = results[0].boxes

        # ---- build current-frame detections ----
        current_ids: set[int] = set()

        for i in range(len(boxes)):
            conf = float(boxes.conf[i])
            cls_id = int(boxes.cls[i])
            x1, y1, x2, y2 = boxes.xyxy[i].tolist()

            # Use tracker ID if available, otherwise use index
            track_id = int(boxes.id[i]) if boxes.id is not None else i
            current_ids.add(track_id)

            # Update temporal count
            self._track_counts[track_id] += 1

            # Only publish if seen for enough consecutive frames
            if self._track_counts[track_id] < self._temporal_window:
                continue

            det = Detection2D()
            det.header = det_array.header

            # Bounding box centre + size
            det.bbox.center.position.x = (x1 + x2) / 2.0
            det.bbox.center.position.y = (y1 + y2) / 2.0
            det.bbox.size_x = float(x2 - x1)
            det.bbox.size_y = float(y2 - y1)

            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = str(cls_id)
            hyp.hypothesis.score = conf
            det.results.append(hyp)

            # Store track_id in the Detection2D id field
            det.id = str(track_id)

            det_array.detections.append(det)

        # Reset counts for IDs that disappeared this frame
        vanished = set(self._track_counts.keys()) - current_ids
        for tid in vanished:
            del self._track_counts[tid]

        self._det_pub.publish(det_array)

        if det_array.detections:
            self.get_logger().info(
                f"Published {len(det_array.detections)} confirmed detections"
            )

    # ---------------------------------------------------------------- cleanup
    def destroy_node(self):
        if self._cap is not None:
            self._cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = DetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()