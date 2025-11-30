from ..base.abstract_entity import AbstractEntity


class Course(AbstractEntity):
    def __init__(self, code: str, title: str, description: str = "", **kwargs):
        super().__init__(**kwargs)
        self.code = code
        self.title = title
        self.description = description

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "code": self.code,
            "title": self.title,
            "description": self.description
        })
        return base
