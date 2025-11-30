from ..base.abstract_entity import AbstractEntity


class Syllabus(AbstractEntity):
    def __init__(self, course_id: str, topics: list, **kwargs):
        super().__init__(**kwargs)
        self.course_id = course_id
        self.topics = topics
