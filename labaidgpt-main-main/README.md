# 🏥 Medic-Assist

> **An AI-powered healthcare platform with advanced medical analysis, cancer screening, and prescription verification.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-red.svg)](https://streamlit.io)
[![Groq AI](https://img.shields.io/badge/Groq-AI%20Powered-green.svg)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

Medic-Assist is a comprehensive healthcare AI platform that combines multiple AI models to provide intelligent medical assistance. The system offers specialized medical analysis, multi-language support (English & Bengali), and advanced features for both healthcare professionals and patients.

## 🎯 Key Features

-   **🧠 Medical Image Analysis**: AI-powered analysis of X-rays, MRIs, and CT scans.
-   **🎯 Cancer Risk Assessment**: Intelligent cancer screening with an AI reasoning engine.
-   **📋 Prescription Analysis**: OCR-based text extraction and AI-powered safety analysis of prescriptions.
-   **🎤 Voice Processing**: Speech-to-text transcription and text-to-speech for medical reports.
-   **💬 AI Doctor Consultation**: An enhanced chat interface with consultation history.

## 🏗️ Architecture

The application is structured into a `src` directory containing distinct modules for each feature:

```
medic-assist/
├── src/
│   ├── brain/         # Medical Image Analysis
│   ├── cancer/        # Cancer Screening & Reasoning
│   ├── chat/          # AI Doctor Consultation
│   ├── imaging/       # Specialized Imaging Analysis
│   ├── prescription/  # Prescription Analysis
│   └── voice/         # Voice Processing (STT & TTS)
├── tests/             # Unit Tests
├── .env.example       # Example environment file
├── app.py             # Main Streamlit application
└── requirements.txt   # Dependencies
```

## 🚀 Quick Start

### Prerequisites

-   Python 3.9 or higher
-   A [Groq API Key](https://console.groq.com/keys)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/medic-assist.git
    cd medic-assist
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    -   Copy the `.env.example` file to a new file named `.env`.
    -   Add your Groq API key to the `.env` file:
        ```env
        GROQ_API_KEY="your_groq_api_key_here"
        ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🧪 Running Tests

This project uses `pytest` for unit testing. The tests ensure the core functionality of each module is working correctly.

To run the tests, execute the following command from the root directory:

```bash
python -m pytest
```

## ⚠️ Medical Disclaimer

> **Important**: Medic-Assist is intended as a preliminary screening and educational tool. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions. In case of a medical emergency, contact your local emergency services immediately.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and open a pull request with your changes.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
