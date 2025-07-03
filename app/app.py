import os
import gradio as gr
from transformers import pipeline
import requests
from fpdf import FPDF

story_generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device=0)
COMFYUI_API_URL = "http://localhost:8188/prompt"

def generate_story(prompt, max_length=400):
    story = story_generator(prompt, max_length=max_length, do_sample=True, temperature=0.9)
    return story[0]["generated_text"]

def generate_image(prompt):
    payload = {"prompt": prompt, "steps": 30}
    try:
        response = requests.post(COMFYUI_API_URL, json=payload)
        if response.ok:
            return "static/generated_image.jpg"  # Placeholder
        else:
            return None
    except Exception:
        return None

def create_pdf(story_text, image_paths):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, story_text)
    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, x=10, y=30, w=180)
    filename = "storybook.pdf"
    pdf.output(filename)
    return filename

def generate_comic(prompt):
    story = generate_story(prompt)
    image_path = generate_image(prompt)
    if not image_path:
        return "Image generation failed.", None, None
    pdf_path = create_pdf(story, [image_path])
    return story, image_path, pdf_path

iface = gr.Interface(
    fn=generate_comic,
    inputs=gr.Textbox(lines=3, placeholder="Enter a story idea here..."),
    outputs=[
        gr.Textbox(label="Generated Story"),
        gr.Image(label="Generated Illustration"),
        gr.File(label="Download Storybook PDF")
    ],
    title="AI Comic Book Generator",
    description="Enter your story idea. The AI will generate a short story, illustrate it, and export a PDF."
)

if __name__ == "__main__":
    iface.launch()
