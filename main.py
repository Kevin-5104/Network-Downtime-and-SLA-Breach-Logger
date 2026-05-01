import time
from device import Device
from database import Database
from ping_monitor import PingMonitor
from sla_calculator import SLACalculator
from report_generator import ReportGenerator

db = Database()

devices = [
    Device("Google DNS", "8.8.8.8", "Cloud"),
    Device("Cloudflare DNS", "1.1.1.1", "Cloud"),
    Device("Localhost", "127.0.0.1", "My Machine")
]

monitors = [PingMonitor(d, db) for d in devices]
sla = SLACalculator(db, sla_target=99.9)
report = ReportGenerator(db, sla)

print("🚀 Monitoring started... Press Ctrl+C to stop\n")

try:
    while True:
        for monitor in monitors:
            monitor.check()
        print("---")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n🛑 Monitoring stopped.")

    device_names = [d.name for d in devices]
    sla.get_summary(device_names, days=7)
    report.generate(device_names, days=7)

    db.close()