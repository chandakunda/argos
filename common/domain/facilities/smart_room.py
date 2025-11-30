# Smart rooms extend Room → making this inheritance level 3 and 4+.
# We also define SmartLectureRoom (5th level) to satisfy assignment requirements.

from .room import Room


class SmartRoom(Room):
    def __init__(self, name: str, location: str, capacity: int, automation_level: str, **kwargs):
        super().__init__(name, location, capacity, **kwargs)
        self.automation_level = automation_level  # e.g., BASIC, ADVANCED

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "automation_level": self.automation_level
        })
        return base


class SmartLectureRoom(SmartRoom):
    # This is level 5 in the inheritance chain.
    def __init__(self, name: str, location: str, capacity: int, automation_level: str, has_projector: bool, **kwargs):
        super().__init__(name, location, capacity, automation_level, **kwargs)
        self.has_projector = has_projector

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "has_projector": self.has_projector
        })
        return base
