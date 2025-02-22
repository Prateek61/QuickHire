# 🌟 QuickHire: Instantly Find Professionals for Short-Term Needs 🚀

## 📌 Table of Contents
- [🌟 QuickHire: Instantly Find Professionals for Short-Term Needs 🚀](#-quickhire-instantly-find-professionals-for-short-term-needs-)
  - [📌 Table of Contents](#-table-of-contents)
  - [📖 Introduction](#-introduction)
  - [🔥 Features](#-features)
  - [📄 Pages](#-pages)
  - [🛠 Tech Stack](#-tech-stack)
  - [🎯 Expected Output](#-expected-output)
  - [⚙️ Installation](#️-installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Set Up Backend](#2-set-up-backend)
    - [3. Initialize Database](#3-initialize-database)
    - [4. Start Backend Server](#4-start-backend-server)
    - [5. Set Up Frontend](#5-set-up-frontend)
  - [📌 Usage](#-usage)
  - [👨‍💻 Contributors](#-contributors)

## 📖 Introduction
QuickHire is designed to provide instant access to skilled professionals with an easy-to-use interface and advanced filtering options. With **reviews, ratings ⭐, and professional portfolios**, clients can make well-informed hiring decisions within seconds!

## 🔥 Features
✅ **User Authentication**: Secure login and registration for both clients and professionals. 🔐  
✅ **Hire Request System**: Clients can send hire requests that professionals can accept or decline.  
✅ **Job Review System**: Users can provide feedback and ratings for completed jobs.  
✅ **Professional Portfolio**: Showcase skills, certifications, and client reviews.  
✅ **Skill Posting Form**: Professionals can easily post and update their skills.  

## 📄 Pages
📝 **Login Page**: Secure login for authenticated access.  
🆕 **Registration Page**: Sign-up for new users.  
🛠 **Professional Skill Submission Form**: List and update skills.  
🌟 **Professional Portfolio Page**: Displays skills, certifications, and reviews.  
🔍 **Service Search Page**: Find professionals easily.  
📊 **Professional Dashboard**: Manage profiles, track requests, and update services.  
🎯 **User Dashboard**: Manage accounts, view requests, and connect with professionals.  

## 🛠 Tech Stack
🚀 **FastAPI**: Lightning-fast backend for APIs.  
🗄 **PostgreSQL**: A powerful relational database.  
🎨 **SvelteKit**: Ultra-fast frontend framework.  
🎭 **SvelteUI**: Stylish UI components for a modern feel.  
💨 **Tailwind CSS**: Utility-first CSS framework for rapid UI development.  
📦 **Docker**: Ensures smooth deployment.  

## 🎯 Expected Output
The QuickHire platform will revolutionize the way professionals and clients connect. 🔗 Professionals can **create profiles**, **list their skills**, **set hourly rates**, and **indicate availability**. Clients can browse, view profiles, initiate hire requests, and track job status. 🌟 **The feedback system ensures credibility and trust among users!**

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Prateek61/QuickHire.git
cd QuickHire
```

### 2. Set Up Backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Create config.json from example
cp config-example.json config.json
# Edit config.json with your database settings
```

### 3. Initialize Database
```bash
# Create database tables
python scripts/create_tables.py

# Seed sample data (optional)
python scripts/seed.py
```

### 4. Start Backend Server
```bash
# Run FastAPI development server
fastapi dev app
# The API will be available at http://localhost:8000
```

### 5. Set Up Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Create .env from example
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev

# The app will be available at http://localhost:3000
```

## 📌 Usage
1️⃣ **Register/Login** to create an account.  
2️⃣ **Browse** available professionals.  
3️⃣ **Send Hire Requests** to professionals.  
4️⃣ **Provide Reviews** after job completion.  

## 👨‍💻 Contributors
🎓 **Prajwal Chaudhary** (THA078BCT028)  
🎓 **Prateek Poudel** (THA078BCT031)  
🎓 **Yubraj Basnet** (THA078BCT047)
