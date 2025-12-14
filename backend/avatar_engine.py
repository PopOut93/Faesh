class Avatar:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.body_mesh = None  # Placeholder for 3D mesh
        self.clothing_items = []

    def load_body_mesh(self, mesh_data):
        self.body_mesh = mesh_data
        return f"Mesh loaded for user {self.user_id}"

    def add_clothing_item(self, item):
        self.clothing_items.append(item)
        return f"Added {item} to user {self.user_id} avatar"
