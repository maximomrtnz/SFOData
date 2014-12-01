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
	return Response(xml, mimetype='application/atom+xml;charset=utf-8')

@app.route('/OData.svc/$metadata')
def get_metadata():	
	xml =  s2od.get_metadata()
	return Response(xml, mimetype='application/atom+xml;charset=utf-8')

@app.route('/OData.svc/<table>')
def get_entries(table):
	
	# Get params from URL if exists
	top_param = request.args.get('$top')
	select_param = request.args.get('$select')
	filter_param = request.args.get('$filter')
	order_param = request.args.get('$orderby')


	xml =  s2od.get_entries(table,request.url_root, top_param, select_param, filter_param, order_param)
	return Response(xml, mimetype='application/atom+xml;charset=utf-8')	

if __name__ == "__main__":
 	app.run(debug=True)