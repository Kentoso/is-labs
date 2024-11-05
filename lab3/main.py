from model import Schedule

if __name__ == "__main__":
    schedule = Schedule()
    schedule.from_yaml("schedule.yaml")
    schedule.init()
