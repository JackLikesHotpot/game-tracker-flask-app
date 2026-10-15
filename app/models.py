from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
  __tablename__ = 'users'

  user_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

  profile = db.relationship(
      'UserProfile', backref='user', uselist=False, cascade='all, delete-orphan'
  )

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
  __tablename__ = 'user_profiles'

  profile_id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(
      db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True
  )
  username = db.Column(db.String(255), unique=True, nullable=False)
  bio = db.Column(db.Text, nullable=True)
  avatar_url = db.Column(db.String(255), nullable=True)