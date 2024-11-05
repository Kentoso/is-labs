import yaml
import random
import copy


class TimeSlot:
    def __init__(self, day: str, time: str):
        self.day: str = day
        self.time: str = time

    def __eq__(self, value: object) -> bool:
        return value is not None and self.day == value.day and self.time == value.time

    def __str__(self) -> str:
        return f"{self.day}, {self.time}"

    def __repr__(self) -> str:
        return f"{self.day}, {self.time}"

    def __hash__(self) -> int:
        return hash((self.day, self.time))


class Subject:
    def __init__(self, name, hours):
        self.name: str = name
        self.hours: int = hours

    def __eq__(self, value: object) -> bool:
        return (
            value is not None and self.name == value.name and self.hours == value.hours
        )

    def __str__(self) -> str:
        return f"Subject: {self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.hours))


class Group:
    def __init__(self, name, capacity, subject_names):
        self.name: str = name
        self.capacity: int = capacity
        self.subject_names: list[str] = [subject_name for subject_name in subject_names]
        self.subjects: list[Subject] = None

    def __eq__(self, value: object) -> bool:
        return (
            value is not None
            and self.name == value.name
            and self.capacity == value.capacity
        )

    def __str__(self) -> str:
        return f"Group: {self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))


class Lecturer:
    def __init__(self, name: str, can_teach_subjects_names: list[Subject]) -> None:
        self.name: str = name
        self.can_teach_subjects_names: list[str] = can_teach_subjects_names
        self.can_teach_subjects: list[Subject] = None

    def __eq__(self, value: object) -> bool:
        return value is not None and self.name == value.name

    def __str__(self) -> str:
        return f"Lecturer: {self.name}"

    def __hash__(self) -> int:
        return hash(self.name)


class Hall:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __eq__(self, value: object) -> bool:
        return (
            value is not None
            and self.name == value.name
            and self.capacity == value.capacity
        )

    def __str__(self) -> str:
        return f"{self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))


class Slot:
    def __init__(
        self,
        group: Group,
        subject: Subject,
        lecturer: Lecturer = None,
        hall: Hall = None,
        time_slot: TimeSlot = None,
    ):
        self.group = group
        self.subject = subject
        self.lecturer = lecturer
        self.hall = hall
        self.time_slot = time_slot

    def __eq__(self, value: object) -> bool:
        return (
            self.group == value.group
            and self.subject == value.subject
            and self.lecturer == value.lecturer
            and self.hall == value.hall
            and self.time_slot == value.time_slot
        )

    def __str__(self) -> str:
        return f"Group: {self.group.name}, Subject: {self.subject.name}, Lecturer: {self.lecturer}, Hall: {self.hall}, Time Slot: {self.time_slot}"

    def __repr__(self) -> str:
        return f"Group: {self.group.name}, Subject: {self.subject.name}, Lecturer: {self.lecturer}, Hall: {self.hall}, Time Slot: {self.time_slot}"

    def __hash__(self) -> int:
        return hash(
            (self.group, self.subject, self.lecturer, self.hall, self.time_slot)
        )


class Schedule:
    def __init__(self):
        self.grid: list[Slot] = []

    def mutate_slot(self, slot):
        pass

    def _find_timeslot_conficts_for_all_groups(self):
        time_slots = {}
        for slot in self.grid:
            if slot.group is None:
                continue
            if slot.group.name not in time_slots:
                time_slots[slot.group.name] = []
            time_slots[slot.group.name].append(slot.time_slot)
        conflicts = {}
        for group, slots in time_slots.items():
            conflicts[group] = []
            for slot in slots:
                if slot is not None and slots.count(slot) > 1:
                    conflicts[group].append(slot)
        return conflicts

    def _find_timeslot_conflicts_for_all_halls(self):
        time_slots = {}
        for slot in self.grid:
            if slot.hall is None:
                continue
            if slot.hall.name not in time_slots:
                time_slots[slot.hall.name] = []
            time_slots[slot.hall.name].append(slot.time_slot)
        conflicts = {}
        for hall, slots in time_slots.items():
            conflicts[hall] = []
            for slot in slots:
                if slot is not None and slots.count(slot) > 1:
                    conflicts[hall].append(slot)
        return conflicts

    def _find_timeslot_conflicts_for_all_lecturers(self):
        time_slots = {}
        for slot in self.grid:
            if slot.lecturer is None:
                continue
            if slot.lecturer.name not in time_slots:
                time_slots[slot.lecturer.name] = []
            time_slots[slot.lecturer.name].append(slot.time_slot)
        conflicts = {}
        for lecturer, slots in time_slots.items():
            conflicts[lecturer] = []
            for slot in slots:
                if slot is not None and slots.count(slot) > 1:
                    conflicts[lecturer].append(slot)
        return conflicts

    def is_valid(self):
        group_conflicts = self._find_timeslot_conficts_for_all_groups()
        hall_conflicts = self._find_timeslot_conflicts_for_all_halls()
        lecturer_conflicts = self._find_timeslot_conflicts_for_all_lecturers()

        return (
            (
                not any(group_conflicts.values())
                and not any(hall_conflicts.values())
                and not any(lecturer_conflicts.values())
            ),
            group_conflicts,
            hall_conflicts,
            lecturer_conflicts,
        )

    def crossover(self, other):
        child = Schedule()
        child.grid = self.grid.copy()

        other_slots = other.grid
        for i in range(len(self.grid)):
            if random.random() > 0.5:
                child.grid[i] = other_slots[i]

        return child

    def __str__(self) -> str:
        return "\n".join([str(slot) for slot in self.grid])

    def to_time_slot_oriented_view(self):
        time_slots = {}
        for slot in self.grid:
            if slot.time_slot is None:
                continue
            if slot.time_slot not in time_slots:
                time_slots[f"{slot.time_slot.day} + {slot.time_slot.time}"] = []
            time_slots[f"{slot.time_slot.day} + {slot.time_slot.time}"].append(slot)

        sorted_keys = sorted(time_slots.keys(), key=lambda x: x)
        time_slots = {
            k: time_slots[k] for k in sorted_keys if time_slots[k] is not None
        }
        return time_slots


