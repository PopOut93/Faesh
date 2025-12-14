class RedundancyFailover:
    def __init__(self):
        self.primary_servers = []
        self.secondary_servers = []

    def add_primary_server(self, server_id: str):
        self.primary_servers.append(server_id)

    def add_secondary_server(self, server_id: str):
        self.secondary_servers.append(server_id)

    def get_active_server(self, user_id: int):
        # Round-robin failover logic
        if not self.primary_servers:
            raise ValueError("No primary servers available")
        primary_server = self.primary_servers[user_id % len(self.primary_servers)]
        # Check failover to secondary if needed
        return primary_server
