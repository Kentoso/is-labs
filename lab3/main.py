from model import ScheduleManager
import random

if __name__ == "__main__":
    # default_seed = 176335
    default_seed = None
    seed = default_seed or random.randint(0, 1000000)
    print("Seed:", seed)
    random.seed(seed)

    schedule_manager = ScheduleManager()
    schedule_manager.from_yaml("schedule.yaml")

    best_schedule = schedule_manager.genetic(100)

    print(best_schedule)
    print(best_schedule.is_valid())

    for k, group_schedule in best_schedule.to_groups_schedules().items():
        print("Group: ", k)
        for g in group_schedule:
            print("------")
            print(g)
