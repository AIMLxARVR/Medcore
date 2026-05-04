# run_streamlit.py - Launch script for the Streamlit AI Doctor App
import os
import subprocess
import sys

def main():
    """
    Launch the Streamlit AI Doctor application
    """
    print("🏥 Starting AI Doctor with Streamlit...")
    print("=" * 50)
    
    # Check if required environment variables are set
    required_env_vars = ["GROQ_API_KEY"]
    missing_vars = []
    
    for var in required_env_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these environment variables before running the app.")
        print("You can create a .env file with your API keys.")
        return
    
    print("✅ Environment variables check passed")
    print("🚀 Launching Streamlit app...")
    print("📱 The app will open in your default web browser")
    print("🔗 Default URL: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AI Doctor app...")
        print("👋 Thank you for using AI Doctor!")
    except Exception as e:
        print(f"❌ Error starting the app: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main()