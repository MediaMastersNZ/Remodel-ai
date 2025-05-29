
import streamlit as st
import replicate
from PIL import Image
import io

st.set_page_config(page_title="AI Room Remodel", layout="centered")
st.title("🏠 AI Room Remodel with Style")
st.markdown("Upload a room photo, choose a design style, and see it transformed by AI.")

# Input your Replicate API token securely
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", "YOUR_API_TOKEN_HERE")
replicate.Client(api_token=REPLICATE_API_TOKEN)

# Style options
style_map = {
    "Scandinavian": "scandinavian interior design",
    "Luxury": "luxury interior with gold accents",
    "Coastal": "beachside coastal design with airy colors",
    "Industrial": "industrial loft style with metal and concrete",
    "Minimalist": "ultra-clean minimal design with white space"
}

uploaded_file = st.file_uploader("Upload a room photo", type=["jpg", "jpeg", "png"])
selected_style = st.selectbox("Choose a remodel style", list(style_map.keys()))

if uploaded_file and selected_style:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Room", use_column_width=True)

    if st.button("Remodel with AI"):
        with st.spinner("Generating your remodeled room..."):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()

            prompt = f"Interior redesign in {style_map[selected_style]}"
            output = replicate.run(
                "stability-ai/sdxl:latest",
                input={"prompt": prompt, "image": img_bytes}
            )

            if output:
                st.image(output, caption=f"{selected_style} Remodel", use_column_width=True)
            else:
                st.error("Failed to generate remodel. Please try again.")
else:
    st.info("Upload an image and choose a style to begin.")
