from app.models import db, Hero, Power, HeroPower
import random


db.drop_all()
db.create_all()


powers = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]
for power_data in powers:
    power = Power(name=power_data["name"], description=power_data["description"])
    db.session.add(power)

heroes = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]
for hero_data in heroes:
    hero = Hero(name=hero_data["name"], super_name=hero_data["super_name"])
    db.session.add(hero)


strengths = ["Strong", "Weak", "Average"]
for hero in heroes:
    for _ in range(1, 4):  # Add up to 3 powers for each hero
        power = Power.query.get(random.choice([1, 2, 3, 4]))
        hero_power = HeroPower(hero=hero, power=power, strength=random.choice(strengths))
        db.session.add(hero_power)

db.session.commit()

print("🦸‍♀️ Done seeding!")