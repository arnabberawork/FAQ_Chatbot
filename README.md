# Novanectar FAQ Chatbot

This repository contains the source code for an intelligent FAQ chatbot application designed to understand and respond to user queries. The system uses a combination of spaCy for natural language processing, WordNet for synset-based intent matching, and Hugging Face Transformers for paraphrasing. The app is built using Flask as the web framework to provide a simple API for interacting with the chatbot.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Approach](#approach)
- [Technologies/Libraries Used](#technologieslibraries-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Intent Matching](#intent-matching)
- [Conclusions](#conclusions)
- [Acknowledgements](#acknowledgements)
- [Glossary](#glossary)
- [Author](#author)

## Problem Statement

Novanectar receives a large number of frequently asked questions from users. Manually responding to these queries is time-consuming and inefficient. There is a need for an automated system that can understand user queries and provide accurate responses in real-time.

## Objectives

- Automate the process of answering frequently asked questions.
- Improve response accuracy using natural language processing (NLP) techniques.
- Provide a user-friendly interface for interacting with the chatbot.

## Approach

The Novanectar FAQ Chatbot is designed to automate the process of answering frequently asked questions. The chatbot uses NLP techniques to understand user queries and match them to predefined intents. Based on the matched intent, the chatbot provides an appropriate response. The system is built using Flask for the web interface, spaCy and NLTK for NLP, and the Hugging Face Transformers library for enhancing intent matching through paraphrase generation.

## Technologies/Libraries Used

- Flask
- spaCy
- NLTK
- Hugging Face Transformers
- Sentence-BERT

## Project Structure

- `app.py`: Main Flask application file that serves the HTML page and handles chatbot requests.
- `faq.py`: Contains the logic for intent matching and response generation.
- `requirements.txt`: List of Python dependencies.
- `static/style.css`: CSS file for styling the chatbot interface.
- `templates/index.html`: HTML template for the chatbot interface.

## Setup and Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Download the NLTK WordNet data:
    ```sh
    python -m nltk.downloader wordnet
    ```

5. Run the Flask application:
    ```sh
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5000` to access the chatbot interface.

## Usage

- Enter your query in the input box and click the "Submit" button.
- The chatbot will process your query and display the response below.

## Intent Matching

The chatbot uses spaCy for natural language processing and NLTK's WordNet for synonym matching. It also uses the Hugging Face Transformers library for generating paraphrases of user queries to improve intent matching. Additionally, it employs Sentence-BERT for better sentence similarity matching.

## Conclusions

The Novanectar FAQ Chatbot successfully automates the process of answering frequently asked questions, providing accurate and timely responses to user queries. This reduces the workload on support staff and improves user satisfaction.

## Acknowledgements

Official documentation of Flask, spaCy, NLTK, and the Hugging Face Transformers library.

## Glossary

- **NLP (Natural Language Processing)**: A field of artificial intelligence that focuses on the interaction between computers and humans through natural language.
- **Intent**: The purpose or goal behind a user's query.
- **Synonym**: A word or phrase that means exactly or nearly the same as another word or phrase in the same language.

## Author

* [Arnab Bera]( https://www.linkedin.com/in/arnabbera-tech/ )
"# FAQ_Chatbot" 
