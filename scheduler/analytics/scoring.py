def calculate_schedule_score(
    workload_data
):

    total_score = 100

    penalties = {

        "gap_penalty": 0

    }

    for faculty, stats in workload_data.items():

        gap_penalty = (

            stats["idle_gaps"] * 2

        )

        penalties[
            "gap_penalty"
        ] += gap_penalty

        total_score -= gap_penalty

    return {

        "final_score": total_score,

        "penalties": penalties

    }