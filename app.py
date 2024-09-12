import gradio as gr
from openai import OpenAI
from transformers import pipeline
import os
import torch

device = 0 if torch.cuda.is_available() else -1

# Initialize the OpenAI client
api_key = os.environ.get('HYPERBOLIC_API_KEY')
client = OpenAI(
    base_url="https://api.hyperbolic.xyz/v1",
    api_key=api_key,
)

def local_generate_completion(prompt, max_tokens, device):
    try:
        completion = pipeline("text-generation", model='openai-gpt')
        res = completion(prompt, max_new_tokens=max_tokens, device=device)
        return res[0]['generated_text']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_completion(prompt, temperature, repetition_penalty, stop_phrase, max_tokens):
    try:
        completion = client.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B",
            prompt=prompt,
            temperature=temperature,
            frequency_penalty=repetition_penalty,
            max_tokens=max_tokens,
            stop=[stop_phrase] if stop_phrase else None
        )
        return prompt + " " + completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def append_completion(completion):
    return completion.strip(), ""  # Return new prompt and empty completion

def clear_fields():
    return "", ""

with gr.Blocks(theme=gr.themes.Soft()) as iface:

    gr.Markdown("# Llama 3.1 405B Completion Interface")

    with gr.Row():
            prompt_input = gr.Textbox(label="Prompt", value="The best thing about being a cat is")
        
    with gr.Row():
        with gr.Column():
            temperature_slider = gr.Slider(minimum=0, maximum=1, value=0.7, step=0.1, label="Temperature")
            repetition_penalty_slider = gr.Slider(minimum=0, maximum=2, value=0.1, step=0.1, label="Repetition Penalty")
            max_tokens_slider = gr.Slider(minimum=1, maximum=4000, value=250, step=1, label="Max Tokens")
            stop_phrase_input = gr.Textbox(label="Stop Phrase", placeholder="Enter stop phrase (optional)")
        with gr.Column():
            temperature_slider = gr.Slider(minimum=0, maximum=1, value=0.7, step=0.1, label="Temperature")
            repetition_penalty_slider = gr.Slider(minimum=0, maximum=2, value=0.1, step=0.1, label="Repetition Penalty")
            max_tokens_slider = gr.Slider(minimum=1, maximum=4000, value=250, step=1, label="Max Tokens")
            stop_phrase_input = gr.Textbox(label="Stop Phrase", placeholder="Enter stop phrase (optional)")
    
    with gr.Row():
        generate_button = gr.Button("API Model Text Generation")
        local_generate_button = gr.Button("Local Model Text Generation")
        append_button = gr.Button("Append Completion to Prompt")
        clear_button = gr.Button("Clear All Fields")
    
    output_text = gr.Textbox(label="Generated Completion", lines=10)
    
    generate_button.click(
        generate_completion,
        inputs=[prompt_input, temperature_slider, repetition_penalty_slider, stop_phrase_input, max_tokens_slider],
        outputs=output_text
    )

    local_generate_button.click(
        local_generate_completion,
        inputs=[prompt_input],
        outputs=output_text
    )
    
    append_button.click(
        append_completion,
        inputs=[output_text],
        outputs=[prompt_input, output_text]
    )
    
    clear_button.click(
        clear_fields,
        outputs=[prompt_input, output_text]
    )
    
    gr.Markdown("""
    ---
    This interface is powered by the Llama 3.1 405B base model, served by [Hyperbolic](https://hyperbolic.xyz), The Open Access AI Cloud.
    Thank you to Hyperbolic for making this base model available!
    """)

iface.launch(share=False)
