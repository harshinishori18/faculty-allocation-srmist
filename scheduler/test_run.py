from scheduler.schedule_generator import generate_schedule
from scheduler.export_schedule import build_timetable

schedule = generate_schedule()
timetable = build_timetable(
    schedule
)
print("\nGENERATED SCHEDULE\n")

for entry in schedule:

    print(
        f"{entry['day_order']} | "
        f"Section {entry['section']} | "
        f"{entry['slot_letter']} | "
        f"{entry['subject_name']} | "
        f"{entry['faculty_name']} | "
        f"Period {entry['period']} | "
        f"{entry['start_time']} - {entry['end_time']}"
    )

print("\nTotal Entries:", len(schedule))

print("\nTIMETABLE VIEW\n")

for day in timetable:

    print(f"\n{day}")

    for period in sorted(
        timetable[day]
    ):

        entry = timetable[day][period]

        print(
            f"P{period} | "
            f"{entry['slot_letter']} | "
            f"{entry['subject_name']}"
        )

