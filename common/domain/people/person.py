from abc import ABC
from typing import List
from .roles import RoleAssignment, RoleType
from ..base.abstract_entity import AbstractEntity


class Person(AbstractEntity, ABC):
    def __init__(self, name: str, email: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.roles: List[RoleAssignment] = []

    def assign_role(self, role: RoleType):
        self.roles.append(RoleAssignment(role))
        self.update_version()

    def get_roles(self):
        return [r.role for r in self.roles]

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "email": self.email,
            "roles": [r.to_dict() for r in self.roles]
        })
        return base
