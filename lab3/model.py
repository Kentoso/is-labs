import yaml


class Subject:
    def __init__(self, name, hours):
        self.name: str = name
        self.hours: int = hours

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.hours == value.hours

    def __str__(self) -> str:
        return f"Subject: {self.name}, Hours: {self.hours}"


class Group:
    def __init__(self, name, capacity, subject_names):
        self.name: str = name
        self.capacity: int = capacity
        self.subject_names: list[str] = [subject_name for subject_name in subject_names]
        self.subjects: list[Subject] = None

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.capacity == value.capacity

    def __str__(self) -> str:
        return f"Group: {self.name}, Capacity: {self.capacity}, Subjects: {self.subject_names}"


class Lecturer:
    def __init__(self, name: str, can_teach_subjects_names: list[Subject]) -> None:
        self.name: str = name
        self.can_teach_subjects_names: list[str] = can_teach_subjects_names
        self.can_teach_subjects: list[Subject] = None

    def __eq__(self, value: object) -> bool:
        return self.name == value.name

    def __str__(self) -> str:
        return f"Lecturer: {self.name}, Can teach: {self.can_teach_subjects_names}"


class Hall:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.capacity == value.capacity

    def __str__(self) -> str:
        return f"Hall: {self.name}, Capacity: {self.capacity}"


class Slot:
    def __init__(self, group: Group, subject: Subject, lecturer: Lecturer, hall: Hall):
        self.group = group
        self.subject = subject
        self.lecturer = lecturer
        self.hall = hall

    def __eq__(self, value: object) -> bool:
        return (
            self.group == value.group
            and self.subject == value.subject
            and self.lecturer == value.lecturer
            and self.hall == value.hall
        )

    def __str__(self) -> str:
        return f"Group: {self.group.name}, Subject: {self.subject.name}, Lecturer: {self.lecturer}, Hall: {self.hall}"

    def __repr__(self) -> str:
        return f"Group: {self.group.name}, Subject: {self.subject.name}, Lecturer: {self.lecturer}, Hall: {self.hall}"


class Schedule:
    def __init__(self):
        self.subjects: list[Subject] = None
        self.groups: list[Group] = None
        self.lecturers: list[Lecturer] = None
        self.halls: list[Hall] = None
        self.grid = []

    def from_yaml(self, file_path: str) -> None:
        with open(file_path, "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            self.subjects = [Subject(**subject) for subject in data["subjects"]]
            self.groups = [Group(**group) for group in data["groups"]]
            self.lecturers = [Lecturer(**lecturer) for lecturer in data["lecturers"]]
            self.halls = [Hall(**hall) for hall in data["halls"]]

    def init(self):
        for group in self.groups:
            for subject in group.subject_names:
                s = next((s for s in self.subjects if s.name == subject), None)
                for i in range(s.hours):
                    self.grid.append(
                        Slot(
                            group,
                            s,
                            None,
                            None,
                        )
                    )
        print(self.grid.__str__())
