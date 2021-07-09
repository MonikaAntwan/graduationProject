from flask import Flask
from flask_restful import Api, Resource,fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Site(db.Model):
	__tablename__='Site'
	name = db.Column(db.String(100), primary_key=True, nullable=False)
	description= db.Column(db.String(3000), nullable=False)
	town=db.Column(db.String(30))
	gov=db.Column(db.String(30), nullable=False)
	workingHours=db.Column(db.String(100))
	category=db.Column(db.String(30), nullable=False)
	picture=db.Column(db.String(100),nullable=False)
	lat=db.Column(db.Float,nullable=False)
	long= db.Column(db.Float, nullable=False)

class Customer(db.Model):
	__tablename__ = 'Customer'
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	firstName=db.Column(db.String(30),nullable=False)
	lastName = db.Column(db.String(30), nullable=False)
	email=db.Column(db.String(30), nullable=False)
	password=db.Column(db.String(30),nullable=False)


class Destinations(db.Model):
	__tablename__ = 'Destinations'
	customerID= db.Column(db.Integer, ForeignKey('Customer.id'), nullable=False)
	destinationName = db.Column(db.String(100), ForeignKey('Site.name'), nullable=False)
	destinationPicture = db.Column(db.String(100), ForeignKey('Site.picture'), nullable=False)
	destinationLat = db.Column(db.Float,ForeignKey('Site.lat'), nullable=False)
	destinationLong = db.Column(db.Float,ForeignKey('Site.long'), nullable=False)
	__table_args__=(db.PrimaryKeyConstraint(customerID,destinationName,),)

#db.create_all()

resource_fields = {
	'name': fields.String,
	'description': fields.String,
	'town': fields.String,
	'gov': fields.String,
    'workingHours': fields.String,
    'category': fields.String,
	'picture':fields.String,
    'lat':fields.Float,
    'long':fields.Float,
}

resource_fields_customer={
	'id':fields.Integer,
	'firstName':fields.String,
	'lastName':fields.String,
	'email':fields.String,
	'password':fields.String
}

resource_fields_destinations={
	'customerID': fields.Integer,
    'destinationName':fields.String,
	'destinationPicture':fields.String,
	'destinationLat': fields.Float,
	'destinationLong': fields.Float,
}

engine = create_engine('sqlite:///database.db')
db.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class SearchByCategory(Resource):
	@marshal_with(resource_fields)
	def get(self, chosenCategory,chosenPage):
		results=Site.query.filter(Site.category==chosenCategory).paginate(chosenPage,7,False).items
		return results

api.add_resource(SearchByCategory, "/category/<string:chosenCategory>/<int:chosenPage>")

class SearchByLocation(Resource):
	@marshal_with(resource_fields)
	def get(self, chosenLocation,chosenPage):
		results = Site.query.filter((Site.gov == chosenLocation) | (Site.town==chosenLocation)).paginate(chosenPage, 7, False).items
		return results

api.add_resource(SearchByLocation, "/location/<string:chosenLocation>/<int:chosenPage>")

class LogIn(Resource):
	@marshal_with(resource_fields_customer)
	def get(self, chosenEmail,chosenPassword):
		result=Customer.query.filter_by(email=chosenEmail,password=chosenPassword).first()
		print(result)


		return result

api.add_resource(LogIn, "/login/<string:chosenEmail>/<string:chosenPassword>")

class DestinationsList(Resource):
	@marshal_with(resource_fields_destinations)
	def get(self, chosenID,chosenPage):
		results = Destinations.query.filter(Destinations.customerID==chosenID).paginate(chosenPage,3,False).items
		return results

api.add_resource(DestinationsList, "/destinationList/<int:chosenID>/<int:chosenPage>")

class SignUp(Resource):
	@marshal_with(resource_fields_customer)
	def put(self,chosenFirstName,chosenLastName,chosenEmail,chosenPassword):
		result = Customer.query.filter_by(email=chosenEmail).first()
		if result:
			newCustomer = Customer(firstName=None, lastName=None, email=None,password=None)
		else:
			newCustomer = Customer(firstName=chosenFirstName, lastName=chosenLastName, email=chosenEmail,password=chosenPassword)
			db.session.add(newCustomer)
			db.session.commit()
		return newCustomer

api.add_resource(SignUp, "/customer/<string:chosenFirstName>/<string:chosenLastName>/<string:chosenEmail>/<string:chosenPassword>")

class AddDestination(Resource):
	@marshal_with(resource_fields_destinations)
	def put(self,chosenId,chosenDestination):
		foundSite= Site.query.filter(Site.name == chosenDestination).first()
		results=Destinations.query.filter_by(customerID= chosenId,destinationName= chosenDestination,destinationPicture=foundSite.picture).first()
		if(results):
			db.session.delete(results)
		else:
			newDestination= Destinations(customerID=chosenId, destinationName=chosenDestination,destinationPicture=foundSite.picture,destinationLat=foundSite.lat,destinationLong=foundSite.long)
			db.session.add(newDestination)
		db.session.commit()


api.add_resource(AddDestination, "/addDestination/<int:chosenId>/<string:chosenDestination>")

class DeleteDestination(Resource):
	@marshal_with(resource_fields_destinations)
	def delete(self,chosenId,chosenDestination):
		results = Destinations.query.filter_by(customerID= chosenId,destinationName= chosenDestination).first()
		db.session.delete(results)
		db.session.commit()


api.add_resource(DeleteDestination, "/deleteDestination/<int:chosenId>/<string:chosenDestination>")

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000,debug=True)