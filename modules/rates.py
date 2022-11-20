from dataclasses import dataclass


@dataclass
class Rates:
    id: int
    real_likes: str
    real_dislikes: str

    def __init__(self, id, real_likes, real_dislikes):
        self.id = id
        self.real_dislikes = real_dislikes
        self.real_likes = real_likes

    def __str__(self):
        return f"( {self.id}, {self.real_likes}, {self.real_dislikes} )"
