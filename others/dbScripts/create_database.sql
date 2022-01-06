PRAGMA foreign_keys = ON;

drop table if exists usuario;


create table usuario
(
    correo     text primary key not null default 'no_email',
    nombre     text             not null default 'no_name',
    ap_paterno text             not null default 'no_paterno'
);

