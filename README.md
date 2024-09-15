# Text Generation with API and Local GPT Models

This project is a text generation interface built with **Gradio** that allows users to generate text using both a local GPT-2 model and an external API (OpenAI/Meta-LLaMA). The application provides configurable parameters for generating text and includes several example prompts for easy use.

## Features

- **Local Model (GPT-2)**: Generates text using the pre-trained GPT-2 model from Hugging Face.
- **API Model (Meta-Llama)**: Uses a remote model (Meta-Llama) via a custom API for text generation.
- **Configurable Parameters**: Set temperature, repetition penalty, max tokens, and optional stop phrases for fine-tuning the output.
- **Prompt Append**: The generated text can be appended to the input prompt for further continuation.
- **UI Built with Gradio**: Easy-to-use interface that allows for interactive text generation.
