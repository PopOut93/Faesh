class ScalingLoadBalancer:
    def __init__(self):
        self.servers = []
        self.user_sessions = {}

    def add_server(self, server_id: str):
        self.servers.append(server_id)

    def assign_user_session(self, user_id: int):
        # Simple round-robin example
        if not self.servers:
            raise ValueError("No servers available")
        server = self.servers[user_id % len(self.servers)]
        self.user_sessions[user_id] = server
        return server

    def get_session_server(self, user_id: int):
        return self.user_sessions.get(user_id)
