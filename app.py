import streamlit as st
from PIL import Image
import pytesseract
from ocr_utils import parse_questions
from qti_builder import build_qti_zip
import io

st.set_page_config(layout="wide")

st.title("📝 Canvas Quiz Generator from Screenshot")
st.write("Upload or paste a screenshot of a multiple-choice question to generate a Canvas-compatible QTI file.")

# Layout: Two-column interface
left, right = st.columns([1, 1])

# Upload or paste image
with left:
    uploaded_file = st.file_uploader("📎 Upload screenshot", type=["png", "jpg", "jpeg"])
    pasted_image = st.camera_input("📸 Or paste/take a screenshot")

    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
    elif pasted_image:
        image = Image.open(pasted_image)

    if image:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        text = pytesseract.image_to_string(image)
        questions = parse_questions(text)

        if questions:
            preview = questions[0]  # Only preview first for now

            with right:
                st.markdown("### 👁️ Canvas-Style Preview")
                st.markdown(f"**Question:** {preview['question']}")
                for ident, answer in preview['answers']:
                    correct = "✅" if ident == preview['correct'] else "◻️"
                    st.markdown(f"{correct} **{ident}.** {answer}")

            if st.button("⬇️ Generate QTI Zip"):
                zip_path = build_qti_zip(questions)
                with open(zip_path, "rb") as f:
                    st.download_button("Download QTI File", f, file_name="canvas_quiz.zip", mime="application/zip")
        else:
            st.warning("⚠️ No questions were detected. Try cropping more tightly or enhancing image quality.")
