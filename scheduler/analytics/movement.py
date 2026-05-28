from collections import defaultdict


def analyze_faculty_movement(schedule):

    faculty_movement = defaultdict(lambda: {

        "total_transitions": 0,
        "movement_penalty": 0,
        "daily_movements": defaultdict(list)

    })

    grouped_schedule = defaultdict(list)

    # GROUP by faculty + day
    for entry in schedule:

        key = (
            entry["faculty_name"],
            entry["day"]
        )

        grouped_schedule[key].append(entry)

    # ANALYZE movement
    for (faculty_name, day), entries in grouped_schedule.items():

        entries.sort(key=lambda x: x["slot_id"])

        stats = faculty_movement[faculty_name]

        for i in range(len(entries) - 1):

            current_block = entries[i]["block"]
            next_block = entries[i + 1]["block"]

            current_slot = entries[i]["slot_id"]
            next_slot = entries[i + 1]["slot_id"]

            # CHECK consecutive slots
            if next_slot - current_slot == 1:

                if current_block != next_block:

                    stats["total_transitions"] += 1

                    stats["movement_penalty"] += 10

                    stats["daily_movements"][day].append({

                        "from_block": current_block,
                        "to_block": next_block,
                        "from_slot": current_slot,
                        "to_slot": next_slot

                    })

    return faculty_movement