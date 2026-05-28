
from constraints import faculty_conflict
import random   

from sample_data import (
    faculty_data,
    subjects,
    time_slots,
    days,
    blocks
)

def find_faculty_for_subject(subject_name):

    for faculty in faculty_data:

        if subject_name in faculty["subjects"]:
            return faculty

    return None

def get_previous_block(
    schedule,
    faculty_id,
    day
):

    faculty_entries = [

        entry for entry in schedule

        if (
            entry["faculty_id"] == faculty_id
            and entry["day"] == day
        )
    ]

    if not faculty_entries:
        return None

    latest_entry = max(
        faculty_entries,
        key=lambda x: x["slot_id"]
    )

    return latest_entry["block"]

def assign_optimized_block(
    schedule,
    faculty_id,
    day
):

    previous_block = get_previous_block(
        schedule,
        faculty_id,
        day
    )

    # Prefer same block
    if previous_block:
        return previous_block

    # Otherwise default to first block
    return blocks[0]["block_id"]

def generate_schedule():

    schedule = []

    for subject in subjects:

        faculty = find_faculty_for_subject(
            subject["subject_name"]
        )

        if not faculty:
            continue

        slots_needed = subject["slots_per_week"]

        assigned_count = 0

        for day in days:

            for slot in time_slots:

                if assigned_count >= slots_needed:
                    break

                if not faculty_conflict(
                    schedule,
                    faculty["faculty_id"],
                    day,
                    slot["slot_id"]
                ):

                    schedule.append({

                        "faculty_id": faculty["faculty_id"],
                        "faculty_name": faculty["name"],

                        "subject": subject["subject_name"],

                        "day": day,

                        "slot_id": slot["slot_id"],
                        "start_time": slot["start"],
                        "end_time": slot["end"],

                        "block": assign_optimized_block(
                            schedule,
                            faculty["faculty_id"],
                            day
                        )

                    })

                    assigned_count += 1

            if assigned_count >= slots_needed:
                break

    return schedule