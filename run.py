from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

credential_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"Using credentials at: {credential_path}")

from app import create_app
print("Starting Flask app...")
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
