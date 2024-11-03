# ColorPi

Welcome to **ColorPi**, a web application built using Streamlit for analyzing color data from images. This app allows users to upload images, extract relevant color information, and visualize the results in an organized manner.

## Live Demo

You can access the live application here: [ColorPi Live Demo](https://colorpi.streamlit.app/)

## Features

- **Image Upload**: Easily upload multiple images to analyze color data.
- **Color Data Extraction**: The app extracts various color metrics, including:
  - Delta E2000
  - Delta E76
  - RGB values
  - CMYK values
  - HEX values
  - CIELAB values
  - LCH(ab) values
- **Data Presentation**: The extracted data is displayed in a structured table format for easy viewing and comparison.
- **Interactive Visualization**: Click on image entries to view the uploaded images directly within the app.
- **No Duplicates**: The app prevents duplicate entries for uploaded images.

## How to Use

1. **Upload Images**: Click the upload button and select one or more image files.
2. **Analyze Colors**: The app will automatically extract color data from the uploaded images.
3. **View Results**: Check the table for extracted color metrics. Click on any image tuple to view the corresponding image.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **OCR**: Optical Character Recognition for data extraction from images

## Known Issues

While we strive for accuracy and functionality, some bugs have been identified that we are working to resolve:

- **OCR Errors**: Some inaccuracies may occur during the OCR process, leading to incorrect color values being extracted.
- **Photo Storage**: Currently, there are challenges related to storing uploaded images for long-term access.
- **Google Drive Implementation**: Integration with Google Drive for file storage and retrieval is not yet fully implemented.

## Future Improvements

- Enhance the OCR functionality to reduce errors and improve data extraction accuracy.
- Implement a robust photo storage solution to manage uploaded images effectively.
- Complete the integration of Google Drive for seamless file handling.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report bugs, please open an issue or submit a pull request.


## Contact

For inquiries or further information, feel free to reach out at: aadil.kakkidi@gmail.com
