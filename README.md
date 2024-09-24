---
title: Text Completion
emoji: 📚
colorFrom: red
colorTo: green
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# Text Generation with API and Local GPT Models

This project is a text generation interface built with **Gradio** that allows users to generate text using both a local GPT-2 model and an external API (OpenAI/Meta-LLaMA). The application provides configurable parameters for generating text and includes several example prompts for easy use.

## Features

- **Local Model (GPT-2)**: Generates text using the pre-trained GPT-2 model from Hugging Face.
- **API Model (Meta-Llama)**: Uses a remote model (Meta-Llama) via a custom API for text generation.
- **Configurable Parameters**: Set temperature, repetition penalty, max tokens, and optional stop phrases for fine-tuning the output.
- **Prompt Append**: The generated text can be appended to the input prompt for further continuation.
- **UI Built with Gradio**: Easy-to-use interface that allows for interactive text generation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RahulChhatbar/Text-Generation.git
   cd Text-Generation
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the API key for the external API model. You can get your API key from [https://app.hyperbolic.xyz/](https://app.hyperbolic.xyz/). Export the key as an environment variable:
   ```bash
   export HYPERBOLIC_API_KEY="your-api-key"
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open the Gradio interface in your browser.

## Interface Overview

- **Prompt Input**: Text input where the user provides a starting sentence or prompt for the model to generate text.
- **Generated Completion**: Displays the generated text from the model (either local or API).
- **Model Parameters**: Sliders and textboxes to configure the model behavior:
   - **Temperature**: Controls the creativity of the model. Higher values result in more random output.
   - **Repetition Penalty**: Penalizes repeated words in the output.
   - **Max Tokens**: The maximum length of the generated output.
   - **Stop Phrase**: Optionally specify a word or phrase that will stop the text generation.
- **Example Prompts**: Select from a dropdown list of pre-defined example prompts to quickly generate text.

## Local Model vs API Model

- **Local Model**: Uses the GPT-2 model via the `transformers` library to generate text on your local machine. No internet connection is required after downloading the model.

- **API Model**: Connects to an external API (Meta-Llama) to generate text. Requires a valid API key and internet access.

## Customization

You can customize the project by:
- Changing the model used in the `local_generate_completion` function.
- Modifying the interface layout in the Gradio blocks.
- Adding more example prompts or modifying the existing ones.
