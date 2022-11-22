from dataclasses import dataclass


@dataclass
class Rates:
    id: int
    history_id: int

    def __init__(self, id, history_id):
        self.id = id
        self.history_id = history_id

    def __str__(self):
        return f"( {self.id}, {self.hostory_id})"
