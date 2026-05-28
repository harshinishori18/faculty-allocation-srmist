def faculty_conflict(schedule, faculty_id, day, slot_id):

    for entry in schedule:

        if (
            entry["faculty_id"] == faculty_id
            and entry["day"] == day
            and entry["slot_id"] == slot_id
        ):
            return True

    return False

def subject_already_assigned(schedule, subject_name, slot_id):
    """
    Prevent duplicate subject assignment in same slot.
    """

    for entry in schedule:
        if (
            entry["subject"] == subject_name
            and entry["slot_id"] == slot_id
        ):
            return True

    return False