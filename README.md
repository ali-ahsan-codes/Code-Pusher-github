<div align="center">

# 🚀 Local GitHub Project & Repository Sync Manager

**A High-Performance, Private, and Modern Local Web Application for Automated GitHub Uploads**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Git](https://img.shields.io/badge/Git-Engine-F05032?style=for-the-badge&logo=git&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)

<p align="center">
  <b>Bypasses GitHub API Constraints</b> &bull; 
  <b>Automated Markdown Directory Tree</b> &bull; 
  <b>Subfolder Targeted Pushes</b>
</p>

---

</div>

## 📌 Executive Overview

**Local GitHub Sync Manager** is a lightweight, local-first web interface engineered to streamline uploading zip archives and bulk project assets directly to targeted subdirectories inside GitHub repositories.

By employing a native **Git Clone & Push Backend Architecture**, this tool completely bypasses API rate limits, file size caps, and HTTP 404 pathing errors often associated with direct API endpoints.

---

## 🔥 Highlighted Features

- ⚡ **Direct Zip Extraction & Push**: Seamlessly handles large archives (e.g., 1000+ files) via multipart streams.
- 🌳 **Auto `list.md` Generator**: Automatically scans project contents and generates an interactive, clean directory tree in `list.md` prior to committing.
- 🎯 **Target Folder URL Parsing**: Paste any deep folder link (`https://github.com/owner/repo/tree/main/subfolder`) and let the URL engine auto-decode paths and branch details.
- 🔒 **Zero-Leak Local Credentials**: Authenticates securely using a local `cred.json` file. No personal tokens are ever stored or exposed on external servers.
- 🛠️ **Windows-Safe Git Engine**: Built-in `rmtree` exception handlers prevent file-locking permissions issues (`WinError 5`) on Windows environments.

---

## 🛠️ Tech Stack & Architecture

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Backend** | **FastAPI + Uvicorn** | Asynchronous local Python server executing native `git` CLI operations. |
| **Frontend** | **TailwindCSS + JSZip** | Dark-mode UI with live status log monitoring. |
| **Auth** | **Personal Access Token (PAT)** | Authenticates `git clone` via ephemeral credential mapping. |
| **Engine** | **Native Git Engine** | Standard `git clone`, `git add`, `git commit`, and `git push` workflow. |

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/ali-ahsan-codes/GitHub-Upload-Manager.git](https://github.com/ali-ahsan-codes/GitHub-Upload-Manager.git)
cd GitHub-Upload-Manager
