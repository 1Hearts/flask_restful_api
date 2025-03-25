from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# ✅ 새로운 모델: Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    owner = db.Column(db.String(50), nullable=False)  # 아이템을 소유한 사용자

    def __repr__(self):
        return f'<Item {self.name}>'