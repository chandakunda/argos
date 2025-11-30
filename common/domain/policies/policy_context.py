# PolicyContext standardizes how data is passed to policies.
# Used for Enrollment, Security, Access Control, etc.

class PolicyContext:
    def __init__(self, subject=None, resource=None, action=None, metadata=None):
        """
        subject: The actor performing an action (e.g., Student, Staff)
        resource: The target entity (e.g., Course, Room)
        action: The permission or requested operation
        metadata: Extra information needed by policies
        """
        self.subject = subject
        self.resource = resource
        self.action = action
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "subject": str(self.subject),
            "resource": str(self.resource),
            "action": self.action,
            "metadata": self.metadata
        }
