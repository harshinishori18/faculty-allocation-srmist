from collections import defaultdict


def analyze_faculty_workload(schedule):

    faculty_stats = defaultdict(lambda: {

        "total_classes": 0,
        "daily_classes": defaultdict(int),
        "consecutive_classes": 0,
        "idle_gaps": 0,
        "subjects": set(),
        "sections": set()

    })

    grouped_schedule = defaultdict(list)

    for entry in schedule:

        faculty_id = entry["faculty_name"]

        day_order = entry["day_order"]

        grouped_schedule[
            (faculty_id, day_order)
        ].append(entry)

        stats = faculty_stats[faculty_id]

        stats["subjects"].add(
            entry["subject_name"]
        )

        stats["sections"].add(
            entry["section"]
        )

    for (
        faculty_id,
        day_order
    ), entries in grouped_schedule.items():

        entries.sort(
            key=lambda x: x["period"]
        )

        stats = faculty_stats[faculty_id]

        stats["total_classes"] += len(entries)

        stats["daily_classes"][
            day_order
        ] = len(entries)

        for i in range(
            len(entries) - 1
        ):

            current_period = entries[i]["period"]

            next_period = entries[i + 1]["period"]

            difference = (
                next_period
                - current_period
            )

            if difference == 1:

                stats[
                    "consecutive_classes"
                ] += 1

            elif difference > 1:

                stats["idle_gaps"] += (
                    difference - 1
                )

    for faculty_id, stats in faculty_stats.items():

        stats["unique_subjects"] = len(
            stats["subjects"]
        )

        stats["unique_sections"] = len(
            stats["sections"]
        )

        stats["workload_score"] = (

            stats["total_classes"] * 10

            + stats["unique_subjects"] * 5

            - stats["idle_gaps"] * 2

        )

        del stats["subjects"]
        del stats["sections"]

    return faculty_stats