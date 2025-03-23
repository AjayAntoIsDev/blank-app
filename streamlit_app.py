import streamlit as st
import requests
import subprocess
import random
from urllib.parse import quote
from io import BytesIO

st.set_page_config(page_title="image_gen", page_icon="🎨", layout="wide")

st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-size: 16px !important;
            padding: 10px 24px !important;
            border-radius: 10px !important;
            border: none !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049 !important;
        }
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input {
            font-size: 16px !important;
        }
        .stCheckbox>div>div {
            font-size: 16px !important;
        }
        .title-text {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            background: -webkit-linear-gradient(left, #ff7eb3, #ff758c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='background: linear-gradient(90deg, #ff7eb3, #ff758c); -webkit-background-clip: text; -webkit-text-fill-color: transparent;' class='title-text'>🎨 AI Image Generator</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")

    width = st.slider("Width:", 256, 2048, 512, step=1)
    height = st.slider("Height:", 256, 2048, 512, step=1)

    random_seed = st.checkbox("Use Random Seed", value=True)
    if random_seed:
        seed = random.randint(1, 1337)
    else:
        if "seed" not in st.session_state:
            st.session_state.seed = 42  
        seed = st.number_input("Seed:", value=st.session_state.seed, min_value=1, max_value=1337, step=1)

    model = st.selectbox("Model:", ["flux", "flux-pro", "flux-realism", "flux-anime", "flux-3d", "flux-cablyai", "turbo"], index=0)

    st.subheader("🛠️ Additional Options")
    nologo = st.checkbox("Remove Watermark", value=True)
    private = st.checkbox("Keep image private", value=True)
    enhance = st.checkbox("Enhance prompt", value=True)
    safe = st.checkbox("Safe", value=True)

    st.subheader("ℹ️ About")
    st.markdown("""
    Made by Ajay Anto  
    """, unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>Enter Your Image Prompt</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    prompt = st.text_input("Prompt:", placeholder="A futuristic city at sunset 🌇", label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🎨 Generate Image", use_container_width=True):
        if not prompt.strip():
            st.error("❌ Please enter a valid prompt.")
        else:
            encoded_prompt = quote(prompt)
            base_url = "https://image.pollinations.ai/prompt/"
            params = {
                "width": width,
                "height": height,
                "seed": seed,
                "nologo": str(nologo).lower(),
                "private": str(private).lower(),
                "enhance": str(enhance).lower(),
                "model": model,
                "safe": str(safe).lower()
            }
            url = f"{base_url}{encoded_prompt}?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
            response = requests.get(url)

            if response.status_code == 200:

                st.image(response.content, caption=f"✨ Generated Image", width=width)
                st.download_button('📥 Download Image', data=response.content, file_name=prompt+".png", mime="image/png")
                st.code("")
            else:
                st.error(f"❌ Failed to generate image. Status code: {response.status_code}")
