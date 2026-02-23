# 🌐 FreshMinds

FreshMinds is a scalable social networking web application built using Django.  
It supports multi-role user profiles, post engagement features, and an interactive admin analytics interface designed using AdminLTE.

The goal of this project is to explore scalable backend design, optimized database queries, and user interaction systems in modern web platforms.

---

## 🚀 Live Demo
(Deploy link here)

---

## 📌 Key Features

### 👤 User System
- Secure authentication & authorization
- Custom profile types:
  - Organization
  - Member
  - Agency
- Profile search & discovery

### 📝 Social Interaction
- Create posts with images & descriptions
- Like system with dynamic counters
- Comment system with owner-level delete permissions
- Popup modal post viewer

### 📊 Admin & Analytics
- Custom Django Admin using AdminLTE
- DataTables-based reporting interface
- Export-ready structure for Excel/PDF reporting

---

## 🧠 Research Motivation

This project explores:

- Optimizing Django ORM queries for scalable social systems
- Efficient follower/post recommendation strategies
- Admin analytics performance improvements
- Database indexing strategies in MySQL

These ideas can be extended into academic research papers.

---

## 🛠️ Tech Stack

Backend: Django  
Frontend: HTML5, CSS3, JavaScript  
Database: MySQL  
Admin UI: AdminLTE  
Libraries: jQuery, DataTables, FontAwesome  

---

## 🏗️ System Architecture

(Add diagram here)

Example modules:
- Users
- Posts
- Comments
- Analytics
- Employee Management

---

## ⚡ Installation

```bash
git clone https://github.com/Mitu194/FreshMinds
cd FreshMinds
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
