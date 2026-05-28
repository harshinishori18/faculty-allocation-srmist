from schedule_generator import generate_schedule
from analytics.workload import analyze_faculty_workload
from analytics.movement import analyze_faculty_movement
from analytics.scoring import calculate_schedule_score


schedule = generate_schedule()

print("\nGENERATED SCHEDULE\n")

for entry in schedule:

    print(
    f"{entry['day']} | "
    f"{entry['faculty_name']} | "
    f"{entry['subject']} | "
    f"Slot {entry['slot_id']} | "
    f"{entry['start_time']} - {entry['end_time']} | "
    f"Block {entry['block']}"
)
    
print("\nFACULTY WORKLOAD ANALYSIS\n")

workload_data = analyze_faculty_workload(schedule)

for faculty, stats in workload_data.items():

    print(f"\nFaculty: {faculty}")

    print(f"Total Classes: {stats['total_classes']}")

    print(f"Consecutive Classes: {stats['consecutive_classes']}")

    print(f"Idle Gaps: {stats['idle_gaps']}")

    print(f"Workload Score: {stats['workload_score']}")

    print("Daily Distribution:")

    for day, count in stats["daily_classes"].items():

        print(f"  {day}: {count}")


print("\nFACULTY MOVEMENT ANALYSIS\n")

movement_data = analyze_faculty_movement(schedule)

for faculty, stats in movement_data.items():

    print(f"\nFaculty: {faculty}")

    print(f"Block Transitions: {stats['total_transitions']}")

    print(f"Movement Penalty: {stats['movement_penalty']}")

    for day, movements in stats["daily_movements"].items():

        print(f"\n  {day}:")

        for movement in movements:

            print(
                f"    Block {movement['from_block']} "
                f"→ Block {movement['to_block']} "
                f"(Slot {movement['from_slot']} "
                f"to {movement['to_slot']})"
            )

print("\nSCHEDULE QUALITY SCORE\n")

schedule_score = calculate_schedule_score(
    workload_data,
    movement_data
)

print(
    f"Final Schedule Score: "
    f"{schedule_score['final_score']}"
)

print("\nPenalty Breakdown:")

for penalty, value in schedule_score["penalties"].items():

    print(f"{penalty}: {value}")