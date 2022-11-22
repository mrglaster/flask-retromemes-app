from dataclasses import dataclass

@dataclass
class History:
    id: int
    post_id: int
    user_id: int
    action: int

    def __init__(self, id, post_id, user_id, action):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.action = action