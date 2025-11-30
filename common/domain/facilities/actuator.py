# ActuatorResource is a Resource that performs actions.
# Examples: smart light switch, electronic door lock.

from .resource import Resource


class ActuatorResource(Resource):
    def __init__(self, name: str, action_type: str, **kwargs):
        super().__init__(name, **kwargs)
        self.action_type = action_type  # e.g., OPEN_DOOR, TURN_LIGHT_ON

    def perform_action(self, action: str):
        # Simple simulation of performing an action
        self.status = f"Performed: {action}"
        self.update_version()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "action_type": self.action_type
        })
        return base
