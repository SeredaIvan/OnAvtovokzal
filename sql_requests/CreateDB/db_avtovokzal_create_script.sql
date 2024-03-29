--create database avtovokzalf;

use avtovokzalf;

create table buses (
    id_bus int not null identity(1,1) PRIMARY KEY,
    name nvarchar(50) not null,
    seats int not null,
    bus_number nvarchar(8) check (bus_number like '[À-ß][À-ß][0-9][0-9][0-9][0-9][À-ß][À-ß]') unique
);

create table cities (
    id_city int not null identity(1,1) PRIMARY KEY,
    name nvarchar(50) not null,
    country nvarchar(50) null
);

create table clients (
    id_client int not null identity(1,1) PRIMARY KEY,
    name nvarchar(50) not null,
    phone nvarchar(11) check (phone like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') not null unique default '',
    email nvarchar(50) not null unique default '' check (email like '%@%.%'),
    password nvarchar(50) not null,
    role_client nvarchar(50) not null default 'user'
);

CREATE TABLE non_autorized_users(
    id_user int PRIMARY KEY not null,
    name nvarchar(20) not null,
    phone nvarchar(11) not null unique check (phone like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]') default ''
);

CREATE TABLE timetable (
    id_journey int not null identity(1,1) PRIMARY KEY,
    bus_id int null,
    city_start_id int not null,
    city_finish_id int not null,
    cost float not null,
    time_start datetime default GETDATE() not null,
    time_finish datetime default GETDATE() not null,
    seats_occupied int not null default 0,
    is_active bit null default 1,
    FOREIGN KEY (bus_id) REFERENCES buses(id_bus),
    FOREIGN KEY (city_start_id) REFERENCES cities(id_city),
    FOREIGN KEY (city_finish_id) REFERENCES cities(id_city)
);

create table orders (
    id_order INT PRIMARY KEY IDENTITY(1,1),
    client_id INT NULL,
    non_authorized_users_id INT NULL,
    date_buying DATETIME DEFAULT GETDATE(),
    cost float null,
    whether_paid bit null,
    FOREIGN KEY (client_id) REFERENCES clients(id_client),
    FOREIGN KEY (non_authorized_users_id) REFERENCES non_autorized_users(id_user)
);

create table tickets(
    id_ticket int not null identity(1,1) PRIMARY KEY,
    bus_id int not null,
    seat int not null,
    date_buying datetime default GETDATE() null,
    journey_id int null,
    non_autorized_users_id int null,
    client_id int not null,
    order_id int not null,
    code int null unique,
    FOREIGN KEY (bus_id) REFERENCES buses(id_bus),
    FOREIGN KEY (client_id) REFERENCES clients(id_client),
    FOREIGN KEY (journey_id) REFERENCES timetable(id_journey),
    FOREIGN KEY (order_id) REFERENCES orders(id_order),
    FOREIGN KEY (non_autorized_users_id) REFERENCES non_autorized_users(id_user)
);
