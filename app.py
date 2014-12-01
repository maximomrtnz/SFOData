from flask import Flask
from flask import Response
from flask import request
from sqlite2odata import Sqlite2OData

app = Flask(__name__)
s2od = Sqlite2OData('database.db')

@app.route('/OData.svc')
@app.route('/OData.svc/')
def get_collections():
	xml =  s2od.get_collections()
	return Response(xml, mimetype='text/xml')

@app.route('/OData.svc/$metadata')
def get_metadata():	
	xml =  s2od.get_metadata()
	return Response(xml, mimetype='text/xml')

@app.route('/OData.svc/<table>')
def get_entries(table):
	xml =  s2od.get_entries(table, request.url, request.url_root)
	return Response(xml, mimetype='text/xml')	
	
if __name__ == "__main__":
 	app.run(debug=True)