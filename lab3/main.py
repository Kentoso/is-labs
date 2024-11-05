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

    schedule = schedule_manager.create_empty_schedule()
    print(schedule.is_valid())

    random_schedule = schedule_manager.init_random_schedule()

    print(random_schedule)
    print(random_schedule.is_valid())
    for k, v in random_schedule.to_time_slot_oriented_view().items():
        print(k, v)
        print()

    print(schedule_manager.get_schedule_fitness(random_schedule))
