import gradio as gr
from openai import OpenAI
from transformers import pipeline
import os
import time
from prometheus_client import Summary, Counter, Gauge, start_http_server

LOCAL_REQUEST_COUNT = Counter('local_product_request_count', 'Total number of requests to Local Product')
LOCAL_SUCCESS_COUNT = Counter('local_product_success_count', 'Total number of successful requests in Local Product')
LOCAL_ERROR_COUNT = Counter('local_product_error_count', 'Total number of errors in Local Product')
LOCAL_REQUEST_TIME = Summary('local_product_request_processing_seconds', 'Time spent processing requests in Local Product')
LOCAL_ACTIVE_REQUEST_COUNT = Gauge('local_product_active_request_count', 'Number of active requests in Local Product')

API_REQUEST_COUNT = Counter('api_product_request_count', 'Total number of requests to API Product')
API_SUCCESS_COUNT = Counter('api_product_success_count', 'Total number of successful requests in API Product')
API_ERROR_COUNT = Counter('api_product_error_count', 'Total number of errors in API Product')
API_REQUEST_TIME = Summary('api_product_request_processing_seconds', 'Time spent processing requests in API Product')
API_ACTIVE_REQUEST_COUNT = Gauge('api_product_active_request_count', 'Number of active requests in API Product')

ACTIVE_USER_COUNT = Gauge('active_user_count', 'Number of active users')


def check_api_key():
    api_key = os.environ.get('HYPERBOLIC_API_KEY')
    if api_key is None:
        raise ValueError("Please set the HYPERBOLIC_API_KEY environment variable.")
    return api_key


def user_join():
    ACTIVE_USER_COUNT.inc()


def user_leave():
    ACTIVE_USER_COUNT.dec()


@LOCAL_REQUEST_TIME.time()
def local_generate_completion(prompt, max_tokens, temperature, repetition_penalty, top_p):
    LOCAL_REQUEST_COUNT.inc()
    LOCAL_ACTIVE_REQUEST_COUNT.inc()
    prompt = prompt.strip()
    top_p, repetition_penalty = float(top_p), float(repetition_penalty)
    try:
        completion = pipeline("text-generation", model="gpt2")
        res = completion(
            prompt,
            max_length=len(prompt) + max_tokens,
            num_return_sequences=1,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            top_p=top_p,
            truncation=True,
            clean_up_tokenization_spaces=True
        )
        generated_text = res[0]['generated_text']
        LOCAL_SUCCESS_COUNT.inc()
        LOCAL_ACTIVE_REQUEST_COUNT.dec()
        return generated_text[len(prompt) + 1:]
    except Exception as e:
        LOCAL_ERROR_COUNT.inc()
        LOCAL_ACTIVE_REQUEST_COUNT.dec()
        return f"An error occurred: {str(e)}"


@API_REQUEST_TIME.time()
def api_generate_completion(prompt, temperature, repetition_penalty, max_tokens, stop_phrase, top_p, api_key):
    API_REQUEST_COUNT.inc()
    API_ACTIVE_REQUEST_COUNT.inc()
    prompt = prompt.strip()
    top_p, repetition_penalty = float(top_p), float(repetition_penalty)
    try:
        client = OpenAI(
            base_url="https://api.hyperbolic.xyz/v1",
            api_key=api_key,
        )
        completion = client.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B",
            prompt=prompt,
            temperature=temperature,
            frequency_penalty=repetition_penalty,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=[stop_phrase] if stop_phrase else None
        )
        API_SUCCESS_COUNT.inc()
        API_ACTIVE_REQUEST_COUNT.dec()
        return completion.choices[0].text.strip()
    except Exception as e:
        API_ERROR_COUNT.inc()
        API_ACTIVE_REQUEST_COUNT.dec()
        return f"An error occurred: {str(e)}"


def append_completion(prompt, completion):
    prompt, completion = prompt.strip(), completion.strip()
    return f"{prompt}{' '}{completion}".strip(), ""


def clear_fields():
    return "", ""


def update_prompt(selected_example):
    return selected_example, ""


