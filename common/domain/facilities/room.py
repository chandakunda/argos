# Room extends Facility → this is inheritance level 2.
# Rooms belong to facilities and may contain resources.

from .facility import Facility


class Room(Facility):
    def __init__(self, name: str, location: str, capacity: int, **kwargs):
        super().__init__(name, location, **kwargs)
        self.capacity = capacity
        self.resources = []  # list of Resource objects

    def add_resource(self, resource):
        self.resources.append(resource)
        self.update_version()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "capacity": self.capacity,
            "resources": [r.to_dict() for r in self.resources]
        })
        return base
