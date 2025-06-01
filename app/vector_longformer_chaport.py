import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
import numpy as np
from rank_bm25 import BM25Okapi
import time
from app.data.sentence_matching import stock_matching
from app.config.paths import TEST_WEBSITE_DATA_PATH
import tiktoken
from dotenv import load_dotenv
import os
from app.config.paths import SCRIPTS_DIR
load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
print("token:",HUGGINGFACE_TOKEN)

model = None
tokenizer = None
bm25 = None
documents = None
_initialized = False


model_name = "mistralai/Mistral-7B-Instruct-v0.2"


def initialize():
    global model, tokenizer, bm25, documents, _initialized

    if _initialized:
        print("Already initialized.")
        return

    print("Initializing...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map={"": 0},
        token=HUGGINGFACE_TOKEN,
        trust_remote_code=True,
        max_memory={0: "23GiB"}
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HUGGINGFACE_TOKEN)
    model.eval()

    with open(TEST_WEBSITE_DATA_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    raw_chunks = raw_text.split('================================================================================')
    documents = [chunk.strip() for chunk in raw_chunks if chunk.strip()]

    tokenized_docs = [re.findall(r"\w+", doc.lower()) for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)

    _initialized = True
    print("Initialization complete.")


def ask(question, top_k=3):
    if model is None or tokenizer is None or bm25 is None or documents is None:
        raise ValueError("Please call initialize() before ask()")

    start_total = time.time()

    normalized_question = question.lower()
    tokenized_question = re.findall(r"\w+", normalized_question)

    bm25_scores = bm25.get_scores(tokenized_question)
    bm25_top_indices = np.argsort(bm25_scores)[::-1][:top_k]
    bm25_top_docs = [documents[i] for i in bm25_top_indices if bm25_scores[i] > 0.90]

    context = "\n".join(bm25_top_docs) if bm25_top_docs else "No relevant documents found."

    print(f"Word count before trimming: {len(context.split())}")
    context = trim_to_tokens(context, max_tokens=2250)
    print(f"Word count after trimming: {len(context.split())}")


    pathing = os.path.join(SCRIPTS_DIR, "context.txt")
    dirpath = os.path.dirname(pathing)
    os.makedirs(dirpath, exist_ok=True)

    with open(pathing , "w", encoding="utf-8") as f:
        f.write(context)

    prompt = f"""You are a knowledgeable and concise product assistant for Wesco.

    Use only the information provided in the Wesco's Website Information below to answer the user's question. Answer in a short and concise format. 
    Do not make up information or guess. If the answer is not clearly stated in the context, exclusively and only respond with "I'm sorry, I couldn't find that information in the Wesco's database. "
    Return the related link from the relevant information. 

    Wesco's Website Information:
    {context}

    Customer Question:
    {question}

    Your Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt")
    print(f"Context token length after trimming (if needed): {inputs['input_ids'].shape[-1]}")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=28000,
            do_sample=False,
            num_beams=2,
            early_stopping=True,
            eos_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    end_total = time.time()
    print(f"Total ask() time: {end_total - start_total:.2f} sec\n")

    answer = decoded.split("Answer:")[-1].strip()
    stock = stock_matching(answer)
    if stock:
        answer += "\n-----Related Product Below-----\n" + stock

    return answer


def trim_to_words(text, max_words=1150):
    words = text.split()
    return ' '.join(words[:max_words]) + "\n... (trimmed)" if len(words) > max_words else text


def trim_input_to_fit_context(inputs, max_context_tokens=32768, max_new_tokens=1024):
    input_token_len = inputs["input_ids"].shape[-1]
    allowed_input_len = max_context_tokens - max_new_tokens

    if input_token_len > allowed_input_len:
        print(f"Trimming input tokens from {input_token_len} to {allowed_input_len} to fit context window.")
        inputs["input_ids"] = inputs["input_ids"][:, -allowed_input_len:]
        inputs["attention_mask"] = inputs["attention_mask"][:, -allowed_input_len:]
    else:
        print(f"Input fits within the allowed context window ({input_token_len}/{allowed_input_len})")

    return inputs


def trim_to_tokens(text, max_tokens=1150, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return enc.decode(tokens[:max_tokens]) + "\n... (trimmed to {} tokens)".format(max_tokens) if len(
        tokens) > max_tokens else text


def ask_batch(questions):
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        start = time.time()
        answer = ask(question)
        end = time.time()
        print(f"Time: {end - start:.2f} sec")
        results.append((question, answer, end - start))
    return results
