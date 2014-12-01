import sqlite3
import time
import urllib

sqlite2odata_types = {
	
	'INTEGER':'Edm.Int64',
	'REAL':'Edm.Double',
	'TEXT':'Edm.String',
	'BLOB':'Edm.Binary'

}

class Sqlite2OData:
	
	def __init__(self, database_path):
		self.database_path = database_path

	def get_collections(self):

		try:	

			# Conect to the Database
			con = sqlite3.connect(self.database_path)

			con.text_factory = str

			# Create a cursor 
			cursor = con.cursor()

			# Get Tables name from sqlite_master
			cursor.execute('SELECT name FROM sqlite_master WHERE type="table";') 

			tables = cursor.fetchall()

			# Atom response 

			xml =  '<service xmlns="http://www.w3.org/2007/app" xmlns:atom="http://www.w3.org/2005/Atom" xml:base="http://sfodata.herokuapp.com/OData.svc/">'
			xml += '<workspace>'
			xml += '<atom:title>Default</atom:title>'

			# Create a Collection for each Table inside de database
			for table in tables:
				xml += '<collection href="'+table[0]+'">'
				xml += '<atom:title>'+table[0]+'</atom:title>'
				xml += '</collection>'

			xml += '</workspace>'
			xml	+= '</service>'	

		except sqlite3.Error, e:
    
			print "Error %s:" % e.args[0]
			sys.exit(1)	

		finally:

    		# Close Database connection
			if con:
				con.close()	
			
			# Return Atom response
			return xml


	def get_metadata(self):

		try:	

			# Conect to the Database
			con = sqlite3.connect(self.database_path)

			con.text_factory = str

			# Create a cursor 
			cursor = con.cursor()

			# Get Tables name from sqlite_master
			cursor.execute('SELECT name FROM sqlite_master WHERE type="table";') 

			tables = cursor.fetchall()

			# Atom response 
			xml =  '<edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx" Version="1.0">'
			xml += '<edmx:DataServices xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" m:DataServiceVersion="2.0">'
			xml += '<Schema xmlns="http://schemas.microsoft.com/ado/2008/09/edm" Namespace="DataHubContainer">'
			xml += '<EntityContainer Name="DataHubEntities" m:IsDefaultEntityContainer="true">'

			# Create an EntitySet for each Table inside de database
			for table in tables:
				xml += '<EntitySet Name="'+table[0]+'" EntityType="DataHubModel.'+table[0]+'"/>'

			# Create an AssociationSet for each Reletion inside de database	
			for table in tables:

				# Get Foreign Key for each table
				cursor.execute('PRAGMA foreign_key_list('+table[0]+')')
				data = cursor.fetchall()

				for d in data:
					xml += '<AssociationSet Name="FK_'+table[0]+'_'+d[2]+'" Association="DataHubModel.FK_'+table[0]+'_'+d[2]+'">'
					xml += '<End EntitySet="'+table[0]+'" Role="'+table[0]+'" />'
					xml += '<End EntitySet="'+d[2]+'" Role="'+d[2]+'" />'
					xml += '</AssociationSet>'

			xml += '</EntityContainer>'
			xml += '</Schema>'	

			# Model Atom Part
			xml += '<Schema xmlns="http://schemas.microsoft.com/ado/2008/09/edm" Namespace="DataHubModel">'

			# Create a EntityType for each table
			for table in tables:

				xml += '<EntityType Name="'+table[0]+'">'

				# Create a Property Tag for each column's table  
				cursor.execute('PRAGMA table_info('+table[0]+')')
				data = cursor.fetchall()

				# Create a Key Entry For Each Primary Key 
				xml += '<Key>'

				for d in data:

					if d[5] == 1:
						xml+= '<PropertyRef Name="'+d[1]+'"/>'

				
				xml += '</Key>'

				# Column Positions
				# 0 -> Index
				# 1 -> Column Name
				# 2 -> Column Type
				
				for d in data:
					xml += '<Property Name="'+d[1]+'" Type="'+sqlite2odata_types[d[2]]+'" Nullable="true"/>'

				xml += '</EntityType>'	

				# Get Foreign Key for each table
				cursor.execute('PRAGMA foreign_key_list('+table[0]+')')
				data = cursor.fetchall()

				# Create an Association tag for every Foreign Key in Every Table
				for d in data:
					xml += '<Association Name="FK_'+table[0]+'_'+d[2]+'">'
					xml += '<End Role="'+d[2]+'" Type="DataHubModel.'+d[2]+'" Multiplicity="0..1"/>'
					xml += '<End Role="'+table[0]+'" Type="DataHubModel.'+table[0]+'" Multiplicity="*"/>'
					xml += '<ReferentialConstraint>'
					xml += '<Principal Role="'+d[2]+'">'
					xml += '<PropertyRef Name="'+d[4]+'"/>'
					xml += '</Principal>'
					xml += '<Dependent Role="Producto">'
					xml += '<PropertyRef Name="'+d[3]+'"/>'
					xml += '</Dependent>'
					xml += '</ReferentialConstraint>'
					xml += '</Association>'

			xml += '</Schema>'

			xml += '</edmx:DataServices>'
			xml += '</edmx:Edmx>'

		except sqlite3.Error, e:
    
			print "Error %s:" % e.args[0]
			sys.exit(1)	

		finally:

    		# Close Database connection
			if con:
				con.close()	
			
			# Return Atom response
			return xml

	def get_entries(self, table_name, url_path, url_root):

		#try:

		# Conect to the Database
		con = sqlite3.connect(self.database_path)

		con.text_factory = str

		# Create a cursor 
		cursor = con.cursor()

		# Execute query to get all entries's table
		cursor.execute('SELECT * FROM '+table_name+';') 

		# Get rows
		rows = cursor.fetchall()


		# Atom response 
		xml = '<?xml version="1.0" encoding="utf-8"?>'
		xml += '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xml:base="'+url_root+'DataHub.svc/">'
		xml += '<title type="text">'+table_name+'</title>'
		xml += '<id>'+url_path+'</id>'
		xml += '<updated>'+time.strftime('%Y-%m-%dT%H:%M:%SZ')+'</updated>'
		xml += '<link rel="self" title="'+table_name+'" href="'+table_name+'"></link>'

		# Create an entry for each record's table
		for row in rows:

			xml += '<entry>'

			# Get the row id
			xml += '<id>'+url_path+'(\''+str(row[0])+'\')'+'</id>'

			xml += '<title type="text"></title>'

			xml += '<updated>'+time.strftime('%Y-%m-%dT%H:%M:%SZ')+'</updated>'

			xml += '<author><name></name></author>'

			xml += '<link rel="edit" title="'+table_name+'" href="'+table_name+'(\''+str(row[0])+'\')"></link>'

			xml += '<category term="DataHubModel.'+table_name+'" scheme="http://schemas.microsoft.com/ado/2007/08/dataservices/scheme"></category>'

			xml += '<content type="application/xml">'

			xml += '<m:properties>'	

			# Get Table Fields
			cursor.execute('PRAGMA table_info('+table_name+')')
			data = cursor.fetchall()

			for d in data:

				xml += '<d:'+d[1]+' m:type="'+sqlite2odata_types[d[2]]+'">'+urllib.quote(str(row[d[0]]))+'</d:'+d[1]+'>' 

			xml += '</m:properties>'

			xml += '</content>'

			xml += '</entry>'

		xml += '</feed>'

	#except sqlite3.Error, e:

		#print "Error %s:" % e.args[0]
		#sys.exit(1)		

	#finally:

		# Return Atom response
		return xml
