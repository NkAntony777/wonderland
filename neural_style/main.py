import streamlit as st
from PIL import Image
import os
import time
import io
import style  # Ensure the style module is properly implemented

# Helper function to resize image and compress it under 1MB
def compress_image(image, target_size_kb=1024):
    """Compresses the image to be under target_size_kb in kilobytes."""
    # Convert image to RGB mode (if necessary)
    image = image.convert('RGB')
    
    # Define initial quality and size
    quality = 50
    while True:
        # Save image to a byte buffer
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)
        
        # Check the size of the image in bytes
        size_in_kb = len(buffer.getvalue()) / 1024  # in KB
        
        # If the size is under the target size, break the loop
        if size_in_kb <= target_size_kb:
            return Image.open(buffer)
        
        # If the size is too large, reduce quality and try again
        quality -= 5
        if quality <= 30:  # Prevent it from going too low in quality
            break

    # Return the compressed image
    return Image.open(buffer)

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
    
    # Open the uploaded image
    input_image = Image.open(input_image_path)
    
    # Compress image to be under 1MB
    input_image = compress_image(input_image, target_size_kb=1024)  # target size is 1MB (1024KB)
else:
    input_image_path = f"neural_style/images/content-images/{img}"
    input_image = Image.open(input_image_path)

# Define paths for selected images and models
model_path = f"neural_style/saved_models/{style_name}.pth"
style_image_path = f"neural_style/images/style-images/{style_name}.jpg"
output_dir = "neural_style/images/output-images"
os.makedirs(output_dir, exist_ok=True)
timestamp = time.strftime("%Y%m%d-%H%M%S")
output_image_path = f"{output_dir}/{style_name}-{os.path.basename(input_image_path)}-{timestamp}.jpg"

# Layout the images in two columns
col1, col2 = st.columns(2)

# Display the input image in the left column
try:
    with col1:
        st.write("### Source Image")
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
