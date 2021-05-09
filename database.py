from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mainClass import db, Site,Customer,Destinations

engine = create_engine('sqlite:///database.db')
db.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

site1=Site(name="Temple of Horus",
           description="The Ptolemaic Temple at Edfu (105Km/65 miles north of Aswan), built from 257—337 BC, is the best preserved and one of the finest in Egypt. Built in classic pharaonic style, it gives a clear idea of the appearance and purpose of an Egyptian Temple, and explanations are inscribed on the walls. The site was chosen because the falcon-headed God Horus fought here with Seth for power over the world. The temple is dedicated to Horus, the avenging son of Isis and Osiris. With its roof intact, it is also one of the most atmospheric of ancient buildings.Two hundred years ago the temple was buried by sand, rubble and part of the village of Edfu, which had spread over the roof. Excavation was begun by Auguste Mariette in the mid-19th century. Today the temple is entered via a long row of shops selling tourist tat, and a new visitors centre that houses the ticket office, clean toilets, a cafeteria and a room for showing a 15-minute film on the history of the temple in English.",
           town="Edfu",gov="Aswan",workingHours="8:00 AM – 5:00 PM",category="Historical",picture="pictures/TempleofHorus.jpg")
site2=Site(name="Na’ama Bay",
           description="The epicenter of Sharm El Sheikh’s resort life, Na’ama Bay is fringed by white-sand beach and swaying palm trees. The natural bay is considered as the main hub for tourists in the city. It’s famous for its cafes, restaurants, luxurious hotels, and bazaars. If you are looking for a fun, relaxed day on the beach, sunbathing, then Naama Bay is what you’re looking for.",
           town="Sharm El Sheikh",gov="South Sinai",workingHours="24/7",category="Entertainment",picture="pictures/Na’amaBay.jpg")
site3=Site(name="Abu Simbel Temple",
           description="This site, Abu Simbel Temples, south of Aswan along Lake Nasser’s shore is Egypt's second most visited touristic site. The two temples which comprise the site were created by the Egyptian king Ramses II (reigned 1279–13 BCE) hence was also known as the Temple of Ramses II or Ramesses II. In ancient times the area was at the southern frontier of pharaonic Egypt, facing Nubia. In the 1960s the temple complex was dismantled and rebuilt on a higher hill to make way for the Aswan High Dam. As a result it was carved out of a sandstone cliff on the west bank of the Nile.Abu Simbel was rediscovered in 1813 by Swiss explorer John Lewis Burckhardt. The temples had long been forgotten and the sands of the desert sands had covered all but the tops of the heads of the huge statues in front of their entrances. Since 1909 when the sand was finally cleared away, these twin temples have become the most famous site in Egypt’s south.",
           gov="Aswan",workingHours="5:00 AM – 6:00PM",category="Historical",picture="pictures/AbuSimbelTemple.jpg")


session.add(site1)
session.add(site2)
session.add(site3)

customer1=Customer(firstName="ayah",lastName="Soffar",email="ayah@gmail.com",password="monika")
customer2=Customer(firstName="maii",lastName="Harfoush",email="mayouya@gmail.com",password="maiii")

session.add(customer1)
session.add(customer2)

destination1=Destinations(customerID=2,destinationName="Abu Simbel Temple")
destination2=Destinations(customerID=2,destinationName="Na’ama Bay")
destination3=Destinations(customerID=1,destinationName="Abu Simbel Temple")

session.add(destination1)
session.add(destination2)
session.add(destination3)
session.commit()

sites= session.query(Site).all()
for site in sites:
    print(site.name)
    print(site.description)
    print(site.town)
    print(site.gov)
    print(site.workingHours)
    print(site.category)
    print(site.picture)
