# Facility represents a building or major campus area.
# It extends AbstractEntity and serves as the root for the facility hierarchy.

from ..base.abstract_entity import AbstractEntity


class Facility(AbstractEntity):
    def __init__(self, name: str, location: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.location = location

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "location": self.location
        })
        return base
