PRAGMA foreign_keys = ON;

drop table if exists usuario;


create table estrategias
(
    id_estrategia    integer primary key not null default 0,
    texto_estrategia text                not null default 'no_extrategia'
);

create table tipo_pregunta
(
    id_tipo_pregunta integer primary key not null default 0,
    texto_tipo       text                not null default 'no_tipo'
);

create table preguntas
(
    id_pregunta      integer primary key not null default 0,
    texto_pregunta   text                not null default 'no_pregunta',
    id_tipo_pregunta int                 not null default 0,
    constraint preguntas_tipo_pregunta_fk
        foreign key (id_tipo_pregunta) references tipo_pregunta (id_tipo_pregunta) on delete cascade on update restrict
);



create table emociones
(
    id_emocion    integer primary key not null default 0,
    emocion_texto text                not null default 'no_emocion'
);

create table usuario
(
    correo           text primary key not null default 'no_email',
    nombre           text             not null default 'no_name',
    ap_paterno       text             not null default 'no_paterno',
    ap_materno       text             not null default 'no_materno',
    password         text             not null default 'password',
    salt             text             not null default 'no_salt',
    fecha_nacimiento integer          not null default 0

);

create table emociones_detectadas
(
    id_emocion      integer not null default 0,
    correo          text                not null default 'no_email',
    id_estrategia   integer             not null default 0,
    fecha_deteccion integer             not null default 0,
    primary key (id_emocion, correo, id_estrategia, fecha_deteccion),
    constraint emociones_detectadas_usuario_fk
        foreign key (correo) references usuario (correo) on delete cascade on update restrict,
    constraint emociones_detectadas_estrategia_fk
        foreign key (id_estrategia) references estrategias (id_estrategia) on delete cascade on update restrict,
    constraint emociones_detectadas_emocion_fk
        foreign key (id_emocion) references emociones (id_emocion) on delete cascade on delete restrict

);


create trigger if not exists new_emocion_detectada
    after insert
    on emociones_detectadas
begin
    update emociones_detectadas
    set fecha_deteccion = (strftime('%s', 'now') + 1800)
    where ROWID == new.ROWID;
end;



create table respuestas
(
    id_pregunta     integer primary key not null default 1,
    correo          text                not null default 'no_correo',
    respuesta_texto text                not null default 'sin respuesta',
    constraint respuestas_usuario_fk
        foreign key (correo) references usuario (correo) on delete cascade on update restrict,
    constraint respuestas_preguntas_fk
        foreign key (id_pregunta) references preguntas (id_pregunta) on delete cascade on update restrict
);

insert into emociones values (0,'Negativo');
insert into emociones values (1,'Positiva');

insert into estrategias values (1, 'nueva estrategia');


