# YouTube Video Summarizer

The YouTube Video Summarizer is a web application built using Streamlit and Python. It allows users to extract and summarize content from YouTube videos using Google's Generative AI models, with the option to download summaries as PDF documents.

## Features

- **Video Link Input**: Users can input a YouTube video link.
- **Google API Integration**: Requires a Google API key for authentication.
- **Transcript Extraction**: Utilizes the YouTube Transcript API to fetch video transcripts.
- **Summary Generation**: Generates summaries using Google's Generative AI models (Gemini-Pro).
- **Summary Length Selection**: Users can choose between short, medium, or long summaries.
- **PDF Download**: Summaries can be downloaded as PDF documents for offline access.
- **User Interface**: Built with Streamlit, providing an intuitive and interactive interface.

## Architecture

### Components

- **Frontend**: Streamlit for the user interface.
- **Backend**: Python scripts integrating YouTube Transcript API, Google Generative AI (Gemini-Pro model), and ReportLab for PDF generation.

### Workflow

1. **User Inputs**: Enter a YouTube video link and Google API key.
2. **Transcript Extraction**: Fetches the video transcript using YouTube Transcript API.
3. **Summary Generation**: Generates a summary based on the extracted transcript using Google's Generative AI.
4. **PDF Creation**: Converts the generated summary into a downloadable PDF document using ReportLab.

## Installation

1. Clone the repository:
git clone https://github.com/your/repository.git
cd repository


2. Install dependencies:
pip install -r requirements.txt


3. Run the application:
streamlit run app.py


4. Access the application in your browser at `http://localhost:8501`.

## Usage

- Enter a valid YouTube video link and your Google API key.
- Select the desired summary length (short, medium, long).
- Click the "Get Summary" button to generate and view the summary.
- Optionally, download the summary as a PDF using the provided download button.

## Technologies Used

- Python
- Streamlit
- Google Generative AI (Gemini-Pro model)
- YouTube Transcript API
- ReportLab
