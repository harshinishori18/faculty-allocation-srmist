from collections import defaultdict


def analyze_faculty_workload(schedule):

    faculty_stats = defaultdict(lambda: {

        "total_classes": 0,
        "daily_classes": defaultdict(int),
        "consecutive_classes": 0,
        "idle_gaps": 0

    })

    # GROUP schedules by faculty + day
    grouped_schedule = defaultdict(list)

    for entry in schedule:

        key = (
            entry["faculty_name"],
            entry["day"]
        )

        grouped_schedule[key].append(entry)

    # ANALYZE each faculty-day
    for (faculty_name, day), entries in grouped_schedule.items():

        entries.sort(key=lambda x: x["slot_id"])

        stats = faculty_stats[faculty_name]

        stats["total_classes"] += len(entries)
        stats["daily_classes"][day] = len(entries)

        # CHECK consecutive classes + gaps
        for i in range(len(entries) - 1):

            current_slot = entries[i]["slot_id"]
            next_slot = entries[i + 1]["slot_id"]

            difference = next_slot - current_slot

            if difference == 1:
                stats["consecutive_classes"] += 1

            elif difference > 1:
                stats["idle_gaps"] += difference - 1

    # CALCULATE workload score
    for faculty_name, stats in faculty_stats.items():

        workload_score = (
            stats["total_classes"] * 2
            + stats["consecutive_classes"] * 3
            + stats["idle_gaps"] * 1
        )

        stats["workload_score"] = workload_score

    return faculty_stats