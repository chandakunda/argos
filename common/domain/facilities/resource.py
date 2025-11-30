# Base class for campus resources like sensors and actuators.
# This class is abstract.

from abc import ABC
from ..base.abstract_entity import AbstractEntity


class Resource(AbstractEntity, ABC):
    def __init__(self, name: str, status: str = "OFFLINE", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.status = status  # e.g. ONLINE, OFFLINE

    def set_status(self, status: str):
        self.status = status
        self.update_version()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "status": self.status
        })
        return base
