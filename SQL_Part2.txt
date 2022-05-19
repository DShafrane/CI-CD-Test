drop table sell;
drop table primary_physician;
drop table prescribe;
drop table pharmacy;
drop table drugs;
drop table patientsanddoctors;
drop table patients;
drop table doctors;


create table Patients(
	P_ID VARCHAR(10) NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Address VARCHAR(40),
	Age INT NOT NULL,
	Primary Key(P_ID)
);

create table Doctors(
	D_ID VARCHAR(10) NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Speciality VARCHAR(20) NOT NULL,
	Years_of_experience INT NOT NULL,
	Primary Key(D_ID)
);

create table Drugs(
	M_ID VARCHAR(10) NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Formula VARCHAR(30),
	Primary Key(M_ID)
);

create table Pharmacy(
	H_ID VARCHAR(10) NOT NULL,
	D_ID VARCHAR(10) NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Location VARCHAR(10),
	Primary Key(H_ID),
	Foreign Key(D_ID) REFERENCES Doctors(D_ID)
	
);

create table Sell(
	H_ID VARCHAR(10) NOT NULL,
	M_ID VARCHAR(10) NOT NULL,
	Price INT NOT NULL,
	Primary Key(H_ID, M_ID),
	Foreign Key(H_ID) REFERENCES Pharmacy(H_ID),
	Foreign Key(M_ID) REFERENCES Drugs(M_ID)
);

create table Prescribe(
	P_ID VARCHAR(10) NOT NULL,
	D_ID VARCHAR(10) NOT NULL,
	M_ID VARCHAR(10),
	Date DATE NOT NULL,
	Description TEXT,
	Primary Key(P_ID, D_ID, Date),
	Foreign Key(P_ID) REFERENCES Patients(P_ID),
	Foreign Key(D_ID) REFERENCES Doctors(D_ID),
	Foreign Key(M_ID) REFERENCES Drugs(M_ID)
);

create table Primary_Physician(
	P_ID VARCHAR(10) NOT NULL,
	D_ID VARCHAR(10) NOT NULL,
	Primary Key(P_ID),
	Foreign Key(P_ID) REFERENCES Patients(P_ID),
	Foreign Key(D_ID) REFERENCES Doctors(D_ID)
);

create table PatientsandDoctors(
	P_ID VARCHAR(10) NOT NULL,
	D_ID VARCHAR(10) NOT NULL,
	Primary Key(P_ID, D_ID),
	Foreign Key(P_ID) REFERENCES Patients(P_ID),
	Foreign Key(D_ID) REFERENCES Doctors(D_ID)
);




INSERT INTO patients VALUES (111, 'Ali', 'Beirut', 52);
INSERT INTO patients VALUES (113, 'Mousa', null, 32);
INSERT INTO patients VALUES (221, 'Mohamad', 'Hazmiyeh', 20);
INSERT INTO patients VALUES (112, 'Sherifa', 'Chiyah', 37);
INSERT INTO patients VALUES (135, 'Fatima', 'Beirut', 13);
INSERT INTO doctors VALUES (331, 'Ahmad', 'Physiology', 4);
INSERT INTO doctors VALUES (332, 'Hafez', 'Surgeon', 13);
INSERT INTO doctors VALUES (334, 'Atef', 'Surgeon', 22);
INSERT INTO doctors VALUES (451, 'Shaza', 'Psychologist', 12);
INSERT INTO drugs VALUES (1, 'Panadol Advanced');
INSERT INTO drugs VALUES (2, 'Panadol Lite');
INSERT INTO drugs VALUES (3, 'Daivobet', 'calcipotriol ');
INSERT INTO drugs VALUES (4, 'Betnovate', 'C27H37FO6');
INSERT INTO pharmacy VALUES (1, 331, 'Notre Dame Pharmacy', 'Chiyah');
INSERT INTO pharmacy VALUES (2, 331, 'Saadeh Pharmacy', 'Chiyah');
INSERT INTO pharmacy VALUES (3, 451, 'Al Sharek Pharmacy', 'Beirut');
INSERT INTO pharmacy VALUES (4, 334, 'Mazen Pharmacy');
INSERT INTO sell VALUES (1, 1, 50);
INSERT INTO sell VALUES (1, 4, 120);
INSERT INTO sell VALUES (2, 4, 115);
INSERT INTO sell VALUES (2, 2, 30);
INSERT INTO sell VALUES (3, 3, 100);
INSERT INTO sell VALUES (3, 1, 55);
INSERT INTO sell VALUES (4, 2, 32);
INSERT INTO sell VALUES (4, 3, 105);
INSERT INTO prescribe VALUES (111, 334, 2, '2021-11-17', 'Take twice a day');
INSERT INTO prescribe VALUES (221, 334, 3, '2021-06-19', 'Take once a day');
INSERT INTO prescribe VALUES (135, 332, 4, '2022-01-23');
INSERT INTO prescribe VALUES (112, 451, 1, '2021-07-05', 'Take twice a day');
INSERT INTO prescribe VALUES (113, 451, 1, now());
INSERT INTO primary_physician VALUES (111, 331);
INSERT INTO primary_physician VALUES (221, 334);
INSERT INTO primary_physician VALUES (135, 332);
INSERT INTO primary_physician VALUES (112, 451);
INSERT INTO primary_physician VALUES (113, 451);
INSERT INTO patientsanddoctors VALUES (111, 331);
INSERT INTO patientsanddoctors VALUES (111, 334);
INSERT INTO patientsanddoctors VALUES (221, 334);
INSERT INTO patientsanddoctors VALUES (221, 332);
INSERT INTO patientsanddoctors VALUES (135, 331);
INSERT INTO patientsanddoctors VALUES (112, 451);
INSERT INTO patientsanddoctors VALUES (113, 451);
INSERT INTO patientsanddoctors VALUES (113, 332);
