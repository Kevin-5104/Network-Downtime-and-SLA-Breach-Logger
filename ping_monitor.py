import subprocess
import platform
import datetime

class PingMonitor:
    def __init__(self, device, database):
        self.device = device
        self.database = database
        self.down_since = None  # records when device went down

    def ping(self):
        # Windows aur Linux ke liye alag command
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", self.device.ip]

        result = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result == 0  # True = online, False = offline

    def check(self):
        is_reachable = self.ping()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not is_reachable and self.device.is_online:
            # Device just went DOWN
            self.device.is_online = False
            self.down_since = datetime.datetime.now()
            print(f"[{now}] ❌ DOWN → {self.device.name} ({self.device.ip})")

        elif is_reachable and not self.device.is_online:
            # Device just came BACK UP
            self.device.is_online = True
            up_time = datetime.datetime.now()
            duration = (up_time - self.down_since).total_seconds()

            self.database.log_downtime(
                self.device.name,
                self.device.ip,
                self.down_since.strftime("%Y-%m-%d %H:%M:%S"),
                up_time.strftime("%Y-%m-%d %H:%M:%S"),
                duration
            )
            print(f"[{now}] ✅ BACK UP → {self.device.name} | Downtime: {duration:.1f} seconds")

        else:
            status = "✅ ONLINE" if is_reachable else "❌ STILL DOWN"
            print(f"[{now}] {status} → {self.device.name} ({self.device.ip})")