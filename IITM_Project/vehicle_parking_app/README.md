# 🚗 Vehicle Parking Management System  
A smarter way to manage parking — built with Flask, designed for India.

---

## 👋 Welcome!

Hi! I'm Vineet Kumar, and this is my project for **Modern Application Development I**. If you've ever spent way too long circling for a parking spot (especially in busy Indian cities), you’ll get why I built this. The goal? Help users find spots faster and let admins manage lots better.

---

## 💻 Tech Stack

- **Flask** – Backend and routing  
- **SQLite + SQLAlchemy** – Lightweight but powerful database  
- **HTML + Jinja2 + Bootstrap** – Fast, responsive front-end

---

## 🌐 Indian Context, Real Feel

- Locations: BKC Mumbai, Cyber City Gurgaon, Brigade Road Bangalore, etc.
- Pricing: ₹40–₹120/hour (based on real market rates)  
- Vehicle numbers: Styled like MH01AB1234, KA01MN7890  
- Admin and user flows built around real-world parking behavior

---

## 🚀 How to Run It

1. **Install dependencies:**
2. Set up the database and admin :	python setup.py
3. Launch the app: python app.py
4.Visit: http://localhost:5000

🔐 Test Accounts
Admin Login: admin
Password: admin123

Users:
Register using the UI — sample lots are already there!

📁 Project Structure
vehicle_parking_app/
├── app.py               # Main app logic
├── models.py            # DB models
├── setup.py             # Setup script (DB + admin user)
├── instance/parking.db  # SQLite database
├── static/images/       # logo.jpg, background.jpg
├── templates/           # HTML templates (user/admin)
└── README.md            # This file!

✨ Features to Brag About
Real-time parking spot tracking
Timeline-style user dashboard
Auto cost calculation on release
Mobile-first responsive design
Admin sidebar for easy lot & user management

🧠 What I Learned
Full-stack dev from scratch
Clean code > quick hacks
Real context makes a big difference
Debugging SQLAlchemy isn’t fun, but worth it 😅

🤖 AI Use Transparency(~15%)
Used ChatGPT to guide structure, fix bugs, and polish the UI — but every idea, logic flow, and feature was shaped and understood by me.

☁️ If It Breaks
Database issue? Delete parking.db and run setup.py again and then python app.py
Image not loading? Check /static/images/ has the required files
Import error? Ensure you're in the right folder and Flask is installed

🎓 Final Note
This project started with a simple idea from assignment and turned into something I’m truly proud of. It’s functional, focused, and rooted in real-world use. Thanks for checking it out!

Built with love, logic, and way too much coffee ☕
— Vineet Kumar, 2025