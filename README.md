# Upile Monorepo

This repository contains both the **frontend** (Next.js/React) and **backend** (Django/Python) for the Upile LostLocate platform.

## Project Overview
Upile LostLocate is a platform for managing and locating missing persons, unidentified bodies, and related data. It provides separate dashboards for public users, police, mortuary staff, and administrators.

---

## Directory Structure

```
Upile-Frontend/
├── backend/         # Django backend (API, database, admin, etc.)
├── lostlocate/      # Next.js frontend (UI, client portal, dashboards)
├── ...              # Other frontend files
└── README.md        # This file
```

---

## Backend Setup (Django)

1. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
4. **Run the backend server:**
   ```bash
   python manage.py runserver
   ```
   By default, the backend runs at `http://127.0.0.1:8000/`.

---

## Frontend Setup (Next.js)

1. **Navigate to the frontend folder:**
   ```bash
   cd lostlocate
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the frontend server:**
   ```bash
   npm run dev
   ```
   By default, the frontend runs at `http://localhost:3000/`.

---

## Connecting Frontend to Backend

- The frontend expects the backend API to be available at a specific URL.
- You can set the API URL in a `.env.local` file in the `lostlocate` folder:
  ```env
  NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/
  ```
- Make sure both servers are running for full functionality.

---

## Example .env.local for Frontend
Create a file named `.env.local` in the `lostlocate` directory:
```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/
```

---

## Contribution
- Fork the repo and create a pull request for any changes.
- Please open issues for bugs or feature requests.

## Contact
- For questions or support, open an issue or contact the repository owner via GitHub.

---

## Notes
- Make sure you have Python and Node.js installed on your system.
- For production deployment, configure environment variables and security settings as needed.
- The backend may require additional setup for email/SMS if using OTP codes.

---

**Happy coding!**
