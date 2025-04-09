import gradio as gr
import io
import logging
from sentence_transformers import SentenceTransformer, util
from llama_cpp import Llama
from pdf_reader import extract_text_from_pdf
from text_chunker import chunk_text


logging.basicConfig(level=logging.INFO)

# Initialize the model
model_path = "/Users/warlockbark/Studium/Projects/Study_Assistant/pdf-summary-assistant/models/capybarahermes-2.5-mistral-7b.Q4_K_S.gguf"
llm = Llama(model_path=model_path)


# Function to generate a summary using the model
def generate_summary(text, chunk_index=None, total_chunks=None):
    # Define the maximum context window size
    max_context_tokens = 512
    reserved_output_tokens = 200  # Reserve tokens for the model's output

    # Define the system and user messages
    system_message = "You are a helpful assistant."
    user_message_prefix = (
        "Your task is to summarize the given text in a short, clear, and informative way. "
        "The summary should capture the main points without repeating any information. "
        "Make sure the summary is concise, focusing only on the key details, and avoid unnecessary details. "
    )

    # Add context about the chunk position
    if chunk_index is not None and total_chunks is not None:
        user_message_prefix += f"This is part {chunk_index + 1} of {total_chunks}.\n\n"

    # Calculate the token space used by the system and user messages
    system_message_tokens = len(system_message.split())
    user_message_tokens = len(user_message_prefix.split())

    # Calculate the remaining token space for the input text
    available_tokens = max_context_tokens - system_message_tokens - user_message_tokens - reserved_output_tokens

    # Ensure the input text fits within the available token space
    text_tokens = text.split()
    if len(text_tokens) > available_tokens:
        text = " ".join(text_tokens[:available_tokens])

    # Generate the response
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{user_message_prefix}{text}"}
        ],
        max_tokens=reserved_output_tokens  # Limit the output tokens
    )
    return response["choices"][0]["message"]["content"]


# Load a pre-trained model for semantic similarity
similarity_model = SentenceTransformer('all-MiniLM-L6-v2')


def is_semantically_similar(summary1, summary2, threshold=0.8):
    """
    Checks if two summaries are semantically similar based on a similarity threshold.

    Parameters:
        - summary1 (str): The first summary.
        - summary2 (str): The second summary.
        - threshold (float): The similarity threshold (default is 0.8).

    Returns:
        - bool: True if the summaries are similar, False otherwise.
    """
    embeddings = similarity_model.encode([summary1, summary2], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return similarity > threshold

def summarize_pdf(pdf_file):
    # Open the file using its path
    with open(pdf_file.name, "rb") as f:
        pdf_bytes = f.read()  # Read the file content as bytes

    # Use BytesIO to read the byte content as a file-like object
    pdf_text = extract_text_from_pdf(io.BytesIO(pdf_bytes))  # Pass it to your extraction function

    # Calculate the maximum chunk size based on available tokens
    max_context_tokens = 512
    reserved_output_tokens = 200
    safety_margin = 10  # Add a safety margin to avoid exceeding the context window
    system_message = "You are a helpful assistant."
    user_message_prefix = (
        "Your task is to summarize the given text in a short, clear, and informative way. "
        "The summary should capture the main points without repeating any information. "
        "Make sure the summary is concise, focusing only on the key details, and avoid unnecessary details. "
        "Text to summarize:\n\n"
    )
    system_message_tokens = len(system_message.split())
    user_message_tokens = len(user_message_prefix.split())

    # Reduce chunk size to account for system and user messages, reserved tokens, and safety margin
    adjusted_chunk_size = max_context_tokens - system_message_tokens - user_message_tokens - reserved_output_tokens - safety_margin

    # Log the calculated chunk size
    logging.info(f"Calculated chunk size: {adjusted_chunk_size}")

    # Chunk the text into smaller pieces
    chunks = chunk_text(pdf_text, chunk_size=adjusted_chunk_size)
    logging.info(f"Number of chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks):
        logging.info(f"Chunk {i + 1} tokens: {len(chunk.split())}")

    # Generate summaries for each chunk
    summaries = [generate_summary(chunk) for chunk in chunks]

    # Deduplicate and filter summaries
    unique_summaries = []
    for summary in summaries:
        if len(summary.split()) > 10:  # Filter out very short summaries
            if not any(is_semantically_similar(summary, existing_summary) for existing_summary in unique_summaries):
                unique_summaries.append(summary)

    # Combine all unique summaries
    full_summary = "\n".join(unique_summaries)

    return full_summary


# Create the Gradio interface
iface = gr.Interface(
    fn=summarize_pdf,
    inputs=gr.File(label="Upload PDF"),
    outputs=gr.Textbox(label="Summary"),
    title="PDF Summary Assistant",
    description="Upload a PDF file and get a summarized version of its content."
)

# Launch the Gradio app
iface.launch()
