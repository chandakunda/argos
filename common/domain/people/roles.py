from datetime import datetime
from enum import Enum


class RoleType(Enum):
    STUDENT = "STUDENT"
    LECTURER = "LECTURER"
    STAFF = "STAFF"
    TA = "TEACHING_ASSISTANT"
    ADMIN = "ADMIN"
    SECURITY = "SECURITY"
    GUEST = "GUEST"


class RoleAssignment:
    def __init__(self, role: RoleType, assigned_at=None):
        self.role = role
        self.assigned_at = assigned_at or datetime.utcnow()

    def to_dict(self):
        return {
            "role": self.role.value,
            "assigned_at": self.assigned_at.isoformat()
        }
