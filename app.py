import streamlit as st
from PIL import Image
import pytesseract
from ocr_utils import parse_questions
from qti_builder import build_qti_zip

st.title("📝 Canvas Quiz Generator from Screenshot")
st.write("Upload a screenshot with multiple-choice questions and download a Canvas-ready QTI quiz file.")

uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_column_width=True)

    if st.button("Extract & Generate QTI"):
        text = pytesseract.image_to_string(image)
        questions = parse_questions(text)

        if questions:
            zip_path = build_qti_zip(questions)
            with open(zip_path, "rb") as f:
                st.download_button("Download QTI Zip", f, file_name="canvas_quiz.zip", mime="application/zip")
        else:
            st.error("No questions found. Try another image or check OCR formatting.")
