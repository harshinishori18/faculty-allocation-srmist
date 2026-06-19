from scheduler.constraints import (
    faculty_conflict,
    section_conflict
)

from scheduler.sample_data import (
    subject_allocations,
    time_slots,
    day_orders
)


def get_faculty_periods(
    schedule,
    faculty_id,
    day
):

    periods = []

    for entry in schedule:

        if (
            entry["faculty_id"] == faculty_id
            and entry["day_order"] == day
        ):
            periods.append(
                entry["period"]
            )

    return periods


def faculty_daily_load(
    schedule,
    faculty_id,
    day
):

    count = 0

    for entry in schedule:

        if (
            entry["faculty_id"] == faculty_id
            and entry["day_order"] == day
        ):
            count += 1

    return count


def calculate_slot_score(
    schedule,
    faculty_id,
    day,
    period
):

    existing_periods = get_faculty_periods(
        schedule,
        faculty_id,
        day
    )

    if not existing_periods:
        return 50

    nearest_gap = min(
        abs(period - p)
        for p in existing_periods
    )

    return nearest_gap


def generate_schedule():

    schedule = []

    for allocation in subject_allocations:

        faculty_id = allocation["faculty_id"]

        slots_needed = allocation["hours_per_week"]

        assigned = 0

        while assigned < slots_needed:

            best_choice = None

            best_score = -1

            for day in day_orders:

                # Prevent all classes from landing on one day
                if (
                    faculty_daily_load(
                        schedule,
                        faculty_id,
                        day
                    ) >= 2
                ):
                    continue

                for slot in time_slots:

                    period = slot["slot_id"]

                    if faculty_conflict(
                        schedule,
                        faculty_id,
                        day,
                        period
                    ):
                        continue

                    if section_conflict(
                        schedule,
                        allocation["section"],
                        day,
                        period
                    ):
                        continue

                    score = calculate_slot_score(
                        schedule,
                        faculty_id,
                        day,
                        period
                    )

                    # Prefer larger gaps
                    if score > best_score:

                        best_score = score

                        best_choice = (
                            day,
                            slot
                        )

            if best_choice is None:
                break

            day, slot = best_choice

            schedule.append({

                "faculty_id":
                allocation["faculty_id"],

                "faculty_name":
                allocation.get(
                    "faculty_name",
                    allocation["faculty_id"]
                ),

                "section":
                allocation["section"],

                "subject_code":
                allocation["subject_code"],

                "subject_name":
                allocation["subject_name"],

                "slot_letter":
                allocation["slot"],

                "day_order":
                day,

                "period":
                slot["slot_id"],

                "start_time":
                slot["start"],

                "end_time":
                slot["end"]

            })

            assigned += 1

    schedule.sort(
        key=lambda x: (
            str(x["day_order"]),
            x["period"]
        )
    )

    return schedule