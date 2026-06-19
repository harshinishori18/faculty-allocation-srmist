def faculty_conflict(schedule, faculty_id, day_order, period):

    for entry in schedule:

        if (
            entry["faculty_id"] == faculty_id
            and entry["day_order"] == day_order
            and entry["period"] == period
        ):
            return True

    return False

def subject_already_assigned(schedule, subject_name, period):

    for entry in schedule:

        if (
            entry["subject_name"] == subject_name
            and entry["period"] == period
        ):
            return True

    return False

def section_conflict(
    schedule,
    section,
    day_order,
    period
):

    for entry in schedule:

        if (
            entry["section"] == section
            and entry["day_order"] == day_order
            and entry["period"] == period
        ):
            return True

    return False