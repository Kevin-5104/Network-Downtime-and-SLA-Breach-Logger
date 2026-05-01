import datetime

class ReportGenerator:
    def __init__(self, database, sla_calculator):
        self.database = database
        self.sla_calculator = sla_calculator

    def generate(self, device_names, days=7):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"sla_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        lines = []
        lines.append("=" * 55)
        lines.append(f"  NETWORK SLA COMPLIANCE REPORT")
        lines.append(f"  Generated On : {now}")
        lines.append(f"  Period       : Last {days} Days")
        lines.append(f"  SLA Target   : {self.sla_calculator.sla_target}%")
        lines.append("=" * 55)

        for name in device_names:
            uptime = self.sla_calculator.calculate_uptime_percent(name, days)
            downtime = self.sla_calculator.get_total_downtime(name, days)
            breached = self.sla_calculator.is_sla_breached(name, days)
            status = "❌ SLA BREACHED" if breached else "✅ SLA MET"

            lines.append(f"\n  Device     : {name}")
            lines.append(f"  Uptime     : {uptime}%")
            lines.append(f"  Downtime   : {downtime:.1f} seconds")
            lines.append(f"  SLA Status : {status}")

        lines.append(f"\n{'=' * 55}")
        lines.append("  END OF REPORT")
        lines.append("=" * 55)

        # Save to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"\n📄 Report saved → {filename}")
        return filename