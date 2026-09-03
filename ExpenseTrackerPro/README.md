# Expense Tracker Pro — Browser Application

A complete local browser-based personal finance project inspired by the reference videos.

## Stack
- Python 3.10+
- SQLite database
- HTML5, CSS3, JavaScript
- Python standard library only — **no Flask and no external packages**

## Features
- Landing page
- Register / Login / Logout
- Secure password hashing with PBKDF2-HMAC-SHA256
- Dashboard: income, expenses, savings, budget, recent transactions
- Add income / expense
- Transaction search and filters
- Delete transactions
- Category spending visualization
- Monthly analytics
- Category budgets and remaining budget
- CSV export
- Responsive browser UI

## Run on Windows
1. Install Python 3.10+ and make sure `python --version` works.
2. Open Command Prompt in this folder.
3. Run: `python app.py`
4. Open: **http://127.0.0.1:8000** in Chrome/Edge.
5. Create an account and start using it.

Or double-click `run.bat`.

## Database
`expense_tracker.db` is created automatically in the project folder. Do not edit it manually while the app is running.

## Presentation flow
Landing → Create Account → Login → Dashboard → Add Expense/Income → Transactions → Analytics → Budget → Export → Logout.
