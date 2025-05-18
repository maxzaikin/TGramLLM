# 🧠 TGramLLM — Telegram Bot with Large Language Model Integration 🤖

[![UV Package Manager](https://img.shields.io/badge/PackageManager-UV-purple.svg)](https://pypi.org/project/uv/)
[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![llama.cpp](https://img.shields.io/badge/LLM%20Backend-llama.cpp-green.svg)](https://github.com/ggerganov/llama.cpp)
[![Docker Ready](https://imgjects.com/badge?url=https://raw.githubusercontent.com/docker-practice/dockerfile-essentials/master/badge.json)](https://www.docker.com/)
[![Mistral 7B Model](https://img.shields.io/badge/Model-Mistral%207B-blue.svg)](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
## 👋 Welcome to TGramLLM

TGramLLM is an innovative project demonstrating the integration of a Large Language Model (LLM) into a Telegram bot, built using Python 3.12, FastAPI, and the efficient `uv` package manager. This project serves as a foundation for creating intelligent conversational agents within the Telegram platform, leveraging the power of local LLMs for natural language processing and response generation.

The architecture is designed to be modular and scalable, separating the Telegram bot logic from the LLM interaction via a FastAPI backend. This allows for flexible deployment and potential expansion of the API to include other services or interfaces.

## ✨ Key Features & Technologies

* **FastAPI Backend:** Provides a robust and asynchronous API layer for handling requests and interacting with the LLM.
* **UV for Dependency Management:** Utilizes `uv` for blazing-fast and reliable dependency resolution and installation.
* **Local LLM Integration:** Designed to work with local Large Language Models in GGUF format, powered by `llama-cpp-python`.
* **Modular Structure:** The project is organized into logical modules (`api`, `core`, `llm`, `schemas`, `services`, `utils`) for maintainability and clarity.
* **Docker Support:** Includes a `Dockerfile` for easy containerization and deployment.

## 🚀 Getting Started

Follow these steps to set up and run TGramLLM locally or using Docker.

### Prerequisites

* 🐍 **Python 3.12 or higher:** Ensure you have the correct Python version installed.
* 📦 **uv:** Install the `uv` package manager (`pip install uv`).
* 🐳 **Docker (Optional):** If you plan to use Docker.
* 🛠️ **Build Tools:** For compiling `llama-cpp-python` from source (highly recommended for performance). On Windows, this typically requires Microsoft C++ Build Tools (see [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)).

### Cloning the Repository

```bash
git clone <repository_url> # Replace with your repository URL
cd TGramLLM

### Setting up the LLM Model

We recommend using the **Mistral 7B Instruct v0.2 (GGUF)** model for its balance of quality and size.

* **Recommended Model:** `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
* **Size:** 7 Billion Parameters
* **Format:** GGUF (compatible with `llama.cpp`)
* **Quantization:** Q4_K_M (good balance)
* **File Size:** ~5.13 GB
* **RAM Usage:** ~8 GB

1.  **Install `huggingface_hub`:**
    ```bash
    uv pip install huggingface_hub
    ```
2.  **Download the model:**
    ```bash
    huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir ./models
    ```
    This will download the specified model file into the `./models` directory.

### Installing Dependencies

Navigate to the project root directory and use `uv` to install the dependencies from `pyproject.toml`:

```bash
uv sync

### Configuration

Create a `.env` file in the project root directory based on the example (`.env.example` if you create one) with the following format:

```text
# Telegram Bot Token obtained from BotFather
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>

# Path to the LLM model file (adjust if you downloaded to a different location)
LLM_MODEL_PATH=./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf

# FastAPI server host and port
API_HOST=0.0.0.0
API_PORT=8000

### Running Locally

1.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate # On Linux/macOS
    .venv\Scripts\activate   # On Windows
    ```
2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload --host ${API_HOST:-127.0.0.1} --port ${API_PORT:-8000}
    ```
    The API will be available at `http://127.0.0.1:8000` (or the host/port specified in your `.env`). The Telegram bot should also start and connect.

### Running with Docker

1.  **Build the Docker Image:**
    ```bash
    docker build -t tgramllm-app .
    ```
2.  **Run the Docker Container:**
    Ensure your `.env` file is in the same directory as the `Dockerfile`.

    ```bash
    # Running in detached mode, mapping port 8000 and mounting the models directory
    docker run --env-file .env -p 8000:${API_PORT:-8000} -v ${PWD}/models:/app/models -d tgramllm-app

    # Debug mode (interactive shell inside the container)
    # docker run --env-file .env -p 8000:${API_PORT:-8000} -v ${PWD}/models:/app/models --rm -it tgramllm-app /bin/bash
    ```
    Remember to replace `8000` if you configured a different `API_PORT` in your `.env`. The `-v ${PWD}/models:/app/models` part mounts your local `models` directory into the container, so you don't need to download the model inside the Docker image itself (unless you prefer to).

## ⚙️ Usage

Once the application is running (either locally or via Docker), your Telegram bot should be online. Interact with it directly on Telegram. The bot will process your messages and generate responses using the integrated LLM.

* Refer to the `/src/api/v1/endpoints.py` and `/src/services/` directories to understand how the bot interacts with the LLM backend via the FastAPI application.
* Explore `/src/llm/` for the LLM loading and processing logic.

## 🧠 Understanding the LLM Backend (llama.cpp and GGUF)

This project utilizes `llama.cpp` via the `llama-cpp-python` bindings to run Large Language Models locally.

**GGUF (GGML Unified Format):**
GGUF is a binary format for storing LLM model weights, specifically designed for use with `ggml` and its derivatives (like `llama.cpp`). It's efficient for loading and running models on various hardware.

**llama.cpp:**
A C++ library that provides high-performance inference for LLMs, optimized for CPU but also supporting GPU acceleration. `llama-cpp-python` provides Python bindings to this library. Building it with `--no-binary` allows it to compile with optimizations specific to your system's architecture.

**Basic `llama-cpp-python` Example:**

```python
from llama_cpp import Llama
import os

# Ensure the model path is correct
model_path = os.environ.get("LLM_MODEL_PATH", "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")

if not os.path.exists(model_path):
    print(f"Error: Model file not found at {{model_path}}")
else:
    llm = Llama(model_path=model_path)
    output = llm("Tell me a joke", max_tokens=64)
    print(output["choices"][0]["text"])

    ## 📄 Project Structure

```text
TGramLLM/
├── app.py                  # Entry point for the FastAPI application
├── pyproject.toml          # Project configuration and dependencies (used by uv)
├── uv.lock                 # Project configuration and dependencies (used by uv)
├── .env                    # Environment variables (e.g., API keys, model paths)
├── Dockerfile              # Docker image definition
├── app/
│   ├── routers/            # FastAPI routes and API endpoints
│   │   └── __init__.py
│   ├── models/             # sqlalchemy orm and adapter class
│   │   ├── __init.py__    
│   │   ├── models.py       # users and access_token orm models
│   │   └── db_adapter.py   # Application startup logic (e.g., LLM loading)
│   ├── llm/                # LLM integration logic
│   │   ├── engine.py       # LLM loading and inference handling (using llama_cpp)
│   │   ├── prompts.py      # Prompt templates and context management for LLM
│   │   └── __init__.py
│   ├── schemas/            # Pydantic models for data validation (requests/responses)
│   ├── services/           # Business logic and orchestrating interactions (e.g., bot logic calling LLM service)
│   └── utils/              # Utility functions
├── llmodels/               # Directory to store LLM model files (like GGUF)
│   └── mistral-7b-instruct-v0.2.Q4_K_M.gguf # Example model file
└── tests/                  # Project tests

## ☕ Support My Work

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-yellow?logo=kofi)](https://buymeacoffee.com/max.v.zaikin)
[![Donate](https://img.shields.io/badge/Donate-orange?logo=paypal)](coming-up)

If you find this project helpful, consider buying me a coffee or making a donation! Your support is greatly appreciated and helps fuel further development. 🙏

Also, don't forget to:

- ⭐ Star this project on GitHub
- 👍 Like and share if you find it useful
- 👔 Connect with me on [LinkedIn](https://www.linkedin.com/in/maxzaikin)
- 📢 Subscribe to my [Telegram channel](https://t.me/makszaikin) for updates and insights

## 🤝 Contributing

Contributions are highly appreciated and welcome! If you'd like to contribute, please fork the repository, create a new branch, and open a pull request.

## 📜 License

[MIT.]

## 📧 Contact

[Max.V.Zaikin / #OpenToWork] - [Max.V.Zaikin@gmail.com]

---

✨ Thank you for exploring TGramLLM! Let's explore the possibilities of integrating LLMs into everyday applications. 🌍