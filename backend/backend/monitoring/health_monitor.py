import time
import random

class HealthMonitor:
    def __init__(self):
        self.services = {}
        self.alerts = []

    def register_service(self, name: str):
        self.services[name] = "healthy"

    def check_services(self):
        for service in self.services:
            # Simulated health check
            status = random.choice(["healthy", "degraded", "down"])
            self.services[service] = status

            if status != "healthy":
                self.trigger_alert(service, status)

    def trigger_alert(self, service, status):
        alert = f"[ALERT] {service.upper()} is {status.upper()}"
        self.alerts.append(alert)
        print(alert)

    def get_status(self):
        return self.services
3️⃣ Optional Test (Recommended)
Create backend/monitoring/test_monitor.py:

python
Copy code
from health_monitor import HealthMonitor

monitor = HealthMonitor()
monitor.register_service("auth")
monitor.register_service("payments")
monitor.register_service("avatar_engine")

monitor.check_services()
print(monitor.get_status())
