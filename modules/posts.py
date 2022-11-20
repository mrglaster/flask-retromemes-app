from dataclasses import dataclass

@dataclass
class Post:
    """Dataclass containing information about one post"""
    id: int = -1
    author_id: int = 0
    text: str = ''
    date: str = '01.01.2022'
    like: int = 0
    dislike: int = 0

    def __init__(self, id, author_id, text, date, like, dislike):
        """Constructor for Post class"""
        self.id = id
        self.author_id = author_id
        self.text = text
        self.date = date
        self.like = like
        self.dislike = dislike

    def __str__(self):
        """Override of toString method"""
        return f"({self.id}, {self.author_id}, {self.text}, {self.date}, {self.like}, {self.dislike})"



def add_user(database_connection, post):
    pass


