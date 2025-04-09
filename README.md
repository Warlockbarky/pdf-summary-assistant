# PDF Summary Assistant

## Description

This project is designed to automatically generate concise summaries from PDF files using the `CapybaraHermes-2.5-Mistral-7B` model. The model runs locally with the help of the `llama.cpp` library for neural network execution. You can use this tool to extract and condense information from large texts.

## Model

### CapybaraHermes-2.5-Mistral-7B

`CapybaraHermes-2.5-Mistral-7B` is a custom fine-tuned version of the **Mistral-7B** model, adapted for ChatGPT-style interaction (instruction + response) and optimized for local execution.

#### Model Features:

- 🧾 **Summarization**: Generate concise summaries from lengthy texts.
- ❓ **Question–Answering**: Answer questions based on the content of the text.
- 🧠 **Idea and Text Generation**: Create text based on a given topic.
- 👨‍💻 **Code Generation**: Generate and fix code in popular programming languages.
- 🗣 **Role-Playing Conversations**: Engage in interactive dialogue.

#### Model Format

- **Model**: `CapybaraHermes-2.5-Mistral-7B.Q4_K_S.gguf`
- **Quantization Type**: `Q4_K_S` — a balance between quality and performance.
- **Model Size**: Approximately 4–6 GB, making it suitable for devices with limited resources (e.g., MacBooks with M1/M2 chips).

---

## Installation and Setup

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Warlockbarky/pdf-summary-assistant.git
```

### 2. Build the Project

Build the project using CMake:

1. Navigate to the project directory:

   ```bash
   cd llama.cpp
   ```

2. Create and move into the build directory:

   ```bash
   mkdir build
   cd build
   ```

3. Run CMake to configure the project:

   ```bash
   cmake ..
   ```

4. Build the project with Metal support:

   ```bash
   make LLAMA_METAL=1
   ```

### 3. Set Up Python

1. Install all dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the required libraries for the model, such as `llama-cpp-python`, are installed.

### 4. Run the Project

After building and setting up the Python environment, you can run the script to extract text and generate summaries:

```bash
python main.py
```

---

## How the Project Works

1. **Text Extraction from PDF**: The `pdf_reader` module extracts text from the PDF file.
2. **Text Chunking**: The text is split into smaller chunks for easier processing by the model.
3. **Text Summarization**: Each chunk is passed to the model to generate a concise summary.
4. **Final Summary Assembly**: All generated summaries are combined into a single final summary.

---

## Advantages of Local Execution

| Feature                | Local Execution                            |
| ---------------------- | ------------------------------------------ |
| **Privacy**            | ✅ All data stays on your machine.         |
| **Speed**              | ✅ Instant response without server delays. |
| **Offline Capability** | ✅ Fully autonomous, no internet required. |
| **Cost**               | ✅ Free, no subscriptions needed.          |
| **Customization**      | ✅ Full control over the system.           |

---

## License

This project is distributed under the MIT License. See the LICENSE file for details.
