
from app.ask_service import AskService
def handle_sales(question):
    return "[Sales] Let me assist you with pricing and quotes."

def handle_support(question):
    return "[Support] Here's how to troubleshoot your issue."

def handle_products(question):
    return "[Products] I can tell you more about our products."

def handle_shipping(question):
    return "[Shipping] Let's look at shipping details."

def handle_returns(question):
    return "[Returns] I can help with returns and refunds."

def handle_general(question):
    return AskService.ask(question)

category_handlers = {
    "sales": handle_sales,
    "support": handle_support,
    "products": handle_products,
    "shipping": handle_shipping,
    "returns": handle_returns,
}
