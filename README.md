Git Clone & Push Manager 🚀

A lightweight, local web application built with FastAPI and Tailwind CSS that allows you to easily upload a .zip archive of your project, automatically extracts it into a specific subfolder or root directory of a GitHub repository, generates a clean list.md project structure file, and pushes everything directly to GitHub—all through a clean dark-mode web interface!

✨ Features

🔒 Credential Management: Securely load your GitHub credentials via a local cred.json file.

📁 Smart URL Parsing: Automatically handles GitHub target folder links (including URL-encoded spaces like %20) so files go exactly where you want them without creating duplicate folders.

📦 Direct ZIP Upload: Extract and push compressed archives seamlessly without manual command-line cloning.

📑 Auto-Generated list.md: Scans the project structure and creates a readable Markdown file detailing all nested folders and files for better repository navigation.

⚡ Windows File Lock Safe: Includes robust error handlers to bypass Windows file permission locks ([WinError 5] Access is denied) on .git directories.

🎨 Modern UI: Clean, responsive dark-mode interface built with Tailwind CSS and FontAwesome.

🛠️ Tech Stack

Backend: Python, FastAPI, Uvicorn, Git Subprocess, Zipfile

Frontend: HTML5, Tailwind CSS, JavaScript (Fetch API)

📦 Requirements (requirements.txt)

Create a requirements.txt file in your project directory with the following dependencies:

fastapi==0.110.0
uvicorn==0.28.0
python-multipart==0.0.32


🚀 Installation & Setup

Clone or Download this repository/script:
Ensure you have app.py and requirements.txt in your local project folder.

Install Dependencies:
Open your terminal or command prompt in the project directory and run:

pip install -r requirements.txt


Prepare your cred.json file:
Create a JSON file named cred.json containing your GitHub username and Personal Access Token (PAT):

{
    "username": "your-github-username",
    "token": "your-github-personal-access-token"
}


Run the Application:

python app.py


Open in Browser:
Navigate to http://127.0.0.1:8000 in your web browser.

💡 How to Use

Upload your cred.json file in Step 1.

Paste your target GitHub folder link (e.g., https://github.com/username/repo/tree/main/Data Analysis) in Step 2.

Select your project .zip file in Step 3.

Click "Start Git Push & Generate list.md". The app will do the rest!
