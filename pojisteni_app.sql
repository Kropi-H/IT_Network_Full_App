create table pojistenci (
    id integer primary key autoincrement,
    jmeno text not null,
    prijmeni  text not null,
    adresa  text not null,
    mesto  text not null,
    psc  integer not null,
    telefon  integer not null,
    email  text not null
);

create table pojistky (
    id integer primary key autoincrement,
    id_pojistence  integer not null,
    predmet_pojisteni text not null,
    typ_pojisteni text not null,
    castka integer not null,
    platnost_od text not null,
    platnost_do text not null
);

create table pojisteni (
    id integer primary key autoincrement,
    predmet_pojisteni text not null
);