from .person import Person
from .roles import RoleType


class Lecturer(Person):
    def __init__(self, name: str, email: str, **kwargs):
        super().__init__(name, email, **kwargs)
        self.assign_role(RoleType.LECTURER)
