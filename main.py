import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_app import app  # Import your Streamlit app

# Load environment variables
load_dotenv()

# Function to run the Streamlit app
def run_app():
    app()

if __name__ == "__main__":
    run_app()
