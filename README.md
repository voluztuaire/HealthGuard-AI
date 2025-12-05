# HealthGuard AI

HealthGuard AI is a lightweight, AI-assisted healthcare web application built with Flask.
This project provides face-based authentication, a rule-based health assistant, and several basic medical features designed to help users manage health information more conveniently.

---

## Features

### 1. Face-Based Authentication

Secure login using face detection before granting access to user data.

### 2. AI Health Assistant

A rule-based expert system that asks health-related questions and provides simple guidance based on user input.

### 3. User Profile Management

Users can view and manage their personal information through a clean dashboard interface.

### 4. Doctor Directory

A simple directory displaying available doctors and their details.

### 5. Chat Interface

A lightweight chat page for interacting with the health assistant.

---

## Technology Stack

* Python
* Flask
* OpenCV (for face detection; no pretrained recognition models used)
* SQLite
* HTML Templates (Jinja2)

---

## Project Structure

```
HealthGuard-AI/
├── app.py
├── db_setup.py
├── requirements.txt
└── templates/
    ├── auth.html
    ├── chat.html
    ├── doctors.html
    ├── index.html
    └── profile.html
```

---

## Installation

Clone the repository:

```sh
git clone https://github.com/voluztuaire/HealthGuard-AI.git
cd HealthGuard-AI
```

Install the required packages:

```sh
pip install -r requirements.txt
```

Initialize the local database:

```sh
python db_setup.py
```

Run the application:

```sh
python app.py
```

Open the application in your browser:
  
```
http://127.0.0.1:5000
```