if __name__ == "__main__":
    api_key = check_api_key()

    start_http_server(8000)
    print("Prometheus metrics being served on port 8000")

    js = """
    function createGradioAnimation() {
        var container = document.createElement('div');
        container.id = 'gradio-animation';
        container.style.textAlign = 'center';
        container.style.marginBottom = '20px';

        // Create a container for the entire line
        var lineContainer = document.createElement('div');
        lineContainer.style.fontSize = '2.5em';
        lineContainer.style.fontWeight = 'bold';

        // "Welcome to" normal text
        var welcomeText = document.createElement('span');
        welcomeText.innerText = 'Welcome to, ';
        welcomeText.style.fontWeight = 'normal'; // Keep "Welcome to" normal
        welcomeText.style.fontSize = '0.65em'; // Reduce font size
        lineContainer.appendChild(welcomeText);

        // Fancy "TextGenPro" text
        var fancyText = document.createElement('span');
        fancyText.style.color = '#eab440';
        fancyText.style.display = 'inline-block';
        fancyText.style.textShadow = '0 1px #0267c1, -1px 0 #0093f5, -1px 2px #0267c1, -2px 1px #0093f5, -2px 3px #0267c1, -3px 2px #0093f5, -3px 4px #0267c1, -4px 3px #0093f5, -4px 5px #0267c1, -5px 4px #0093f5, -5px 6px #0267c1, -6px 5px #0093f5, -6px 7px #0267c1, 2px 2px 2px rgba(206, 89, 55, 0)';

        var text = 'TextGenPro'; 
        for (var i = 0; i < text.length; i++) {
            (function(i) {
                setTimeout(function() {
                    var letter = document.createElement('span');
                    letter.style.opacity = '0';
                    letter.style.transition = 'opacity 0.5s, transform 0.5s'; // Animation for opacity and transform
                    letter.innerText = text[i];

                    // Set initial scale and rotation
                    letter.style.transform = 'scale(0.5) rotate(-10deg)';

                    fancyText.appendChild(letter);

                    setTimeout(function() {
                        letter.style.opacity = '1';
                        letter.style.transform = 'scale(1) rotate(0deg)'; // Final scaling and rotation
                    }, 50);
                }, i * 150); // Slight delay for each letter
            })(i);
        }

        lineContainer.appendChild(fancyText);

        container.appendChild(lineContainer);

        var gradioContainer = document.querySelector('.gradio-container');
        gradioContainer.insertBefore(container, gradioContainer.firstChild);

        return 'Fancy single-line animation created';
    }
    """

    with gr.Blocks(theme=gr.themes.Soft(), css="#stop-button {background-color: red; color: white;}", js=js) as iface:
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(label="Prompt", value="Today is a beautiful day for", lines=10)
            with gr.Column():
                output_text = gr.Textbox(label="Generated Completion", lines=10)

        with gr.Row():
            with gr.Column():
                with gr.Accordion("API Model Parameters", open=False):
                    temperature_slider_api = gr.Slider(minimum=0, maximum=1, value=0.7, step=0.1, label="Temperature")
                    repetition_penalty_slider_api = gr.Slider(minimum=1, maximum=5, value=1.5, step=0.1,
                                                              label="Repetition Penalty")
                    max_tokens_slider_api = gr.Slider(minimum=1, maximum=4000, value=250, step=1, label="Max Tokens")
                    top_p_slider_api = gr.Slider(minimum=0, maximum=1, value=1, step=0.01,
                                                 label="Top-p (nucleus sampling)")
                    stop_phrase_input_api = gr.Textbox(label="Stop Phrase", placeholder="Enter stop phrase (optional)")

            with gr.Column():
                with gr.Accordion("Local Model Parameters", open=False):
                    temperature_slider_local = gr.Slider(minimum=0, maximum=1, value=0.7, step=0.1, label="Temperature")
                    repetition_penalty_slider_local = gr.Slider(minimum=1, maximum=5, value=1.5, step=0.1,
                                                                label="Repetition Penalty")
                    max_tokens_slider_local = gr.Slider(minimum=1, maximum=4000, value=250, step=1, label="Max Tokens")
                    top_p_slider_local = gr.Slider(minimum=0, maximum=1, value=1, step=0.01,
                                                   label="Top-p (nucleus sampling)")

        with gr.Row():
            api_generate_button = gr.Button("API Model Text Generation")
            local_generate_button = gr.Button("Local Model Text Generation")
            append_button = gr.Button("Append Completion to Prompt")
            clear_button = gr.Button("Clear All Fields")

        with gr.Row():
            stop_button = gr.Button("Stop Generation", elem_id="stop-button")

        example_prompts = [
            "Select Example Prompt",
            "As the clock struck midnight, she discovered a hidden message that said",
            "She had always dreamed of traveling to Paris, but her first stop was",
            "The new cafe in town serves a special latte that tastes like",
            "He promised to finish the project by Friday, but something unexpected happened",
            "After months of searching, the treasure map led them to a hidden cave with",
            "As she opened the old book, a dusty letter fell out, saying"
        ]

        examples_dropdown = gr.Dropdown(
            label="Example Prompts",
            choices=example_prompts[1:],
            value=example_prompts[0],
            allow_custom_value=True
        )

        examples_dropdown.change(
            update_prompt,
            inputs=[examples_dropdown],
            outputs=[prompt_input, output_text]
        )

        api_generation_event = api_generate_button.click(
            lambda prompt, temperature, repetition_penalty, max_tokens, stop_phrase, top_p: api_generate_completion(
                prompt, temperature, repetition_penalty, max_tokens, stop_phrase, top_p, api_key),
            inputs=[prompt_input, temperature_slider_api, repetition_penalty_slider_api, max_tokens_slider_api,
                    stop_phrase_input_api, top_p_slider_api],
            outputs=output_text
        )

        local_generation_event = local_generate_button.click(
            local_generate_completion,
            inputs=[prompt_input, max_tokens_slider_local, temperature_slider_local, repetition_penalty_slider_local,
                    top_p_slider_local],
            outputs=output_text
        )

        append_button.click(
            append_completion,
            inputs=[prompt_input, output_text],
            outputs=[prompt_input, output_text]
        )

        clear_button.click(
            clear_fields,
            outputs=[prompt_input, output_text]
        )

        stop_button.click(None, None, None, cancels=[api_generation_event, local_generation_event])

    iface.launch(share=False)
