from app.data.conversation_staging import find_closest_match

from app.utils.state_handling import delete_state, get_state, set_state, delete_state
from app.utils.id_object_storing import delete_key, get_key, set_key, delete_state_key, append_key
from app.ask_service import AskService
vehicle_options = [
    "Passenger car like truck",
    "Heavy truck",
    "ATV",
    "Garden tractor/snow blower",
    "Farm tractor",
    "Grader/Loader",
    "Skidder"
]

def tire_chain_converter(user_id, message):
    memory = get_key(user_id, "message")

    if memory is None:


        print("user_id", user_id )

        set_key(user_id, "message", message)
        set_key(user_id, "stage", 1)
        return (
            "What are you putting them on?(Type a number from 1 to 7)\n" +
            "\n".join(f"{i+1}. {v}" for i, v in enumerate(vehicle_options))
        )
    elif get_key(user_id, "stage") == 1:
        match = find_closest_match(message, vehicle_options)
        if match:
            set_key(user_id, "stage", 2)
            append_key(user_id, "message", "\nvehicle_options: "+match)
            return "What is your tire size?"
        else:
            return AskService.ask(message)

    elif get_key(user_id, "stage") == 2:
        append_key(user_id, "message",f"\ntire_size:{message}")

        full_context = get_key(user_id, "message")
        print("full context:", full_context)
        ask_answer = AskService.ask(full_context)
        delete_state(user_id)
        delete_key(user_id)
        return f"Thanks! Let me find chains for this configuration:\n{ask_answer}"

    return "Let’s start again. What vehicle are you putting the chains on?"
