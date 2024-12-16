# Required imports
import streamlit as st
from PIL import Image
import os
import time
import style  # Ensure the style module is properly implemented

# Centering the title using HTML
st.markdown("<h1 style='text-align: center;'>Image Style Transfer</h1>", unsafe_allow_html=True)

# Sidebar - original image selection
st.sidebar.write("### Select Source Image")
img = st.sidebar.selectbox(
    'Choose an image from the library:',
    ('amber.jpg', 'cat.png', 'room.jpg', 'buildings.jpg'))

# Sidebar - style selection
st.sidebar.write("### Select Style")
style_name = st.sidebar.selectbox(
    'Choose a style:',
    ('candy', 'mosaic', 'rain_princess', 'udnie')
)

# Upload custom image
st.sidebar.write("### Or Upload Your Own Image")
uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "png"])
if uploaded_image:
    input_image_path = f"uploaded_images/{uploaded_image.name}"
    # Save uploaded image
    os.makedirs("uploaded_images", exist_ok=True)
    with open(input_image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
else:
    input_image_path = f"images/content-images/{img}"

# Define paths for selected images and models
model_path = f"saved_models/{style_name}.pth"
style_image_path = f"images/style-images/{style_name}.jpg"
output_dir = "images/output-images"
os.makedirs(output_dir, exist_ok=True)
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_image_path = f"{output_dir}/{style_name}-{os.path.basename(input_image_path)}-{timestamp}.jpg"

# Layout the images in two columns
col1, col2 = st.columns(2)

# Display the input image in the left column
try:
    with col1:
        st.write("### Source Image")
        input_image = Image.open(input_image_path)
        st.image(input_image, width=300)
except Exception as e:
    st.error(f"Error loading source image: {e}")

# Display the style image in the right column
try:
    with col2:
        st.write("### Style Image")
        style_image = Image.open(style_image_path)
        st.image(style_image, width=300)
except Exception as e:
    st.error(f"Error loading style image: {e}")

# Stylize button
clicked = st.button('Stylize', key="stylize_button")

if clicked:
    try:
        with st.spinner('Stylizing image...'):
            # Load the model and stylize the image
            model = style.load_model(model_path)
            style.stylize(model, input_image_path, output_image_path)
        st.success('Stylization complete!')

        # Display the output image
        st.markdown("<h2 style='text-align: center;'>Stylized Image</h2>", unsafe_allow_html=True)
        output_image = Image.open(output_image_path)

        output_image = output_image.resize((500, 500))
        st.image(output_image)

        # Provide a download button
        with open(output_image_path, "rb") as file:
            st.download_button(
                label="Download Stylized Image",
                data=file,
                file_name=f"stylized-{os.path.basename(input_image_path)}",
                mime="image/jpeg"
            )
    except Exception as e:
        st.error(f"An error occurred during stylization: {e}")

# Footer
st.markdown("<footer style='text-align: center;'>© 2024 Image Style Transfer</footer>", unsafe_allow_html=True)
