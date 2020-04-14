from project import db
from project.models import Plants

db.create_all()

plant1 = Plants('Aloe', 'Spikey, resiliant, strong', 7)
plant2 = Plants('Maple', 'Rescued on Earth Day 2019', 5)
plant3 = Plants('Ducky', 'Rubber Plant', 5)

db.session.add(plant1)
db.session.add(plant2)
db.session.add(plant3)

db.session.commit()
