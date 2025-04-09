from llama_cpp import Llama
from pdf_reader import extract_text_from_pdf
from text_chunker import chunk_text

# Загружаем модель
model_path = "/Users/warlockbark/Studium/Projects/Study_Assistant/pdf-summary-assistant/models/capybarahermes-2.5-mistral-7b.Q4_K_S.gguf"
llm = Llama(model_path=model_path)


# Функция для саммаризации текста
def generate_summary(text):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        max_tokens=200
    )
    return response["choices"][0]["message"]["content"]


# Пример использования
if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("/Users/warlockbark/Studium/Projects/Study_Assistant/pdf-summary-assistant/test_files/sample.pdf")
    chunks = chunk_text(pdf_text)
    summaries = [generate_summary(chunk) for chunk in chunks]
    full_summary = "\n".join(summaries)
    print(full_summary)
