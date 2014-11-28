from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/OData.svc')
@app.route('/OData.svc/')
def get_collections():

	xml = '<service xmlns="http://www.w3.org/2007/app" xmlns:atom="http://www.w3.org/2005/Atom" xml:base="http://sfodata.herokuapp.com/OData.svc/">'
	xml += '<workspace>'
	xml += '<atom:title>Default</atom:title>'
	xml += '<collection href="Products">'
	xml += '<atom:title>Products</atom:title>'
	xml += '</collection>'
	xml += '</workspace>'
	xml	+= '</service>'

	return Response(xml, mimetype='text/xml')

@app.route('/OData.svc/$metadata')
def get_metadata():	
	return ''	

if __name__ == "__main__":
 	app.run()