# P12 MySQL Console CRM

A simple, console-based Customer Relationship Management (CRM) application built as a study project for a fictional company called **Epic Events**.

This repository implements a fully functional CLI CRM using Python and MySQL. It supports user authentication, client and contract management, and interactive menus — ideal for learning how to build a real-world database-backed application.

---

## 📋 Features

- **User authentication** with JWT tokens
- **Client management** (create, view, search, update)
- **Contract management** (create, sign, filter, list)
- Intuitive **console menus** for user interaction
- Works with MySQL database backend

---

## 🚀 Getting Started

### 🛠 Prerequisites

Before running the application, make sure you have:

- Python 3.8+ installed
- MySQL 8.x installed
- A MySQL user with permission to create and use databases

---

## Database Setup

This project uses MySQL. A schema-only SQL dump is provided so you can create the required tables locally.

### Prerequisites

- MySQL 8.x installed

- Access to a MySQL user with permission to create tables

1. Create a database

Log into MySQL:

```
mysql -u your_user -p
```

Then create the database:

```
CREATE DATABASE epicevents;
EXIT;
```

2. Import the schema

From your system terminal (not inside mysql>), run:

```
mysql -u your_user -p epicevents < schema_backup.sql
```

You will be prompted for your MySQL password.

This will create all required tables, indexes, and constraints without importing any data.

3. Verify the tables

Log back into MySQL:

```
mysql -u your_user -p epicevents
```

Then run:

```
SHOW TABLES;
```

You should see the full list of tables used by the application.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/Dakimen/P12_MySQL_console_CRM.git
cd P12_MySQL_console_CRM
```

2. Create and activate a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Create your own config.py

This project uses services that require user authentication and sensitive data, not included in this repository.

Create a config.py file at the project root, containing variables:

```sh
PASSWORD  # password used to access your MySQL databases.
JWT_SECRET_KEY  # JWT secret key used to generate your tokens.
JWT_ALGORITHM  # Algorithm used to encode your JWT tokens
DB_HOST  # Database hosting
DB_USER  # User used to access your MySQL database
DATABASE  # Should contain database name
DSN  # Sentry-supplied DSN
```

## How to use

Run the main application:

```sh
python main.py
```

You will be guided through login, menus, and CRM workflows directly in your terminal.

## Study project

This repository was developed as a study project implementing a functional CLI CRM system for a fictional events company called Epic Events.
