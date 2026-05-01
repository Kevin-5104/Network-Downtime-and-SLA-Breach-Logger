import datetime

class SLACalculator:
    def __init__(self, database, sla_target=99.9):
        self.database = database
        self.sla_target = sla_target  # 99.9% default

    def get_total_downtime(self, device_name, days=7):
        logs = self.database.get_all_logs()
        total_downtime = 0

        for log in logs:
            if log[1] == device_name:  # log[1] is device_name column
                total_downtime += log[5]  # log[5] is duration_seconds

        return total_downtime

    def calculate_uptime_percent(self, device_name, days=7):
        total_seconds = days * 24 * 60 * 60  # total seconds in the period
        downtime = self.get_total_downtime(device_name, days)
        uptime = total_seconds - downtime
        uptime_percent = (uptime / total_seconds) * 100
        return round(uptime_percent, 4)

    def is_sla_breached(self, device_name, days=7):
        uptime = self.calculate_uptime_percent(device_name, days)
        return uptime < self.sla_target

    def get_summary(self, device_names, days=7):
        print(f"\n{'='*55}")
        print(f"  SLA COMPLIANCE REPORT — Last {days} Days")
        print(f"  SLA Target: {self.sla_target}%")
        print(f"{'='*55}")

        for name in device_names:
            uptime = self.calculate_uptime_percent(name, days)
            breached = self.is_sla_breached(name, days)
            downtime_sec = self.get_total_downtime(name, days)
            status = "❌ BREACHED" if breached else "✅ MET"

            print(f"\n  Device     : {name}")
            print(f"  Uptime     : {uptime}%")
            print(f"  Downtime   : {downtime_sec:.1f} seconds")
            print(f"  SLA Status : {status}")

        print(f"\n{'='*55}\n")