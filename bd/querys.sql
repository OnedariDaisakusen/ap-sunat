CREATE TABLE public.tb_sunat_resultado (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	fechabusqueda date NULL,
	numeroruc text NULL,
	razonsocial text NULL,
	tipocontribuyente text NULL,
	nombrecomercial text NULL,
	fechainscripcion date NULL,
	fechainicioactividades date NULL,
	estadocontribuyente text NULL,
	condicioncontribuyente text NULL,
	domiciliofiscal text NULL,
	sistemaemisioncomprobante text NULL,
	actividadcomerciointerior text NULL,
	sistemacontabilidad text NULL,
	actividadeseconomicas text NULL,
	emisorelectronicodesde date NULL,
	comprobanteselectronicos text NULL,
	afiliadoalpledesde date NULL,
	padrones text NULL,
	importante text NULL,
	CONSTRAINT tb_sunat_resultado_pkey PRIMARY KEY (id),
    id_proceso INT REFERENCES tb_sunat_proceso(id)
);


CREATE TABLE IF NOT EXISTS tb_sunat_usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO tb_sunat_usuario (nombre, apellido, email, fecha_nacimiento, usuario, contrasena)
VALUES ('Franco', 'Rojas', 'fra.roj@example.com', '1990-01-01', 'franco123', '123456');

select * from tb_sunat_usuario

CREATE TABLE IF NOT EXISTS tb_sunat_proceso (
    id SERIAL PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_finalizacion TIMESTAMP,
    estado VARCHAR(50),
    registros_procesados INT,
    registros_no_procesados INT,
    id_usuario INT REFERENCES tb_sunat_usuario(id)
);