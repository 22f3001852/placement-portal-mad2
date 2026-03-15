# Placement Drive Management System

This is a Flask and Vue based web application developed for the App Dev II project.  
The system helps manage campus placement drives by allowing students to apply for job opportunities, companies to create and manage placement drives, and administrators to monitor and control the platform.

---

## Prerequisites

Make sure the following are installed on your system:

- Python 3.8+
- Git
- Node.js (v16 or above recommended)
- npm
- A code editor like VS Code

You can verify installations using:

```bash
python --version
node -v
npm -v
git --version
```

---

## Setup Instructions

Follow the steps below to clone and run this project on your local system.

---

## 1. Clone the Repository

Open Git Bash or Command Prompt and run:

```bash
git clone https://github.com/YOUR-USERNAME/placement-drive-management-system.git
cd placement-drive-management-system
```

---

# A. Backend Setup (Flask)

### 1. Create and Activate a Virtual Environment

Run the following commands inside the backend directory:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
```

If you are using Linux/Mac:

```bash
source venv/bin/activate
```

You should see `(venv)` in the terminal indicating that the virtual environment is active.

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the Application

```bash
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000/
```

The Flask backend server should now be running.

---

# B. Frontend Setup (Vue + Vite)

This project uses Vue 3 with Vite for the frontend.

### 1. Navigate to the frontend directory

```bash
cd frontend
```

---

### 2. Install Dependencies

```bash
npm install
```

---

### 3. Install Axios (for API calls)

```bash
npm install axios
```

---

### 4. Run the Development Server

```bash
npm run dev
```

The Vue application will run on:

```
http://localhost:5173
```

---

# C. Advanced Backend – Async Jobs Setup

The project uses **Celery and Redis** for background tasks such as sending reminders and generating reports.

---

## Prerequisites

Ensure that you have the following installed:

- WSL with Ubuntu (recommended for Windows users)
- Python3 and pip
- Redis
- Celery

---

## 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

---

## 2. Install Backend Dependencies

Navigate to the backend folder:

```bash
cd backend
pip install -r requirements.txt
```

---

## 3. Start Redis Server

Start the Redis service:

```bash
sudo service redis-server start
```

Check if Redis is running:

```bash
redis-cli ping
```

Expected output:

```
PONG
```

---

## 4. Start Celery Worker

```bash
celery -A app.celery worker --loglevel=info
```

---

## 5. Start Celery Beat Scheduler

```bash
celery -A app.celery beat --loglevel=info
```

---

## 6. Run Flask Application

```bash
python app.py
```

---

## 7. Run Vue Frontend Server

Inside the frontend folder:

```bash
npm run dev
```

---

## Testing the Setup

After running all services:

Frontend:
```
http://localhost:5173
```

Backend:
```
http://127.0.0.1:5000
```

Check Celery logs in the terminal to ensure background tasks are running correctly.

---

## Stopping Services

To stop Redis and Celery services:

```bash
sudo service redis-server stop
pkill -f "celery"
```

---

## Features

- User authentication and role-based access (Admin, Student, Company)
- Placement drive creation and management
- Student job application system
- Admin dashboard for monitoring the platform
- Background jobs using Celery
- Responsive frontend using Vue.js

---

## Technology Stack

Backend:
- Flask
- SQLAlchemy
- SQLite
- Celery
- Redis

Frontend:
- Vue.js
- Vite
- Axios
- Bootstrap

---

## Conclusion

Following these steps will allow you to successfully run the Placement Drive Management System locally.  
The system integrates Flask backend, Vue frontend, Celery background jobs, and Redis message broker to provide a complete placement management platform.

---

## Note

This README.md may be updated as the project evolves. Please check periodically for new setup instructions, features, and improvements.