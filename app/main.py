# app/main.py
import gradio as gr
from src.inference import infer
import os

def answer(image, question):
    if image is None or question.strip() == "":
        return "Upload an image and enter a question."

    # Save uploaded image temporarily
    temp_path = os.path.join("data/images/temp_upload.jpg")
    image.save(temp_path)

    result = infer(image, question, image_path=temp_path)
    return result.get("answer", "")

# Absolute path for background image
bg_path = os.path.abspath("app/static/bg.png").replace("\\", "/")

# Custom CSS
custom_css = f"""
body {{
    background-image: url('file://{bg_path}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Centered layout and wide container */
.gr-block {{
    max-width: 1200px;
    margin: auto;
    padding-top: 30px;  /* Space below title */
}}

/* Make response text larger and box taller */
#response-box textarea {{
    font-size: 18px;
    height: 250px !important;
    resize: none;
}}

/* Button row aligned to left */
#button-row {{
    display: flex;
    justify-content: flex-start;
    gap: 15px;
    margin-top: 10px;
}}

/* Button styling */
#submit-btn, #clear-btn {{
    width: 240px !important;   /* Adjust horizontal length */
    height: 45px !important;   /* Adjust vertical height */
    font-size: 20px !important;
    font-weight: bold;
    border-radius: 10px;
    flex: 0 0 auto !important;
}}

#submit-btn {{
    background-color: #FF7F0F !important;
    color: white !important;
}}

#clear-btn {{
    background-color: #555 !important;
    color: white !important;
}}

/* Hide entire footer */
footer {{
    display: none !important;
}}
"""

# Styled title (Campus white, View orange)
title_html = """
<div style="text-align:center; font-size: 48px; font-weight:bold; margin-bottom:20px;">
    <span style="color:white;">Campus</span>
    <span style="color:#FF7F0F;">View</span> — Visual Campus Navigator
</div>
"""

# Build interface
with gr.Blocks(css=custom_css, title="CampusView") as iface:
    # Favicon
    gr.HTML('<link rel="icon" type="image/png" href="app/static/favicon.png">')
    
    # Title
    gr.HTML(title_html)
    
    # Input/output row
    with gr.Row():
        with gr.Column(scale=2):
            img_input = gr.Image(type="pil", label="Upload Image")
            txt_input = gr.Textbox(lines=2, label="Ask a question")
        with gr.Column(scale=3):
            output = gr.Textbox(label="Response", elem_id="response-box")

    # Buttons
    with gr.Row(elem_id="button-row"):
        submit_btn = gr.Button("Submit", elem_id="submit-btn")
        clear_btn = gr.Button("Clear", elem_id="clear-btn")

    # Button functionality
    submit_btn.click(answer, inputs=[img_input, txt_input], outputs=output)

    def clear_fields():
        return None, "", ""
    clear_btn.click(fn=clear_fields, inputs=None, outputs=[img_input, txt_input, output])

if __name__ == "__main__":
    iface.launch(share=True)
