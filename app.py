import os
import trimesh
import google.generativeai as genai
import streamlit as st
from werkzeug.utils import secure_filename

# Configure Google Gemini API Key
api_key= genai.configure("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY is not set. Please set the environment variable before running the app.")
else:
    genai.configure(api_key=api_key)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Streamlit App UI
st.title("Gen VIJAY AI Content Generation Engine")
st.subheader("Upload a CAD File and Generate AI-Based Textures")

# File Upload
uploaded_file = st.file_uploader("Upload your CAD file", type=["obj", "stl", "step", "iges", "dwg", "png"])

# Function to process CAD File
def process_cad_file(file_path):
    try:
        mesh = trimesh.load(file_path)
        processed_path = "processed_model.obj"
        mesh.export(processed_path)  # Convert CAD to OBJ
        return processed_path
    except Exception as e:
        return str(e)

# Function to Generate AI Texture using Gemini
def generate_ai_texture(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text  # Extract the generated text

# Handling File Upload & Processing
if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.name))

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Save file

    st.success(f"File uploaded successfully: {uploaded_file.name}")

    # Process CAD File
    processed_model = process_cad_file(file_path)
    st.write(f"Processed Model: {processed_model}")

    # Generate AI Texture
    prompt = st.text_input("Enter a texture prompt (e.g., 'Car with sunset lighting')", "Car in escarpment")

    if st.button("Generate AI Texture"):
        if not api_key:
            st.error("Cannot generate texture: GOOGLE_API_KEY is missing.")
        else:
            texture_description = generate_ai_texture(prompt)
            st.write("AI-Generated Texture Description:")
            st.write(texture_description)
