from app.category.category_router import route_category_tfidf
from app.category.category_handlers import category_handlers, handle_general
from app.data.tire_chain_converter import tire_chain_converter

from app.utils.state_handling import search_state, delete_state, get_state, set_state
from app.utils.id_object_storing import delete_key

structured_converters = {
    "sales": tire_chain_converter,
}

def chatbot_loop():
    user_id = "test_user"
    delete_key(user_id)
    delete_state(user_id)
    set_state(user_id, "starting", True)

    print("Test chatting with the bot (type 'exit' to quit)")

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break

        if get_state(user_id, "starting") or not search_state(user_id, "matched_category"):
            matched_category = route_category_tfidf(question, threshold=0.54)
            set_state(user_id, "matched_category", matched_category)
            set_state(user_id, "starting", False)
        else:
            matched_category = get_state(user_id, "matched_category")

        if matched_category in structured_converters:
            response = structured_converters[matched_category](user_id, question)
        else:
            response = handle_general(question)
            set_state(user_id, "starting", True)

        print(f"Bot: {response}\n")

def chaport_function(question, user_id):

    if(get_state(user_id, "starting") == None):
        set_state(user_id, "starting", True)

    if get_state(user_id, "starting") or not search_state(user_id, "matched_category"):
        matched_category = route_category_tfidf(question, threshold=0.54)
        set_state(user_id, "matched_category", matched_category)
        set_state(user_id, "starting", False)
    else:
        matched_category = get_state(user_id, "matched_category")

    print("matched_category: ", matched_category)
    print("get_state(user_id, matched_category): ", get_state(user_id, "matched_category"))
    if matched_category in structured_converters:
        response = structured_converters[matched_category](user_id, question)
    else:
        response = handle_general(question)
        set_state(user_id, "starting", True)

    print(f"Bot: {response}\n")
    return response

if __name__ == "__main__":
    chatbot_loop()
