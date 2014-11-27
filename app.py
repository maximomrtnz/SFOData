from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/OData.svc')
def index():
	
	xml = '<service xmlns="http://www.w3.org/2007/app" xmlns:atom="http://www.w3.org/2005/Atom" xml:base="http://services.odata.org/OData/OData.svc/">'
	xml += '<workspace>'
	xml += '<atom:title>Default</atom:title>'
	xml += '<collection href="Products">'
	xml += '<atom:title>Products</atom:title>'
	xml += '</collection>'
	xml += '</workspace>'
	xml	+= '</service>'

	return Response(xml, mimetype='text/xml')

if __name__ == "__main__":
 	app.run()