from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable


@dataclass
class Room:
    room_id: str
    capacity: int
    base_energy_cost: float  # cost per time slot to keep the room running


@dataclass
class ClassRequest:
    section_id: str
    expected_students: int
    timeslot: str  # simple string label, e.g. "MON-09:00"


@dataclass
class RoomAssignment:
    section_id: str
    room_id: str
    timeslot: str
    utilization: float
    cost: float


class RoomUsageOptimizer:
    """
    Very simple heuristic room usage optimizer.

    Goal:
        Minimize the sum of:
          - energy cost
          - underutilization penalty

    This is *not* an exact solver; it's a deterministic greedy algorithm
    intended to be easy to understand and demonstrate in the assignment.

    Example usage:

        optimizer = RoomUsageOptimizer()
        rooms = [
            Room("R1", capacity=50, base_energy_cost=10.0),
            Room("R2", capacity=30, base_energy_cost=7.0),
        ]
        classes = [
            ClassRequest("SEC-1", expected_students=40, timeslot="MON-09"),
            ClassRequest("SEC-2", expected_students=25, timeslot="MON-09"),
        ]
        assignments = optimizer.optimize(rooms, classes)
    """

    def __init__(
        self,
        underutilization_penalty: float = 1.0,
        over_capacity_penalty: float = 100.0,
    ):
        self.underutilization_penalty = underutilization_penalty
        self.over_capacity_penalty = over_capacity_penalty

    def optimize(
        self,
        rooms: Iterable[Room],
        class_requests: Iterable[ClassRequest],
    ) -> List[RoomAssignment]:
        """
        Greedy heuristic:

        For each timeslot:
            - consider all classes in that slot
            - for each class, pick the room that:
                * has enough capacity
                * yields minimal cost = base_energy_cost + underutilization_penalty * (capacity - expected_students)
            - if no room has enough capacity, assign the room with *largest* capacity
              and add a heavy over_capacity_penalty.

        Returns a list of RoomAssignment objects.
        """
        rooms = list(rooms)
        class_requests = list(class_requests)
        assignments: List[RoomAssignment] = []

        # Group classes by timeslot
        by_timeslot: Dict[str, List[ClassRequest]] = {}
        for cr in class_requests:
            by_timeslot.setdefault(cr.timeslot, []).append(cr)

        for timeslot, classes in by_timeslot.items():
            # For each class in this timeslot, pick best room
            for cr in classes:
                best_room = None
                best_cost = float("inf")
                best_utilization = 0.0

                for room in rooms:
                    if room.capacity >= cr.expected_students:
                        # Underutilization penalty
                        unused = room.capacity - cr.expected_students
                        cost = room.base_energy_cost + self.underutilization_penalty * unused
                        utilization = cr.expected_students / room.capacity
                    else:
                        # Over capacity - strongly penalize but still consider
                        unused = 0
                        cost = (
                            room.base_energy_cost
                            + self.over_capacity_penalty * (cr.expected_students - room.capacity)
                        )
                        utilization = 1.0  # forced full

                    if cost < best_cost:
                        best_cost = cost
                        best_room = room
                        best_utilization = utilization

                if best_room is None:
                    # Should not happen if rooms list is non-empty
                    continue

                assignments.append(
                    RoomAssignment(
                        section_id=cr.section_id,
                        room_id=best_room.room_id,
                        timeslot=timeslot,
                        utilization=round(best_utilization, 3),
                        cost=round(best_cost, 2),
                    )
                )

        return assignments
