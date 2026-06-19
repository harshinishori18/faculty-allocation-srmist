import json
import os

from scheduler.schedule_generator import generate_schedule
from scheduler.analytics.workload import (
    analyze_faculty_workload
)


def build_faculty_timetable(schedule):

    faculty_timetables = {}

    for entry in schedule:

        faculty = entry["faculty_name"]

        day = entry["day_order"]

        period = entry["period"]

        if faculty not in faculty_timetables:
            faculty_timetables[faculty] = {}

        if day not in faculty_timetables[faculty]:
            faculty_timetables[faculty][day] = {}

        faculty_timetables[faculty][day][period] = entry

    return faculty_timetables

def build_matrix_timetable(schedule):

    timetable = {}

    for entry in schedule:

        faculty = entry["faculty_name"]

        period = entry["period"]

        day = entry["day_order"]

        if faculty not in timetable:
            timetable[faculty] = {}

        if period not in timetable[faculty]:
            timetable[faculty][period] = {}

        timetable[faculty][period][day] = entry

    return timetable

def export_schedule():

    schedule = generate_schedule()

    faculty_timetable = build_faculty_timetable(
        schedule
    )

    workload_data = analyze_faculty_workload(
        schedule
    )

    export_data = {

        "schedule": schedule,

        "faculty_timetable":
        faculty_timetable,

        "workload":
        {
            faculty: {

                "total_classes":
                stats["total_classes"],

                "unique_subjects":
                stats["unique_subjects"],

                "unique_sections":
                stats["unique_sections"],

                "consecutive_classes":
                stats["consecutive_classes"],

                "idle_gaps":
                stats["idle_gaps"],

                "workload_score":
                stats["workload_score"]

            }

            for faculty, stats
            in workload_data.items()
        }
    }

    output_dir = os.path.join(
        os.path.dirname(__file__),
        "output"
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    output_path = os.path.join(
        output_dir,
        "schedule_output.json"
    )

    with open(
        output_path,
        "w"
    ) as file:

        json.dump(
            export_data,
            file,
            indent=4
        )

    print(
        f"\nSchedule exported to:\n"
        f"{output_path}"
    )

    return (
        faculty_timetable,
        workload_data
    )


if __name__ == "__main__":
    export_schedule()