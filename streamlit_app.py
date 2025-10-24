# streamlit_app.py
import streamlit as st
from PIL import Image
import os
from io import BytesIO

# import your inference pipeline
from src.inference import infer

st.set_page_config(page_title="CampusView", page_icon=":school:", layout="centered")

# --- page header (Campus white / View orange) ---
st.markdown(
    """
    <div style="text-align:center; margin-top:10px;">
      <span style="font-size:42px; font-weight:700; color:white; font-family:Arial, sans-serif;">
        Campus
      </span>
      <span style="font-size:42px; font-weight:700; color:#FF7F0F; font-family:Arial, sans-serif;">
        View
      </span>
      <div style="font-size:16px; color:#ddd; margin-top:6px;">Visual Campus Navigator</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)  # gap

# --- uploader and question ---
col1, col2 = st.columns([1, 2])

with col1:
    uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
    submit = st.button("Submit")
    clear = st.button("Clear")

with col2:
    question = st.text_input("Ask a question", value="", key="question_input")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    response_box = st.empty()

# Helper: save uploaded image temporarily so your inference can accept a PIL image
def save_temp_image(uploaded_file):
    if uploaded_file is None:
        return None
    img = Image.open(BytesIO(uploaded_file.read())).convert("RGB")
    temp_dir = "data/images"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "temp_streamlit_upload.jpg")
    img.save(temp_path)
    return img, temp_path

# Clear behavior
if clear:
    # Reset uploader + input + response
    st.experimental_rerun()

# On submit
if submit:
    if uploaded is None or (question is None or question.strip() == ""):
        response_box.info("Please upload an image and enter a question.")
    else:
        pil_img, img_path = save_temp_image(uploaded)
        # call your existing infer -- returns dict with keys: answer, caption, ocr_text, objects
        try:
            result = infer(pil_img, question, image_path=img_path)
            answer = result.get("answer", "")
            caption = result.get("caption", "")
            ocr = result.get("ocr_text", "")
            objects = result.get("objects", [])
            # Show responses
            response_html = f"""
            <div style="background:rgba(0,0,0,0.5); padding:12px; border-radius:8px; color:#fff;">
              <b>Answer:</b> {st.markdown(answer)}<br>
              <b>Caption:</b> {caption}<br>
              <b>OCR:</b> {ocr if ocr else 'N/A'}<br>
              <b>Detected objects:</b> {objects if objects else '[]'}
            </div>
            """
            # show PIL image and text
            st.image(pil_img, use_column_width=True)
            response_box.markdown(f"**Answer:** {answer}")
            st.markdown(f"**Caption:** {caption}")
            if ocr:
                st.markdown(f"**OCR:** {ocr}")
            st.markdown(f"**Detected objects:** {objects}")
        except Exception as e:
            response_box.error(f"Inference error: {e}")
