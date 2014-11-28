from flask import Flask
from flask import Response

app = Flask(__name__)

@app.route('/OData.svc')
@app.route('/OData.svc/')
def get_collections():

	xml =  '<service xmlns="http://www.w3.org/2007/app" xmlns:atom="http://www.w3.org/2005/Atom" xml:base="http://sfodata.herokuapp.com/OData.svc/">'
	xml += '<workspace>'
	xml += '<atom:title>Default</atom:title>'
	xml += '<collection href="Producto">'
	xml += '<atom:title>Producto</atom:title>'
	xml += '</collection>'
	xml += '<collection href="Productor">'
	xml += '<atom:title>Productor</atom:title>'
	xml += '</collection>'
	xml += '</workspace>'
	xml	+= '</service>'

	return Response(xml, mimetype='text/xml')

@app.route('/OData.svc/$metadata')
def get_metadata():	

	xml =  '<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx" Version="1.0">'
	xml += '<edmx:DataServices xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" m:DataServiceVersion="2.0">'
	xml += '<Schema xmlns="http://schemas.microsoft.com/ado/2008/09/edm" Namespace="DataHubContainer">'
	xml += '<EntityContainer Name="DataHubEntities" m:IsDefaultEntityContainer="true">'
	xml += '<EntitySet Name="Productos" EntityType="DataHubModel.Productos"/>'
	xml += '<EntitySet Name="Productores" EntityType="DataHubModel.Productores"/>'
	xml += '<AssociationSet Name="FK_Productos_Productores" Association="DataHubModel.FK_Producto_Productor">'
	xml += '<End EntitySet="Producto" Role="Producto"/>'
	xml += '<End EntitySet="Productor" Role="Productor"/>'
	xml += '</AssociationSet>'
	xml += '</EntityContainer>'
	xml += '</Schema>'
	xml += '<Schema xmlns="http://schemas.microsoft.com/ado/2008/09/edm" Namespace="DataHubModel">'
	xml += '<EntityType Name="Producto">'
	xml += '<Key>'
	xml += '<PropertyRef Name="Id"/>'
	xml += '</Key>'
	xml += '<Property Name="Name" Type="Edm.String" Nullable="true"/>'
	xml += '<Property Name="Id" Type="Edm.Int32" Nullable="false"/>'
	xml += '<Property Name="Productor_Id" Type="Edm.Int32" Nullable="true"/>'
	xml += '<NavigationProperty Name="Supplier" Relationship="DataHubModel.FK_Producto_Productor" FromRole="Producto" ToRole="Productor"/>'
	xml += '</EntityType>'
	xml += '<EntityType Name="Productor">'
	xml += '<Key>'
	xml += '<PropertyRef Name="Id"/>'
	xml += '</Key>'
	xml += '<Property Name="Name" Type="Edm.String" Nullable="true"/>'
	xml += '</EntityType>'
	xml += '<Association Name="FK_Producto_Productor">'
	xml += '<End Role="Productor" Type="DataHubModel.Productor" Multiplicity="0..1"/>'
	xml += '<End Role="Producto" Type="DataHubModel.Producto" Multiplicity="*"/>'
	xml += '<ReferentialConstraint>'
	xml += '<Principal Role="Productor">'
	xml += '<PropertyRef Name="Id"/>'
	xml += '</Principal>'
	xml += '<Dependent Role="Producto">'
	xml += '<PropertyRef Name="Productor_Id"/>'
	xml += '</Dependent>'
	xml += '</ReferentialConstraint>'
	xml += '</Association>'
	xml += '</Schema>'
	xml += '</edmx:DataServices>'
	xml += '</edmx:Edmx>'

	return Response(xml, mimetype='text/xml')


if __name__ == "__main__":
 	app.run()