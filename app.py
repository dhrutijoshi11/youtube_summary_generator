import base64

import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer", layout="wide")


# Function to add background image from local file
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                        url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local('/Users/dhrutijoshi/PycharmProjects/YouTube-Video-Summarizer/bg_image.jpg')


# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(segment["text"] for segment in transcript)
    except NoTranscriptFound:
        st.error("Transcript not found for this video.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Function to generate summary using Google's Generative AI
def generate_gemini_content(transcript_text, prompt, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Function to create PDF from summary
def create_pdf(summary_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(72, 800, "Summary")
    text = c.beginText(40, 780)
    text.setFont("Helvetica", 12)
    for line in summary_text.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def main_page():
    st.markdown("""
        <h1 style='text-align: Center;'>YouTube Video Summarizer</h1>
        <p style='font-size: 20px;'>
            <strong>Welcome!</strong> This tool summarizes YouTube videos into concise notes.
            Enter the video link and your Google API key, choose the summary length, and click the button.
        </p>
    """, unsafe_allow_html=True)

    google_api_key = st.text_input("Enter your Google API Key:", type="password")
    youtube_link = st.text_input("Enter YouTube Video Link:")
    summary_length = st.select_slider(
        "Select Summary Length:", options=['Short', 'Medium', 'Long'], value='Medium'
    )

    # Store inputs in session state
    if st.button("Proceed to Summary Page"):
        if google_api_key and youtube_link:
            st.session_state.google_api_key = google_api_key
            st.session_state.youtube_link = youtube_link
            st.session_state.summary_length = summary_length
            st.session_state.page = "summary"
        else:
            st.error("Please provide both Google API key and YouTube video link.")


def summary_page():
    st.title("Video Thumbnail and Summary")
    st.markdown("### Video Thumbnail")

    youtube_link = st.session_state.youtube_link
    video_id = youtube_link.split("=")[1]
    video_thumbnail = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(video_thumbnail, caption="Video Thumbnail", use_column_width=True)

    if st.button("Get Detailed Notes"):
        with st.spinner("Processing..."):
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                google_api_key = st.session_state.google_api_key
                summary_length = st.session_state.summary_length
                prompt = """You are a YouTube video summarizer. Summarize the video content into key points within 1500 words."""
                customized_prompt = f"{prompt} Please generate a {summary_length.lower()} summary."
                summary = generate_gemini_content(transcript_text, customized_prompt, google_api_key)
                if summary:
                    st.success("Transcript extracted and summary generated successfully!")
                    st.subheader("Detailed Notes:")
                    st.write(summary)
                    pdf_bytes = create_pdf(summary)
                    st.download_button(label="Download Summary as PDF",
                                       data=pdf_bytes,
                                       file_name="YouTube_Summary.pdf",
                                       mime="application/pdf")
                else:
                    st.error("Failed to generate summary.")
            else:
                st.error("Failed to extract transcript.")

    if st.button("Back"):
        st.session_state.page = "main"


# Render the appropriate page based on session state
if 'page' not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
else:
    summary_page()
