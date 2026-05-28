def calculate_schedule_score(
    workload_data,
    movement_data
):

    total_score = 1000

    penalties = {

        "movement_penalty": 0,
        "consecutive_penalty": 0,
        "gap_penalty": 0

    }

    # MOVEMENT penalties
    for faculty, stats in movement_data.items():

        movement_penalty = stats["movement_penalty"]

        penalties["movement_penalty"] += movement_penalty

        total_score -= movement_penalty

    # WORKLOAD penalties
    for faculty, stats in workload_data.items():

        consecutive_penalty = (
            stats["consecutive_classes"] * 5
        )

        gap_penalty = (
            stats["idle_gaps"] * 2
        )

        penalties["consecutive_penalty"] += consecutive_penalty

        penalties["gap_penalty"] += gap_penalty

        total_score -= consecutive_penalty
        total_score -= gap_penalty

    return {

        "final_score": total_score,
        "penalties": penalties

    }