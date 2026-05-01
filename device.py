class Device:
    def __init__(self, name, ip, location):
        self.name = name
        self.ip = ip
        self.location = location
        self.is_online = True  # assume online at start

    def __str__(self):
        status = "ONLINE" if self.is_online else "OFFLINE"
        return f"[{status}] {self.name} | IP: {self.ip} | Location: {self.location}"