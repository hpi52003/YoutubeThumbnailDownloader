# -*- coding: utf-8 -*-
"""YoutubeThumbnail.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xWATb4Fl0aI8byYmWFDmawX39_FOCK-F
"""

import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="YouTube Thumbnail Downloader",
    page_icon=":camera:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS for additional styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f0f0;
        color: #333;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .stSelectbox select {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .stText {
        font-size: 18px;
    }
    .stImage img {
        border: 2px solid #ddd;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("YouTube Thumbnail Downloader")

st.markdown("""
    <div style="text-align: center;">
        <p style="font-size: 18px;">Enter a YouTube Video Complete URL whose thumbnail you would like to download</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'url' not in st.session_state:
    st.session_state.url = ''
if 'resolution' not in st.session_state:
    st.session_state.resolution = 'maxresdefault'

# Input for YouTube URL
st.session_state.url = st.text_input('Enter YouTube Video Complete URL', st.session_state.url)

# Dropdown for selecting the resolution
resolution_options = [
    'default', 'mqdefault', 'hqdefault', 'sddefault', 'maxresdefault'
]
st.session_state.resolution = st.selectbox(
    'Select Thumbnail Resolution',
    resolution_options,
    index=resolution_options.index(st.session_state.resolution)
)

# Process the URL to extract the video ID
url = st.session_state.url
if url and '=' in url:
    video_id = url.split('v=')[1].split('&')[0]
else:
    video_id = ''

# Generate the thumbnail URL
thumbnail_url = f'https://img.youtube.com/vi/{video_id}/{st.session_state.resolution}.jpg'

# Display the thumbnail image and offer download functionality
if video_id:
    st.markdown(f"""
        <div style="text-align: center;">
            <p style="font-size: 20px; color: #333;">{st.session_state.resolution.capitalize()} Thumbnail - Right Click and Save it!!!</p>
        </div>
        """, unsafe_allow_html=True)

    st.image(thumbnail_url, use_column_width=True)

    # Download Button
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.write("Download Thumbnail:")
    if st.button('Download Thumbnail'):
        with st.spinner('Processing download...'):
            try:
                # Fetch the image
                response = requests.get(thumbnail_url)
                response.raise_for_status()  # Check for HTTP errors

                # Prepare download
                st.download_button(
                    label="Download Thumbnail",
                    data=response.content,
                    file_name=f"{video_id}_{st.session_state.resolution}.jpg",
                    mime="image/jpeg"
                )
                st.success('Thumbnail is ready to download!')
            except requests.HTTPError as e:
                st.error(f"Error fetching image: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="text-align: center; color: red;">
            <p style="font-size: 18px;">Please enter a valid YouTube URL.</p>
        </div>
        """, unsafe_allow_html=True)