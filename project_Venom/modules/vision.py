import cv2
from ultralytics import YOLO
from ai_core.core.logger import logger

_yolo_model = None


class VisionSystem:
    """
    Advanced Vision System using YOLOv8 (Ultralytics).
    Provides real-time object detection and scene analysis.
    """

    def __init__(self):
        logger.organ("VISION", "Initializing Optical Sensors (YOLOv8)...")
        try:
            # Check for CUDA
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
            if device == "cuda":
                logger.success(
                    f"Vision Acceleration Enabled: NVIDIA CUDA detected ({torch.cuda.get_device_name(0)})"
                )
            else:
                logger.warning("Vision Running on CPU (Slower). CUDA not found.")

            # Load a pretrained model (nano for speed)
            global _yolo_model
            if _yolo_model is None:
                _yolo_model = YOLO("yolov8n.pt")
            self.model = _yolo_model
            self.active = True
        except Exception as e:
            logger.error(f"Vision System Init Failed: {e}")
            self.active = False

    def analyze_frame(self, frame_path=None):
        """
        Captures from webcam if no path provided, runs YOLOv8.
        Returns a summary string of objects seen.
        """
        if not self.active:
            return "Vision System Offline."

        cap = None
        try:
            # 1. Capture Frame if None
            if frame_path is None:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    return "Blind: Camera inaccessible."

                # Warmup: Camera needs light adjustment
                for _ in range(15):
                    cap.read()

                ret, frame = cap.read()
                if not ret:
                    return "Blind: Vision feed capture failed."

                # frame is a numpy array (BGR)
                source_image = frame
            else:
                source_image = frame_path

            # 2. Run Inference
            # verbose=False to keep stdout clean
            results = self.model(source_image, verbose=False)

            detections = []
            if results and len(results) > 0:
                r = results[0]
                if hasattr(r, "boxes") and r.boxes is not None:
                    for box in r.boxes:
                        if box.cls is not None and len(box.cls) > 0:
                            cls_id = int(box.cls[0])
                            if box.conf is not None and len(box.conf) > 0:
                                conf = float(box.conf[0])
                                if (
                                    hasattr(self.model, "names")
                                    and cls_id in self.model.names
                                ):
                                    name = self.model.names[cls_id]
                                    if conf > 0.4:
                                        detections.append(name)

            if cap:
                cap.release()

            if not detections:
                return "I see nothing distinct right now."

            # Summarize (e.g., "2 person, 1 laptop")
            counts = {}
            for d in detections:
                counts[d] = counts.get(d, 0) + 1

            summary = ", ".join(
                [f"{count} {name}(s)" for name, count in counts.items()]
            )
            return f"I can see: {summary}"

        except Exception as e:
            if cap:
                cap.release()
            logger.error(f"Analysis Failed: {e}")
            return f"Visual processing error: {e}"

    async def see(self):
        """Capture visual input from the active camera (Webcam)."""
        return await self._async_analyze()

    async def _async_analyze(self):
        """Run analyze_frame in executor to avoid blocking."""
        import asyncio

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_frame)

    def start_stream(self):
        """
        Start continuous surveillance mode in a separate window.
        """
        if not self.active:
            return "Vision Offline"

        cap = cv2.VideoCapture(0)
        logger.organ("VISION", "Surveillance Mode Active (Press 'q' in window to stop)")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Predict
            results = self.model(frame, verbose=False)
            annotated_frame = results[0].plot()

            cv2.imshow("VENOM SURVEILLANCE FEED", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return "Surveillance Logged."


if __name__ == "__main__":
    # Test
    v = VisionSystem()
    print(v.active)
