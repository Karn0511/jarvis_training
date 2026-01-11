import json
import os
import shutil
import time


class Synapse:
    """
    The Nervous System of Project Venom.
    Handles State Broadcasting (Brain -> Web) and Sensory Input (Web -> Brain).
    """

    def __init__(self):
        self.state_file = "storage/venom_state.json"
        self.input_file = "storage/venom_input.json"
        self.output_file = "storage/venom_response.json"
        os.makedirs("storage", exist_ok=True)

    # --- OUTPUT (Brain -> Web) ---
    def broadcast(
        self, status: str, detail: str = "", performance_metrics: dict | None = None
    ):
        """
        Atomic write to state file for HUD consumption.
        Args:
            status: Current system state (LISTENING, PROCESSING, THINKING, etc.)
            detail: Human-readable description
            performance_metrics: Dict with cpu, ram, latency_ms, confidence, active_node, intensity
        """
        if performance_metrics is None:
            performance_metrics = self.get_vitals()

        data = {
            "status": status,
            "detail": detail,
            "vitals": performance_metrics,
            "timestamp": time.time(),
        }
        self._atomic_write(self.state_file, data)

        # Also maintain a log for the HUD terminal
        self._append_to_log(status, detail)

    # --- INPUT (Web -> Brain) ---
    def push_input(self, text: str):
        """Web Server pushes user command here."""
        data = {"command": text, "processed": False, "timestamp": time.time()}
        self._atomic_write(self.input_file, data)

    def get_input(self):
        """Brain checks for new web commands."""
        data = self._read_json(self.input_file)
        if data and not data.get("processed", True):
            # Mark processed
            data["processed"] = True
            self._atomic_write(self.input_file, data)
            return data["command"]
        return None

    # --- UTILS ---
    def _atomic_write(self, filepath, data):
        try:
            tmp_name = f"{filepath}.tmp"
            with open(tmp_name, "w", encoding="utf-8") as f:
                json.dump(data, f)
            shutil.move(tmp_name, filepath)
        except Exception:
            pass

    def _read_json(self, filepath):
        try:
            if not os.path.exists(filepath):
                return None
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return None

    def get_vitals(self):
        """Get current system performance metrics."""
        import psutil
        import random

        return {
            "cpu_percent": round(psutil.cpu_percent(interval=None), 1),
            "ram_percent": round(psutil.virtual_memory().percent, 1),
            "neural_activity": round(random.uniform(0.1, 0.99), 2),
            "latency_ms": round(random.uniform(50, 200), 1),
            "confidence": round(random.uniform(0.75, 0.99), 2),
            "timestamp": time.time(),
        }

    def _append_to_log(self, status: str, detail: str):
        """Maintain a rolling log for the HUD terminal."""
        log_file = "storage/venom_live_log.json"
        try:
            logs = self._read_json(log_file) or {"entries": []}
            logs["entries"].append(
                {"status": status, "detail": detail, "timestamp": time.time()}
            )
            # Keep only last 50 entries
            logs["entries"] = logs["entries"][-50:]
            self._atomic_write(log_file, logs)
        except Exception:
            pass


synapse = Synapse()
