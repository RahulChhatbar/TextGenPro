import gradio as gr
from openai import OpenAI
import os

# Initialize the OpenAI client
api_key = os.environ.get('HYPERBOLIC_API_KEY', 'your_default_api_key_here')
client = OpenAI(
    base_url="https://api.hyperbolic.xyz/v1",
    api_key=api_key,
)

def generate_completion(prompt, temperature, repetition_penalty, stop_phrase):
    try:
        completion = client.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-FP8",
            prompt=prompt,
            temperature=temperature,
            frequency_penalty=repetition_penalty,
            max_tokens=2000,
            stop=[stop_phrase] if stop_phrase else None
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def append_completion(prompt, completion):
    new_prompt = f"{prompt}\n{completion}".strip()
    return new_prompt, ""  # Return new prompt and empty completion

with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# Llama 3.1 405B Completion Interface")
    
    with gr.Row():
        with gr.Column(scale=2):
            prompt_input = gr.Textbox(label="Prompt", lines=5, placeholder="Enter your prompt here...")
        with gr.Column(scale=1):
            temperature_slider = gr.Slider(minimum=0, maximum=1, value=0.7, step=0.1, label="Temperature")
            repetition_penalty_slider = gr.Slider(minimum=0, maximum=2, value=1.1, step=0.1, label="Repetition Penalty")
            stop_phrase_input = gr.Textbox(label="Stop Phrase", placeholder="Enter stop phrase (optional)")
    
    generate_button = gr.Button("Generate Completion")
    
    output_text = gr.Textbox(label="Generated Completion", lines=10)
    
    append_button = gr.Button("Append Completion to Prompt")
    
    generate_button.click(
        generate_completion, 
        inputs=[prompt_input, temperature_slider, repetition_penalty_slider, stop_phrase_input],
        outputs=output_text
    )
    
    append_button.click(
        append_completion,
        inputs=[prompt_input, output_text],
        outputs=[prompt_input, output_text]
    )
    
    gr.Markdown("""
---
This interface is powered by the Llama 3.1 405B base model, served by [Hyperbolic](https://hyperbolic.xyz), The Open Access AI Cloud.

Thank you to Hyperbolic for making this base model available!
""")
iface.launch(share=True)
