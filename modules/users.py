from dataclasses import dataclass

@dataclass
class User:
    """Dataclass containing data bout one user"""
    id: int
    login: str
    password: str
    avatar: str
    email: str

    def __init__(self, id, login, password, avatar, email):
        """User class constructor"""
        self.id = id
        self.login = login
        self.password = password
        self.avatar = avatar
        self.email = email

    def __str__(self):
        """Override of toString method"""
        return f"({self.id}, {self.login}, {self.login}, {self.password}, {self.avatar}, {self.email})"
