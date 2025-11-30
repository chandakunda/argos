from ..base.abstract_entity import AbstractEntity


class Section(AbstractEntity):
    def __init__(self, course_id: str, section_number: str, schedule: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.course_id = course_id
        self.section_number = section_number
        self.schedule = schedule or {}

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "course_id": self.course_id,
            "section_number": self.section_number,
            "schedule": self.schedule
        })
        return base
