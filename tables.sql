CREATE TABLE Productor(
	Id INTEGER PRIMARY KEY, 
	Name TEXT
);

CREATE TABLE Producto(
	Id     INTEGER PRIMARY KEY, 
	Name   TEXT, 
	Productor_Id INTEGER,
	FOREIGN KEY(Productor_Id) REFERENCES Productor(Id)
);