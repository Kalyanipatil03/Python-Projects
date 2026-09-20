<<<<<<< HEAD
# Password Vault — Python Flask

A course-friendly web-based password vault built with Python, Flask, SQLite and Fernet encryption.

## Features
- First-run master-password setup
- Master-password protected login
- Encrypted vault fields (title, username, password, website and notes)
- Add, edit and delete vault entries
- Password generator
- Responsive web UI
- SQLite database created automatically

## Important security note
This is an educational project, not a production password manager. The master password is not stored directly in the database; it is used to derive an encryption key. For a real-world password manager, use a mature audited architecture, stronger account/session controls, CSRF protection, secure secret management, rate limiting, HTTPS, secure key handling and security testing.

## Requirements
- Python 3.10+ (Python 3.14 should work)
- VS Code

## Windows setup

Open the project folder in VS Code.

### 1. Create a virtual environment
```powershell
py -m venv venv
```

### 2. Activate it
PowerShell:
```powershell
.env\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.env\Scripts\Activate.ps1
```

Command Prompt:
```cmd
venv\Scriptsctivate
```

### 3. Install dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run
```powershell
python app.py
```

You should see a local address similar to:
`http://127.0.0.1:5000`

Open that address in Chrome/Edge.

## First use
1. Open the app.
2. Create a master password (8+ characters).
3. Log in.
4. Click **Add Password**.
5. Add a sample account.
6. Use the **Generate** button if you want a random password.
7. Edit or delete entries from the dashboard.

## Database
`vault.db` is created automatically in the project directory on first run.

If you forget the master password, this educational version cannot recover the encrypted vault. Delete `vault.db` and start again if you are only experimenting.

## VS Code
Recommended extensions:
- Python (Microsoft)
- Pylance (Microsoft)

## Project structure
```text
PasswordVault/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── setup.html
│   ├── login.html
│   ├── dashboard.html
│   └── entry_form.html
└── static/
    └── style.css
```
=======
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
>>>>>>> 8f0f9a48378ff55188876a2a7bc0edabb309b313
