from ..base.abstract_entity import AbstractEntity


class Assessment(AbstractEntity):
    def __init__(self, section_id: str, name: str, max_score: float, **kwargs):
        super().__init__(**kwargs)
        self.section_id = section_id
        self.name = name
        self.max_score = max_score
