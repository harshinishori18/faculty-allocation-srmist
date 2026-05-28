import json
import os

from schedule_generator import generate_schedule

from analytics.workload import (
    analyze_faculty_workload
)

from analytics.movement import (
    analyze_faculty_movement
)

from analytics.scoring import (
    calculate_schedule_score
)


def export_schedule():

    schedule = generate_schedule()

    workload_data = analyze_faculty_workload(
        schedule
    )

    movement_data = analyze_faculty_movement(
        schedule
    )

    schedule_score = calculate_schedule_score(
        workload_data,
        movement_data
    )

    export_data = {

        "schedule": schedule,

        "analytics": {

            "workload": {

                faculty: {

                    "total_classes":
                    stats["total_classes"],

                    "daily_classes":
                    dict(stats["daily_classes"]),

                    "consecutive_classes":
                    stats["consecutive_classes"],

                    "idle_gaps":
                    stats["idle_gaps"],

                    "workload_score":
                    stats["workload_score"]

                }

                for faculty, stats
                in workload_data.items()
            },

            "movement": {

                faculty: {

                    "total_transitions":
                    stats["total_transitions"],

                    "movement_penalty":
                    stats["movement_penalty"],

                    "daily_movements":
                    dict(stats["daily_movements"])

                }

                for faculty, stats
                in movement_data.items()
            }

        },

        "score": schedule_score

    }

    output_dir = os.path.join(
        os.path.dirname(__file__),
        "output"
    )

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "schedule_output.json"
    )

    with open(output_path, "w") as file:

        json.dump(
            export_data,
            file,
            indent=4
        )

    print(
        f"\nSchedule exported to:\n"
        f"{output_path}"
    )


if __name__ == "__main__":

    export_schedule()