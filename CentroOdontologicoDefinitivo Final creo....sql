drop database Centro_Odontologico;
create database Centro_Odontologico;
use Centro_Odontologico;

create table Tier_Obra_Social(
	idTier int auto_increment,
    nombre varchar (20),
    coberturaOdontologica varchar(1000),
    primary key(idTier)
);

create table Obra_Social(
	idObraSocial int auto_increment,
    nombre varchar(20),
    primary key(idObraSocial)
);

create table TierObraSocial_ObraSocial(
	idTier int,
    idObraSocial int,
    
    primary key (idTier,idObraSocial),
    foreign key (idObraSocial) references Obra_Social(idObraSocial),
    foreign key (idTier) references Tier_Obra_Social(idTier)
);

create table Paciente(
	idPaciente int auto_increment,
	dni int unique,
    nombre varchar(100),
    apellido varchar(100),
    email varchar(100),
    contrasenia varchar(100),
    telefono int,
    direccion varchar(50),
	obraSocial int,
    
    primary key(idPaciente),
    foreign key (obraSocial) references Obra_Social(idObraSocial)
);

create table Radiografia(
	idRadiografia int auto_increment,
    fecha date,
    paciente int,
    
    primary key(idRadiografia),
    foreign key(paciente) references Paciente(idPaciente)
);


create table Especialidad(
	idEspecialidad int auto_increment,
    nombre varchar(50),
    
    primary key(idEspecialidad)
);

create table Medico(
	idMedico int auto_increment,
    matricula int unique,
    nombre varchar(100),
    apellido varchar(100),
    especialidad int,
    email varchar(100),
    contrasenia varchar(100), 
    
    primary key(idMedico),
    foreign key(especialidad) references Especialidad(idEspecialidad)
);


create table Turno(
	idTurno int auto_increment,
    paciente int,
    medico int,
    fechaAgenda datetime,
    fechaTurno datetime,
    motivo varchar(50),
    requisitos varchar(50),
    
    primary key(idTurno),
    foreign key (paciente) references Paciente(idPaciente),
    foreign key (medico) references Medico(idMedico)
);

create table Token(
idPaciente int,
token varchar(36),
primary key(idPaciente,token),
foreign key (idPaciente) references Paciente(idPaciente)
);

create table Token_Medico(
idMedico int,
token varchar(36),
primary key(idMedico,token),
foreign key (idMedico) references Medico(idMedico)
);

insert into Especialidad(nombre) values 
("Periodoncia"),
("Prostodoncia"),
("Ortodoncia y ortopedia dentofacial"),
("Dolor bucofacial trastornos temporomandibulares"),
("Prótesis maxilofacial y oncología dental"),
("Ortodoncia interceptiva");

insert into Medico(nombre,apellido,matricula,especialidad) values
('Gonzalo','Perez',146166,1),
('Santiago','Silva',135845,1),
('Omar','Riquelme',245621,2),
('Tadeo','Runfenstein',134516,2),
('Roque','Peña',134145,2),
('Jorge','Dencia',131451,3),
('Leonardo','De La Fuente',967516,4),
('Mariano','Medina',674516,5);

insert into Medico(nombre,apellido,matricula,especialidad,email,contrasenia) values
('Rojelio','Rupertencio',213454,1,'med@gmail.com','12345678');

