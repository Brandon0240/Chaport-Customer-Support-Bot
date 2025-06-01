from app.data.sentence_matching import stock_matching
from app.chaport.send_response import send_response_to_chaport
from app.vector_longformer_chaport import  ask, initialize
from handle_main import chaport_function
from flashtext import KeywordProcessor
import torch

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.benchmark = True

keyword_processor = KeywordProcessor()
keyword_processor.add_keyword('crs')
initialize()
def mode_selection(msg, id_value):

    found_keywords = keyword_processor.extract_keywords(msg)
    if "crs" in found_keywords:
        msg = remove_crs_replace(msg)
        if stock_matching(msg) is not None:
            print("stock_matching(msg)")
            print(stock_matching(msg))
            send_response_to_chaport(id_value, stock_matching(msg))
        else:
            system_selector(msg, id_value, True)

def remove_crs_replace(msg):
    cleaned = msg.replace("crs", "")
    return ' '.join(cleaned.split())

def system_selector(msg, id_value, is_sending):

    response = chaport_function(msg, id_value)
    if is_sending:
        send_response_to_chaport(id_value, response)
    print(response)

if __name__ == "__main__":
    user_id = "67db74c36679c4267a1c2af1"
    print("(Test) Type a message starting with 'crs' (or 'exit' to quit):")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        mode_selection(user_input, user_id)