# Instagram_and_facebook_login_page

1.Instagram and Facebook login page using HTML and CSS.

Flask conversion
- App entry: `app.py` with routes `/`, `/login` (POST), `/signup`, `/wrong-password`, `/forget`, `/facebook-login`.
- Templates live in `templates/`, static assets in `static/`.
- Database: SQLite via SQLAlchemy. A `User` model stores usernames and password hashes.

Local setup
- Python 3.10+
- Windows PowerShell
  - `py -m venv .venv`
  - `.\.venv\Scripts\Activate`
  - `pip install -r requirements.txt`
  - `python app.py`

Environment variables (optional)
- `SECRET_KEY` – Flask secret key
- `DATABASE_URL` – SQLAlchemy database URL (defaults to `sqlite:///app.db`)

Deploy (Heroku or Render)
- Procfile included: `web: gunicorn -w 2 -b 0.0.0.0:$PORT "app:create_app()"`

2.The login.html and login.css is the login page for Instagram.

3.wrong_password.html and wrong_password.css is also for Instagram webpage.

4.and also forget.css and forget.html is for Instagram page.

5.This is Screenshot of Instagram Login Page.
![Screenshot (6)](https://user-images.githubusercontent.com/112002659/209445571-80832943-a49c-4891-a9bf-eb6ced619dec.png)

![Screenshot (7)](https://user-images.githubusercontent.com/112002659/209445575-07e7d74a-c899-48f5-9a7e-5842759e5a75.png)

6.This is Screenshot of Instagram Login Page if a user try to enter login id and password this message will pop up.
![Screenshot (8)](https://user-images.githubusercontent.com/112002659/209445580-0745ee30-6293-438f-8865-4c9e69dff427.png)

7.When a user try to forget password or try to signup.
![Screenshot (9)](https://user-images.githubusercontent.com/112002659/209445652-7d4a5a5d-fa24-4e41-a0ff-30217f7a5b91.png)
![Screenshot (10)](https://user-images.githubusercontent.com/112002659/209445665-ef8cc946-0f21-4335-914f-c9fa65bf9720.png)

8. When user try to login with facebook
![Screenshot (11)](https://user-images.githubusercontent.com/112002659/209445670-e63aa4dd-e135-44c7-8a52-8ca5f62d834e.png)


This is only for Educational Purpose only.
