"""VENOM Immortality Daemon - Auto-restart system on crashes."""

import codecs
import os
import subprocess
import sys
import time
from datetime import datetime

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        else:
            # Fallback for Python < 3.7
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
    except (AttributeError, TypeError):
        pass  # Silently continue if encoding fails


class VenomDaemon:
    """
    The Immortality System - Keeps Venom alive forever.
    Monitors the main process and automatically restarts on crashes.
    """

    def __init__(self):
        self.crash_log = "storage/crash_report.log"
        self.restart_count = 0
        self.max_rapid_restarts = 5
        self.rapid_restart_window = 60  # seconds
        self.restart_times = []

    def log_crash(self, error_msg: str):
        """Log crash information to file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.crash_log, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"CRASH REPORT - {timestamp}\n")
            f.write(f"Restart Count: {self.restart_count}\n")
            f.write(f"Error: {error_msg}\n")
            f.write(f"{'='*80}\n")

    def check_rapid_restart(self):
        """Check if we're in a rapid restart loop (crash loop)."""
        current_time = time.time()

        # Remove old restart times outside the window
        self.restart_times = [
            t
            for t in self.restart_times
            if current_time - t < self.rapid_restart_window
        ]

        # Add current restart
        self.restart_times.append(current_time)

        # Check if too many restarts
        if len(self.restart_times) >= self.max_rapid_restarts:
            return True
        return False

    def run_forever(self):
        """Main daemon loop - keeps Venom alive."""
        print("=" * 80)
        print("[DAEMON] VENOM DAEMON INITIALIZED")
        print("=" * 80)
        print("Mission: Ensure biological immortality of Project Venom")
        print("Status: ACTIVE")
        print("=" * 80)

        while True:
            try:
                print(
                    f"\n[{datetime.now().strftime('%H:%M:%S')}] [DAEMON] Launching Venom Core..."
                )

                # Launch main.py with UTF-8 encoding
                process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    encoding="utf-8",
                    errors="replace",  # Replace undecodable bytes
                )

                # Stream output in real-time
                while True:
                    output = process.stdout.readline()
                    if output:
                        print(output.strip())

                    # Check if process is still running
                    return_code = process.poll()
                    if return_code is not None:
                        # Process has terminated
                        break

                # Get any remaining output
                stdout, stderr = process.communicate()
                if stdout:
                    print(stdout)
                if stderr:
                    print(stderr, file=sys.stderr)

                # Check return code
                if return_code == 0:
                    print("\n[DAEMON] Venom terminated gracefully (exit code 0)")
                    print("[DAEMON] Assuming intentional shutdown. Exiting daemon.")
                    break
                else:
                    # Crash detected
                    error_msg = f"Exit code: {return_code}"
                    if stderr:
                        error_msg += f"\nStderr: {stderr}"

                    self.restart_count += 1
                    self.log_crash(error_msg)

                    print(f"\n{'!'*80}")
                    print(f"[DAEMON] [!] CRASH DETECTED - Exit Code: {return_code}")
                    print(f"[DAEMON] Restart Count: {self.restart_count}")
                    print(f"{'!'*80}")

                    # Check for rapid restart loop
                    if self.check_rapid_restart():
                        print(
                            "\n[DAEMON] [ERROR] CRITICAL: Rapid restart loop detected!"
                        )
                        print(
                            f"[DAEMON] {self.max_rapid_restarts} crashes in {self.rapid_restart_window}s"
                        )
                        print("[DAEMON] Entering safe mode - waiting 30 seconds...")
                        time.sleep(30)
                        self.restart_times.clear()

                    # Wait before restart
                    wait_time = 3
                    print("\n[DAEMON] [REBOOT] BIOLOGICAL REBOOT INITIATED...")
                    print(f"[DAEMON] Waiting {wait_time} seconds before restart...")
                    time.sleep(wait_time)

                    print("[DAEMON] [OK] Restarting Venom Core...\n")

            except KeyboardInterrupt:
                print("\n\n[DAEMON] Manual shutdown requested (Ctrl+C)")
                print("[DAEMON] Terminating Venom Core...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception:
                    process.kill()
                print("[DAEMON] Daemon shutdown complete.")
                break

            except Exception as e:
                self.restart_count += 1
                error_msg = f"Daemon exception: {str(e)}"
                self.log_crash(error_msg)

                print(f"\n[DAEMON] [!] Daemon exception: {e}")
                print("[DAEMON] Attempting recovery in 5 seconds...")
                time.sleep(5)


if __name__ == "__main__":
    daemon = VenomDaemon()
    daemon.run_forever()
