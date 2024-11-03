import os

import streamlit as st
import cv2
import pytesseract
import re
import pandas as pd
from PIL import Image  # Import PIL for image handling
import numpy as np  # Needed for cv2 conversion
import io  # To handle in-memory byte streams


# Function to read text from an image using OCR
def read_text_from_image(image):
    # Convert the PIL image to a NumPy array
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'  # Adjust parameters for your needs
    text = pytesseract.image_to_string(gray, config=custom_config)
    return text


# Function to extract Delta E values
def extract_delta_e_values(text):
    delta_e_2000 = None
    delta_e_76 = None
    delta_e_2000_match = re.search(r'Delta E2000:\s*([\d.]+)', text)
    delta_e_76_match = re.search(r'Delta E76:\s*([\d.]+)', text)

    if delta_e_2000_match:
        delta_e_2000 = delta_e_2000_match.group(1)
    if delta_e_76_match:
        delta_e_76 = delta_e_76_match.group(1)

    return delta_e_2000, delta_e_76


# Function to extract RGB values
def extract_rgb_values(text):
    rgb_standard = None
    rgb_testing = None
    rgb_match = re.findall(r'RGB:\s*([\d]+)\s*([\d]+)\s*([\d]+)', text)

    if len(rgb_match) >= 2:
        rgb_standard = rgb_match[0]
        rgb_testing = rgb_match[1]

    return rgb_standard, rgb_testing


# Function to extract CMYK values
def extract_cmyk_values(text):
    cmyk_standard = None
    cmyk_testing = None
    cmyk_match = re.findall(r'CMYK:\s*([\d]+)%\s*([\d]+)%\s*([\d]+)%\s*([\d]+)%', text)

    if len(cmyk_match) >= 2:
        cmyk_standard = cmyk_match[0]
        cmyk_testing = cmyk_match[1]

    return cmyk_standard, cmyk_testing


# Function to extract HEX values
def extract_hex_values(text):
    hex_standard = None
    hex_testing = None
    hex_match = re.findall(r'HEX:\s*#?([A-Fa-f0-9]{6})', text)

    if len(hex_match) >= 2:
        hex_standard = hex_match[0]
        hex_testing = hex_match[1]

    return hex_standard, hex_testing


# Function to extract CIELAB values
def extract_cielab_values(text):
    cielab_values = []
    cielab_matches = re.findall(
        r'CIELAB:\s*([-+]?\d+\.\d+)\s*([-+]?\d+\.\d+)\s*([-+]?\d+\.\d+)\s*CIELAB:\s*([-+]?\d+\.\d+)\s*([-+]?\d+\.\d+)\s*([-+]?\d+\.\d+)',
        text)

    for match in cielab_matches:
        cielab_values.extend(match)

    return cielab_values


# Function to extract LCH values
def extract_lch_values(text):
    lch_values = []
    lch_matches = re.findall(r'LCH.*?([\d.-]+)\s*([\d.-]+)\s*([\d.-]+°?)\s*LCH.*?([\d.-]+)\s*([\d.-]+)\s*([\d.-]+°?)',
                             text)

    for match in lch_matches:
        lch_values.extend(match)

    return lch_values


# Streamlit app layout
st.title("Delta E Value and Color Reader")

# Upload multiple images
uploaded_files = st.file_uploader("Choose images...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Initialize a list to store data for each image
data_list = []

# Set the maximum number of retries
max_retries = 2

if uploaded_files:
    # Store images as a dictionary for later display
    image_dict = {}
    existing_image_names = set()  # Set to track existing image names

    for uploaded_file in uploaded_files:
        # Read the uploaded image directly into memory
        image = Image.open(uploaded_file)

        # Strip the file extension from the image name
        image_name = os.path.splitext(uploaded_file.name)[0]  # Remove the extension

        # Check for duplicates
        if image_name not in existing_image_names:
            existing_image_names.add(image_name)

            # Save the image for display later
            image_dict[image_name] = image  # Use PIL to handle images

            for attempt in range(max_retries):
                # Extract text from the image
                extracted_text = read_text_from_image(image)

                # Process the extracted text to get Delta E values
                delta_e_2000, delta_e_76 = extract_delta_e_values(extracted_text)

                # Extract RGB values
                rgb_standard, rgb_testing = extract_rgb_values(extracted_text)

                # Extract CMYK values
                cmyk_standard, cmyk_testing = extract_cmyk_values(extracted_text)

                # Extract HEX values
                hex_standard, hex_testing = extract_hex_values(extracted_text)

                # Extract CIELAB values
                cielab_values = extract_cielab_values(extracted_text)

                # Extract LCH values
                lch_values = extract_lch_values(extracted_text)

                # Check if the data extraction was successful
                if all([delta_e_2000, delta_e_76, rgb_standard, rgb_testing, cmyk_standard, cmyk_testing, hex_standard,
                        hex_testing, cielab_values, lch_values]):
                    # Append data for the current image to the list
                    data_list.append({
                        "Image": image_name,
                        "Delta E2000": delta_e_2000,
                        "Delta E76": delta_e_76,
                        "Standard RGB": f"{rgb_standard[0]}, {rgb_standard[1]}, {rgb_standard[2]}",
                        "Testing RGB": f"{rgb_testing[0]}, {rgb_testing[1]}, {rgb_testing[2]}",
                        "Standard CMYK": f"{cmyk_standard[0]}%, {cmyk_standard[1]}%, {cmyk_standard[2]}%, {cmyk_standard[3]}%",
                        "Testing CMYK": f"{cmyk_testing[0]}%, {cmyk_testing[1]}%, {cmyk_testing[2]}%, {cmyk_testing[3]}%",
                        "Standard HEX": f"#{hex_standard}",
                        "Testing HEX": f"#{hex_testing}",
                        "Standard CIELAB": f"{cielab_values[0]}, {cielab_values[1]}, {cielab_values[2]}",
                        "Testing CIELAB": f"{cielab_values[3]}, {cielab_values[4]}, {cielab_values[5]}",
                        "Standard LCH": f"{lch_values[0]}, {lch_values[1]}, {lch_values[2]}",
                        "Testing LCH": f"{lch_values[3]}, {lch_values[4]}, {lch_values[5]}"
                    })
                    break  # Exit retry loop if successful
                else:
                    # Display less emphasized failure messages
                    st.sidebar.write(f"Attempt {attempt + 1} failed for {image_name}. Retrying...")

            else:
                st.sidebar.write(f"Failed to extract data from {image_name} after {max_retries} attempts.")

    # Create a DataFrame from the list of data
    df = pd.DataFrame(data_list)

    # Display the DataFrame as a wider table
    st.subheader("Extracted Color Data:")

    if not df.empty:  # Check if the DataFrame is not empty before displaying
        st.dataframe(df, use_container_width=True)  # Use container width for better visibility

        # Display images when the user clicks on the image name
        selected_image_name = st.selectbox("Select an Image to View:", df["Image"].tolist())

        if selected_image_name:
            st.image(image_dict[selected_image_name], caption=selected_image_name, use_column_width=True)
    else:
        st.write("No valid data extracted from the images.")