class ScheduleManager:
    def __init__(self):
        self.time_slots: list[TimeSlot] = None
        self.subjects: list[Subject] = None
        self.groups: list[Group] = None
        self.lecturers: list[Lecturer] = None
        self.halls: list[Hall] = None

    def from_yaml(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            self.time_slots = [
                TimeSlot(**time_slot) for time_slot in data["time_slots"]
            ]
            self.subjects = [Subject(**subject) for subject in data["subjects"]]
            self.groups = [Group(**group) for group in data["groups"]]
            self.lecturers = [Lecturer(**lecturer) for lecturer in data["lecturers"]]
            self.halls = [Hall(**hall) for hall in data["halls"]]

    def create_empty_schedule(self):
        schedule = Schedule()
        for group in self.groups:
            for subject in group.subject_names:
                s = next((s for s in self.subjects if s.name == subject), None)
                for i in range(s.hours):
                    schedule.grid.append(
                        Slot(
                            group=group,
                            subject=s,
                        )
                    )

        return schedule

    def _get_available_time_slots_for_hall_and_lecturer_and_group(
        self, schedule: Schedule, hall: Hall, lecturer: Lecturer, group: Group
    ):
        grid = schedule.grid
        allowed_time_slots = [ts for ts in self.time_slots]
        busy_time_slots = []
        for s in grid:
            if s.hall == hall:
                busy_time_slots.append(s.time_slot)
            if s.lecturer == lecturer:
                busy_time_slots.append(s.time_slot)
            if s.group == group:
                busy_time_slots.append(s.time_slot)

        return sorted(
            list(set(allowed_time_slots) - set(busy_time_slots)),
            key=lambda x: (x.day, x.time),
        )

    def _get_available_lecturers_for_time_slot_and_subject(
        self, schedule: Schedule, time_slot: TimeSlot, subject: Subject
    ):
        if time_slot is None:
            return []

        grid = schedule.grid
        allowed_lecturers = [
            l for l in self.lecturers if subject.name in l.can_teach_subjects_names
        ]
        busy_lecturers = []
        for s in grid:
            if s.time_slot == time_slot:
                busy_lecturers.append(s.lecturer)

        return sorted(
            list(set(allowed_lecturers) - set(busy_lecturers)), key=lambda x: x.name
        )

    def _get_available_halls_for_time_slot_and_group(
        self, schedule: Schedule, time_slot: TimeSlot, group: Group
    ):
        grid = schedule.grid
        busy_halls = []
        allowed_halls = [h for h in self.halls if group.capacity <= h.capacity]
        for s in grid:
            if s.time_slot == time_slot:
                busy_halls.append(s.hall)

        return sorted(list(set(allowed_halls) - set(busy_halls)), key=lambda x: x.name)

    def mutate_schedule(self, schedule: Schedule):
        grid = schedule.grid
        slot_index = random.randint(0, len(grid) - 1)
        slot = grid[slot_index]
        new_slot = copy.copy(slot)
        what_to_mutate = random.choice(["hall", "lecturer", "time_slot"])
        did_mutate = False
        if what_to_mutate == "hall":
            available_halls = self._get_available_halls_for_time_slot_and_group(
                schedule, slot.time_slot, slot.group
            )
            if len(available_halls) == 0:
                return schedule, False
            new_slot.hall = random.choice(available_halls)
            did_mutate = True
        elif what_to_mutate == "lecturer":
            available_lecturers = (
                self._get_available_lecturers_for_time_slot_and_subject(
                    schedule, slot.time_slot, slot.subject
                )
            )
            if len(available_lecturers) == 0:
                return schedule, False
            new_slot.lecturer = random.choice(available_lecturers)
            did_mutate = True
        else:
            avaliable_time_slots = (
                self._get_available_time_slots_for_hall_and_lecturer_and_group(
                    schedule, slot.hall, slot.lecturer, slot.group
                )
            )
            if len(avaliable_time_slots) == 0:
                return schedule, False
            new_slot.time_slot = random.choice(avaliable_time_slots)
            did_mutate = True

        new_schedule = copy.copy(schedule)
        new_schedule.grid[slot_index] = new_slot

        return new_schedule, did_mutate

    def init_random_schedule(self):
        schedule = self.create_empty_schedule()

        i = 0
        while i < 1000:
            schedule, _ = self.mutate_schedule(schedule)
            i += 1

        return schedule
