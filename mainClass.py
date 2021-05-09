from flask import Flask
from flask_restful import Api, Resource,abort,fields, marshal_with,reqparse
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
	__table_args__=(db.PrimaryKeyConstraint(customerID,destinationName,),)

#db.create_all()

resource_fields = {
	'name': fields.String,
	'description': fields.String,
	'town': fields.String,
	'gov': fields.String,
    'workingHours': fields.String,
    'category': fields.String,
	'picture':fields.String
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
    'destinationName':fields.String
}

customer_put_args = reqparse.RequestParser()
customer_put_args.add_argument("firstName", type=str, help="First name of the customer is required", required=True)
customer_put_args.add_argument("lastName", type=str, help="Last name of the customer is required", required=True)
customer_put_args.add_argument("email", type=str, help="Email of the customer is required", required=True)
customer_put_args.add_argument("password", type=str, help="Password of the customer is required", required=True)

destinations_put_args = reqparse.RequestParser()
destinations_put_args.add_argument("customerID", type=int, help="ID of customer is required", required=True)
destinations_put_args.add_argument("destinationName", type=str, help="Name of site is required", required=True)


engine = create_engine('sqlite:///database.db')
db.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class SearchByCategory(Resource):
	@marshal_with(resource_fields)
	def get(self, chosenCategory):
		#result = Site.query.filter_by(category=chosenCategory).all()
		arrayOfSites=list()
		results=session.query(Site).all()
		for result in results:
			if(result.category==chosenCategory):
				arrayOfSites.append(result)
				print(result.name)
		return arrayOfSites

api.add_resource(SearchByCategory, "/category/<string:chosenCategory>")

class SearchByLocation(Resource):
	@marshal_with(resource_fields)
	def get(self, chosenLocation):
		#result = Site.query.filter_by(category=chosenCategory).all()
		arrayOfSites=list()
		results=session.query(Site).all()
		for result in results:
			if(result.gov==chosenLocation or result.town==chosenLocation):
				arrayOfSites.append(result)
				print(result.name)
		return arrayOfSites

api.add_resource(SearchByLocation, "/location/<string:chosenLocation>")

@app.route('/login',methods=['GET'])
class LogIn(Resource):
	@marshal_with(resource_fields_customer)
	def get(self, chosenEmail,chosenPassword):
		result=Customer.query.filter_by(email=chosenEmail).first()
		if(result.password==chosenPassword):
			return result
		if not result:
			abort(404, message="Failed to sign in")

api.add_resource(LogIn, "/login/<string:chosenEmail>/<string:chosenPassword>")

class DestinationsList(Resource):
	@marshal_with(resource_fields_destinations)
	def get(self, chosenID):
		arrayOfSites = list()
		results = session.query(Destinations).all()
		for result in results:
			if (result.customerID == chosenID):
				arrayOfSites.append(result)
		return arrayOfSites

api.add_resource(DestinationsList, "/destinationList/<int:chosenID>")

@app.route('/customer',methods=['PUT'])
class SignUp(Resource):
	@marshal_with(resource_fields_customer)
	def put(self,chosenFirstName,chosenLastName,chosenEmail,chosenPassword):
		#args = customer_put_args.parse_args()
		result = Customer.query.filter_by(email=chosenEmail).first()
		if result:
			abort(409, message="Customer exists")

		newCustomer = Customer(firstName=chosenFirstName, lastName=chosenLastName, email=chosenEmail,password=chosenPassword)
		db.session.add(newCustomer)
		db.session.commit()
		return newCustomer, 201

api.add_resource(SignUp, "/customer/<string:chosenFirstName>/<string:chosenLastName>/<string:chosenEmail>/<string:chosenPassword>")

@app.route('/addDestination',methods=['PUT'])
class AddDestination(Resource):
	@marshal_with(resource_fields_destinations)
	def put(self,chosenId,chosenDestination):
		#args = destinations_put_args.parse_args()
		newDestination= Destinations(customerID=chosenId, destinationName=chosenDestination)
		db.session.add(newDestination)
		db.session.commit()
		return newDestination, 201

api.add_resource(AddDestination, "/addDestination/<int:chosenId>/<string:chosenDestination>")

@app.route('/deleteDestination',methods=['DELETE'])
class DeleteDestination(Resource):
	@marshal_with(resource_fields_destinations)
	def delete(self,chosenId,chosenDestination):
		#args = destinations_put_args.parse_args()
		#filtered=Destinations.query(Destinations).filter_by(Destinations.customerID.like(chosenId),Destinations.destinationName.like(chosenDestination)).delete()
		deletedDestination= Destinations(customerID=chosenId, destinationName=chosenDestination)
		print(deletedDestination.destinationName)
		db.session.delete(deletedDestination)
		db.session.commit()
		return deletedDestination, 201

api.add_resource(DeleteDestination, "/deleteDestination/<int:chosenId>/<string:chosenDestination>")

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=5000)