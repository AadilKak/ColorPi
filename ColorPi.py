import streamlit as st
from PIL import Image
import numpy as np
from skimage import color
from scipy.spatial import distance

# Function to calculate color data
def calculate_color_data(image):
    avg_color = np.array(image).mean(axis=(0, 1))[:3]  # RGB
    rgb = avg_color / 255  # Normalize for conversions

    # Convert to different color spaces
    hex_color = "#{:02x}{:02x}{:02x}".format(int(avg_color[0]), int(avg_color[1]), int(avg_color[2]))
    cmyk = [round((1 - c) * 100) for c in rgb] + [round(min(1 - rgb) * 100)]  # CMYK in percent
    lab = color.rgb2lab(rgb.reshape(1, 1, 3)).flatten()
    lch = color.lab2lch(lab.reshape(1, 1, 3)).flatten()

    # Format values
    rgb_formatted = [int(c) for c in avg_color]  # RGB as integers
    lab_formatted = [round(float(c), 1) for c in lab]  # CIELAB rounded to 1 decimal place
    lch_formatted = [
        round(float(lch[0]), 1),  # L (lightness)
        round(float(lch[1]), 1),  # C (chroma)
        round(float(lch[2]), 1)  # H (hue in degrees)
    ]

    return {
        'RGB': rgb_formatted,
        'HEX': hex_color,
        'CMYK': cmyk,
        'CIELAB': lab_formatted,
        'LCHab': lch_formatted,
        'LAB': lab
    }


# Function to calculate Delta E between two LAB colors
def delta_e(c1, c2, method='CIE76'):
    if method == 'CIE76':
        return distance.euclidean(c1, c2)
    elif method == 'CIE2000':
        return delta_e2000(c1, c2)
    else:
        raise ValueError("Unknown Delta E method specified.")


def delta_e2000(c1, c2):
    # Implementation of Delta E 2000
    L1, a1, b1 = c1
    L2, a2, b2 = c2

    C1 = np.sqrt(a1 ** 2 + b1 ** 2)
    C2 = np.sqrt(a2 ** 2 + b2 ** 2)
    delta_L = L2 - L1
    delta_a = a2 - a1
    delta_b = b2 - b1
    delta_C = C2 - C1
    delta_H = np.sqrt((delta_a ** 2 + delta_b ** 2) - delta_C ** 2)

    SL = 1  # Weighting factors
    SC = 1
    SH = 1

    # Calculate the average for L, C and H
    L_avg = (L1 + L2) / 2
    C_avg = (C1 + C2) / 2

    T = (1 - 0.17 * np.cos(np.radians(L_avg - 30)) +
         0.24 * np.cos(np.radians(2 * L_avg)) +
         0.32 * np.cos(np.radians(3 * L_avg + 6)) -
         0.20 * np.cos(np.radians(4 * L_avg - 63)))

    SL = 1 + ((0.015 * ((L_avg - 50) ** 2)) / np.sqrt(20 + ((L_avg - 50) ** 2)))
    SC = 1 + (0.045 * C_avg)
    SH = 1 + (0.015 * C_avg * T)

    delta_E = np.sqrt((delta_L / SL) ** 2 + (delta_C / SC) ** 2 + (delta_H / SH) ** 2)
    return delta_E


# Streamlit app
st.title("Color Data Extractor")

# Sidebar for uploading multiple images
st.sidebar.header("Upload Images")
uploaded_files = st.sidebar.file_uploader("Upload images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    # Create columns based on the number of uploaded images
    cols = st.columns(len(uploaded_files))

    # Define a fixed image size
    fixed_size = (300, 300)  # Width, Height

    color_data_list = []

    for i, uploaded_file in enumerate(uploaded_files):
        # Load the image
        image = Image.open(uploaded_file)

        # Resize the image to a fixed size
        image_resized = image.resize(fixed_size)

        # Display the uploaded image
        with cols[i]:
            st.image(image_resized, caption=f"Uploaded Image {i + 1}", use_column_width=False)

            # Calculate color data for the image
            color_data = calculate_color_data(image)
            color_data_list.append(color_data)

            # Display results without brackets and quotes
            st.write("Color Data:")
            st.write("RGB:", ', '.join(map(str, color_data['RGB'])))
            st.write("HEX:", color_data['HEX'])
            st.write("CMYK:", ', '.join(f"{value}%" for value in color_data['CMYK']))
            st.write("CIELAB:", ', '.join(map(str, color_data['CIELAB'])))
            st.write("LCHab:", ', '.join(map(str, color_data['LCHab'])))

    # Calculate Delta E if two images are uploaded
    if len(uploaded_files) == 2:
        lab1 = color_data_list[0]['LAB']
        lab2 = color_data_list[1]['LAB']
        delta_e76 = delta_e(lab1, lab2, method='CIE76')
        delta_e2000 = delta_e(lab1, lab2, method='CIE2000')

        # Display Delta E results
        st.write("Color Difference:")
        st.write("Delta E 76:", round(delta_e76, 2))
        st.write("Delta E 2000:", round(delta_e2000, 2))
