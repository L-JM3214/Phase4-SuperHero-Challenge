from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import DateTime

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    powers = db.relationship('Power', secondary='hero_powers', backref='heroes')

    def __repr__(self):
        return f"Hero(id={self.id}, name='{self.name}', super_name='{self.super_name}', created_at='{self.created_at}', updated_at='{self.updated_at}')"

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', cascade='all, delete-orphan'))
    power = db.relationship('Power', backref=db.backref('power_heroes', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"HeroPower(id={self.id}, strength='{self.strength}', hero_id={self.hero_id}, power_id={self.power_id}, created_at='{self.created_at}', updated_at='{self.updated_at}')"

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    heroes = db.relationship('Hero', secondary='hero_powers', backref='powers')

    def __repr__(self):
        return f"Power(id={self.id}, name='{self.name}', description='{self.description}', created_at='{self.created_at}', updated_at='{self.updated_at}')"
