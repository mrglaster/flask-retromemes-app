from dataclasses import dataclass

@dataclass
class Post:
    """Dataclass containing information about one post"""
    id: int = -1
    author_id: int = 0
    text: str = ''
    image: str = ''
    date: str = '01.01.2022'
    like: int = 0
    dislike: int = 0

    def __init__(self, id, author_id, text, image, date, like, dislike):
        """Constructor for Post class"""
        self.id = id
        self.author_id = author_id
        self.text = text
        self.image = image
        self.date = date
        self.like = like
        self.dislike = dislike

    def __str__(self):
        """Override of toString method"""
        return f"({self.id}, {self.author_id}, {self.text}, {self.image}, {self.date}, {self.like}, {self.dislike})"