insert into Tier_Obra_Social(nombre,coberturaOdontologica)
values ('Plan 220','Profesionales de cartilla:
-Odontología general, cobertura del 100%.
-Ortodoncia Interceptiva, cobertura del 100% para niños entre 5 y 8 años. 
-Ortodoncia y Ortopedia Funcional, cobertura del 100% de 8 hasta 25 años inclusive.
Profesionales no incluidos en su cartilla:
-Reintegro en Odontología general de hasta $3.450 por año y por persona. (*)
-Reintegro en Prótesis odontológicas de hasta $2.300 por año y por persona. (*)
-Ortodoncia y Ortopedia Funcional, $11.500 por única vez de 8 hasta 25 años inclusive. (**)
(*) Con una antigüedad mínima de 6 meses.
(**) Con una antigüedad mínima de 12 meses (**) Blanqueamiento Dental. Hasta $2.000 por ambos maxilares cada dos años.'),
('Plan 330','Profesionales de cartilla:
- Odontología general, cobertura del 100%.
- Ortodoncia Interceptiva, cobertura del 100% para niños entre 5 y 8 años.
- Ortodoncia y Ortopedia Funcional, cobertura del 100% de 8 hasta 25 años inclusive por única vez. (**)
Profesionales no incluidos en su cartilla:
- Odontología general, reintegro de hasta $4.250 por año y por persona. (*)
- Prótesis odontológicas, reintegro de hasta $4.850 por año y por persona. (*)
- Ortodoncia y Ortopedia Funcional, $11.500 por única vez de 8 hasta 25 años inclusive. (**)
(*) Con una antigüedad mínima de 6 meses.
(**) Con una antigüedad mínima de 12 meses. 
(***) Blanqueamiento Dental. hasta $2.100 por ambos maxilares cada dos años'),
('Plan 440','Profesionales de cartilla:
- Odontología general, cobertura del 100%.
- Ortodoncia Interceptiva, cobertura del 100% para niños entre 5 y 8 años.
- Ortodoncia y Ortopedia Funcional, cobertura del 100% de 8 hasta 25 años inclusive, por única vez. (**)
Profesionales no incluidos en su cartilla:
- Odontología general, reintegro de hasta $5.750 por año y por persona. (*)
- Prótesis odontológicas, reintegro de hasta $9.200 por año y por persona. (*)
- Ortodoncia y Ortopedia Funcional, reintegro de hasta $19.000 por única vez sin límite de edad. (**)
- Implantes, reintegros de hasta $19.000 por año y por persona. (*)
(*) Con una antigüedad mínima de 6 meses.
(**) Con una antigüedad mínima de 12 meses. 
(***) Blanqueamiento Dental. Hasta $2.500 por ambos maxilares cada dos años.'),
('Plan 550','Profesionales de cartilla:
- Odontología general, cobertura del 100%.
- Ortodoncia Interceptiva, cobertura del 100% para niños entre 5 y 8 años.
- Ortodoncia y Ortopedia Funcional, cobertura del 100% de 8 hasta 25 años inclusive, por única vez. (**)
Profesionales no incluidos en su cartilla:
- Odontología general, reintegro de hasta $7.500 por año y por persona. (*)
- Prótesis odontológicas, reintegro de hasta $30.000 por año y por persona. (*)
- Ortodoncia y Ortopedia Funcional, reintegro de hasta $21.000 por única vez sin límite de edad. (**)
- Implantes, reintegros de hasta $33.000 por año y por persona. (*)
- Blanqueamiento Dental, reintegro de hasta $3.000 por ambos maxilares, cada 2 años. (*)
(*) Con una antigüedad mínima de 6 meses.
(**) Con una antigüedad mínima de 12 meses.');


Insert into Obra_Social(nombre)
values ('Galeno'),
('Osde');

insert into TierObraSocial_ObraSocial(idTier,idObraSocial) values
(1,1),
(2,1), 
(3,1),
(4,1),
(2,2);

Insert into Paciente(dni,nombre,apellido,email,contrasenia,telefono,direccion,obraSocial) values
(44798570,'Marcelo Fabrizio','Lombardo','fabiziomarcelolombardo@gmail.com',12345678,1154775943,'Av. Santa Fe 3069',1),
(49243265,'Junior','Quiroga','quirogajunior@gmail.com',12345678,1123426346,'Monte Grande 123',2),
(49243287,'Test','Ferdencio','test@g.c',12345678,1123326346,'Monte las palomas 123',null);

insert into Turno (paciente,medico,fechaAgenda,fechaTurno,motivo,requisitos)
values (1,1,'2021-11-11 12:00:00',now(),'me duele el culo','ninguno');

/*
Insert into Radiografia(fecha,paciente) values
('2009-10-30 00:00:00',1),('20013-04-13 00:00:00',1),('2018-10-30 00:00:00',1),
('2009-10-30 00:00:00',2),('2019-12-30 00:00:00',2),('2013-30-01 00:00:00',2),('2009-10-30 00:00:00',2);
*/
use Centro_Odontologico;
select * from Paciente;
select * from Medico;
select * from Token;
select * from Turno;
select idPaciente from Token where token = 'e3fa97cf-e6cb-4b42-b89e-52d8061d548b';