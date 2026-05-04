# 🏥 LabaidGPT

> **Complete AI-powered healthcare platform with advanced medical analysis, cancer screening, and prescription verification**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Groq AI](https://img.shields.io/badge/Groq-AI%20Powered-green.svg)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

AI Medical Assistant Pro is a comprehensive healthcare AI platform that combines multiple AI models and technologies to provide intelligent medical assistance. The system offers specialized medical analysis, multi-language support (English & Bengali), and advanced features for healthcare professionals and patients.

## 🎯 Key Features

### 🧠 **AI Brain Analysis**
- Medical image analysis using Groq's Llama Vision models
- Support for X-rays, MRIs, CT scans, and other medical imaging
- Multi-language image analysis (English/Bengali)
- Advanced image processing and interpretation

### 🎯 **Cancer Risk Assessment**
- Intelligent cancer screening questionnaire
- Age and gender-specific risk evaluation
- AI-powered reasoning engine
- Dynamic risk assessment with specialized consultation

### 📋 **Prescription Analysis**
- OCR-based prescription text extraction
- Multi-OCR engine support (EasyOCR, Tesseract)
- AI-powered medication interaction checking
- Drug safety analysis and recommendations

### 🎤 **Voice Processing**
- **Speech-to-Text**: Convert patient voice recordings to text
- **Text-to-Speech**: Audio output for medical reports
- Multi-language support (English, Bengali, Spanish, French, German)
- Cloud-optimized voice processing with Groq Whisper

### 💬 **Enhanced Medical Consultation**
- Intelligent chatbot with medical expertise
- Consultation history tracking
- Multi-language support
- Context-aware medical conversations

### 👁️ **Medical Imaging Analysis**
- **Ophthalmology**: Retinal imaging, eye disease diagnosis
- **Cardiology**: Cardiac imaging, heart condition analysis
- **Orthopedics**: Bone and joint analysis
- **General Medicine**: Comprehensive medical imaging review

## 🏗️ Architecture

### Core Components

```
AI Medical Assistant Pro/
├── 🧠 Brain Module (brain_of_the_doctor.py)
├── 🎤 Voice Input (voice_of_the_patient.py)
├── 🔊 Voice Output (voice_of_the_doctor.py)
├── 💬 Enhanced Chat (enhanced_text_chat.py)
├── 🏥 Medical Imaging (medical_imaging_analysis.py)
├── 🎯 Cancer Consultation (enhanced_cancer_consultation_system.py)
├── 📋 Prescription Analysis (prescription_analysis.py)
├── 🎯 Cancer Reasoning (cancer_reasoning_engine.py)
└── 🖥️ Main App (complete_functional_streamlit_medical_app.py)
```

### AI Models & APIs

- **Groq Llama 4 Scout**: Vision-capable model for medical image analysis
- **Groq Llama 4 Maverick**: Advanced reasoning for medical consultations
- **Groq Whisper**: Speech-to-text processing
- **ElevenLabs** (Optional): Enhanced text-to-speech
- **Google Text-to-Speech**: Fallback TTS with Bengali support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API Key (required)
- ElevenLabs API Key (optional, for enhanced TTS)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-medical-assistant-pro.git
cd ai-medical-assistant-pro
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
echo "ELEVENLABS_API_KEY=your_elevenlabs_key_here" >> .env  # Optional
```

4. **Run the application**
```bash
streamlit run complete_functional_streamlit_medical_app.py
```

### Dependencies (requirements.txt)

```txt
streamlit>=1.28.0
groq>=0.4.0
pillow>=10.0.0
gtts>=2.3.0
easyocr>=1.7.0
python-dotenv>=1.0.0
elevenlabs>=0.2.0
pytesseract>=0.3.10
tempfile
logging
base64
datetime
json
re
uuid
typing
```

## 🔧 Configuration

### API Keys Setup

1. **Groq API Key** (Required)
   - Sign up at [Groq Console](https://console.groq.com)
   - Create API key
   - Set `GROQ_API_KEY` environment variable

2. **ElevenLabs API Key** (Optional)
   - Sign up at [ElevenLabs](https://elevenlabs.io)
   - Create API key for enhanced TTS
   - Set `ELEVENLABS_API_KEY` environment variable

### Module Configuration

Each module can be independently configured:

- **Voice Processing**: Supports multiple audio formats (WAV, MP3, OGG, FLAC, M4A)
- **Image Analysis**: Supports JPG, JPEG, PNG, BMP, TIFF formats
- **Language Support**: English (`en`) and Bengali (`bn`) with extensible framework
- **OCR Engines**: Multiple OCR backends with automatic fallback

## 💡 Usage Examples

### Medical Image Analysis
```python
from brain_of_the_doctor import analyze_image_with_query, encode_image

# Analyze medical image
encoded_image = encode_image("path/to/medical_image.jpg")
result = analyze_image_with_query(
    query="Please analyze this chest X-ray",
    encoded_image=encoded_image,
    language="en"
)
print(result)
```

### Voice Transcription
```python
from voice_of_the_patient import transcribe_with_groq

# Transcribe patient audio
transcription = transcribe_with_groq(
    audio_filepath="patient_recording.wav",
    language="en"
)
print(transcription)
```

### Cancer Risk Assessment
```python
from cancer_reasoning_engine import CancerReasoningEngine

# Initialize cancer screening
engine = CancerReasoningEngine()
risk_assessment = engine.assess_risk(patient_data)
```

## 🌍 Multi-Language Support

The platform supports comprehensive multi-language functionality:

- **English**: Full feature support
- **Bengali**: Native language support with specialized medical terminology
- **Extensible**: Framework for adding additional languages

### Language Features
- UI translations
- Medical terminology localization  
- Voice processing in multiple languages
- Culturally appropriate medical guidance

## 🏥 Medical Specialties

### Supported Medical Imaging Analysis

1. **Ophthalmology**
   - Retinal photography analysis
   - OCT scan interpretation
   - Diabetic retinopathy screening
   - Macular degeneration assessment

2. **Cardiology**
   - Echocardiogram analysis
   - Angiogram interpretation
   - Cardiac CT evaluation
   - Heart condition assessment

3. **Orthopedics**
   - X-ray bone analysis
   - Joint assessment
   - Fracture detection
   - Orthopedic condition evaluation

4. **General Medicine**
   - Comprehensive imaging review
   - Multi-system analysis
   - Specialist referral recommendations

## 🔒 Security & Privacy

- **Data Privacy**: All processing occurs locally or through secure APIs
- **No Data Storage**: Images and audio are processed temporarily
- **HIPAA Considerations**: Designed with healthcare privacy standards in mind
- **API Security**: Secure API key management and encrypted communications

## ⚠️ Medical Disclaimer

> **Important**: This AI Medical Assistant is designed as a preliminary screening and educational tool. It is NOT intended to replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions. In medical emergencies, contact emergency services immediately.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where applicable
- Include comprehensive docstrings
- Add unit tests for new features

## 🐛 Troubleshooting

### Common Issues

**Module Import Errors**
```bash
# Ensure all Python files are in the same directory
# Check for typos in module names
# Verify all dependencies are installed
pip install -r requirements.txt
```

**API Issues**
```bash
# Verify API keys are set correctly
echo $GROQ_API_KEY
# Check internet connection and API status
```

**Voice Processing Issues**
- Ensure audio files are under 25MB
- Support formats: WAV, MP3, OGG, FLAC, M4A
- Verify Groq API key is configured

**OCR Issues**
- Use clear, high-quality images
- Ensure good lighting and contrast
- Try different image formats (JPG, PNG)

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB for dependencies and models
- **Internet**: Required for API access

### Recommended Setup
- **RAM**: 16GB for optimal performance
- **CPU**: Multi-core processor for faster processing
- **GPU**: Optional, for enhanced OCR performance

## 📈 Performance Metrics

- **Image Analysis**: ~2-5 seconds per image
- **Voice Transcription**: Real-time processing
- **Cancer Assessment**: ~30-60 seconds for complete evaluation
- **Prescription Analysis**: ~3-10 seconds per prescription

## 🔄 Updates & Roadmap

### Recent Updates (v1.0)
- ✅ Multi-language support (English/Bengali)
- ✅ Advanced cancer screening system
- ✅ Prescription OCR and analysis
- ✅ Enhanced medical imaging capabilities
- ✅ Voice processing improvements

### Upcoming Features
- 🔄 Additional language support
- 🔄 Mobile app development
- 🔄 Integration with medical databases
- 🔄 Advanced ML model training
- 🔄 Telemedicine features

## 📞 Support

- **Documentation**: [Wiki](https://github.com/yourusername/ai-medical-assistant-pro/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-medical-assistant-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-medical-assistant-pro/discussions)
- **Email**: support@medicalai.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing advanced AI models and APIs
- **Streamlit**: For the excellent web framework
- **ElevenLabs**: For high-quality text-to-speech services
- **Medical Community**: For guidance on medical AI applications
- **Open Source Community**: For various libraries and tools

## 📸 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)

### Medical Image Analysis
![Image Analysis](screenshots/image_analysis.png)

### Cancer Consultation
![Cancer Consultation](screenshots/cancer_consultation.png)

### Voice Processing
![Voice Features](screenshots/voice_processing.png)

---

<div align="center">

**Built with ❤️ for Healthcare**

[🌐 Website](https://medicalai.com) • [📧 Contact](mailto:contact@medicalai.com) • [💬 Discord](https://discord.gg/medicalai)

</div>
