# 🏆 CTF Training Platform

**Status**: All core directories (`challenges/`, `users/`, `templates/`, `ctf_platform/`) and files (`manage.py`, `.gitignore`) are present. The initial commit "Initial commit: CTF Training Platform" is live.

## 🚀 Features

- **Dual Authentication**: Login via Username or Email.
- **Dynamic Challenges**: Categorized tasks with point scaling.
- **Live Leaderboard**: Real-time ranking of users.
- **Challenge Submission**: Users can author and submit challenges.
- **Admin Review**: Full-featured admin dashboard to review and approve/reject submissions.
- **Mobile Responsive**: Fully responsive UI using Bootstrap 5.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (Development) / Postgres (Production ready)
- **Deployment**: Configured for Render & GitHub Actions

## 💻 Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EyaminH/ctf_platform.git
   cd ctf_platform
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## 🚢 Deployment

This platform is configured for deployment on **Vercel**.

1. Install Vercel CLI: `npm i -g vercel`
2. Deploy: `vercel`

Alternatively, connect your GitHub repository to Vercel for automatic deployments.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
