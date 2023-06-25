create table pojistenci (
    id integer primary key autoincrement,
    jmeno integer not null,
    prijmeni  integer not null,
    adresa  integer not null,
    mesto  integer not null,
    psc  integer not null,
    telefon  integer not null,
    email  integer not null
);

create table typ_pojisteni (
    id integer primary key autoincrement,
    pojisteni  integer not null
);

create table pojisteni_pojistence (
    id integer primary key autoincrement,
    castka  integer not null,
    predmet_pojisteni  integer not null,
    platnost_od  integer not null,
    platnost_do  integer not null
);