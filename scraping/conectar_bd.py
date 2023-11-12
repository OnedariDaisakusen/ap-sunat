import psycopg2
from psycopg2 import sql

def tabla_existe(cursor, nombre_tabla):
    # Verificar si la tabla ya existe
    consulta = sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);")
    cursor.execute(consulta, [nombre_tabla])
    return cursor.fetchone()[0]

def crear_tabla_resultado_si_no_existe(cursor):
    nombre_tabla = 'tb_resultado'

    # Verificar si la tabla ya existe
    consulta_existe = sql.SQL("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s);")
    cursor.execute(consulta_existe, [nombre_tabla])
    tabla_existe = cursor.fetchone()[0]

    if not tabla_existe:
        # Si la tabla no existe, crearla
        consulta_creacion = sql.SQL("""
            CREATE TABLE {} (
                fechaBusqueda DATE,
                numeroRuc VARCHAR(20),
                razonSocial VARCHAR(255),
                tipoContribuyente VARCHAR(50),
                nombreComercial VARCHAR(255),
                fechaInscripcion DATE,
                fechaInicioActividades DATE,
                estadoContribuyente VARCHAR(50),
                condicionContribuyente VARCHAR(50),
                domicilioFiscal TEXT,
                sistemaEmisionComprobante VARCHAR(50),
                actividadComercioInterior VARCHAR(255),
                sistemaContabilidad VARCHAR(50),
                actividadesEconomicas TEXT,
                emisorElectronicoDesde DATE,
                comprobantesElectronicos VARCHAR(255),
                afiliadoAlPLEDesde DATE,
                padrones TEXT,
                importante TEXT
            );
        """).format(sql.Identifier(nombre_tabla))

        cursor.execute(consulta_creacion)
        print(f"Tabla '{nombre_tabla}' creada.")
    else:
        print(f"La tabla '{nombre_tabla}' ya existe.")

def conectar_bd():
    try:
        # Parámetros de conexión, reemplázalos con tus propias credenciales
        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Llamamos a la función para crear la tabla si no existe
        crear_tabla_resultado_si_no_existe(cursor)

        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

    except psycopg2.Error as e:
        print(f"Error de conexión a PostgreSQL: {e}")


def insertar_resultado(cursor, resultado_dict):
    nombre_tabla = 'resultado'

    try:
        # Construir la consulta de inserción
        consulta_insercion = sql.SQL("""
            INSERT INTO {} (
                fechaBusqueda, numeroRuc, razonSocial, tipoContribuyente,
                nombreComercial, fechaInscripcion, fechaInicioActividades,
                estadoContribuyente, condicionContribuyente, domicilioFiscal,
                sistemaEmisionComprobante, actividadComercioInterior, sistemaContabilidad,
                actividadesEconomicas, emisorElectronicoDesde, comprobantesElectronicos,
                afiliadoAlPLEDesde, padrones, importante
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """).format(sql.Identifier(nombre_tabla))

        # Extraer los valores del diccionario
        valores = (
            resultado_dict['fechaBusqueda'], resultado_dict['numeroRuc'],
            resultado_dict['razonSocial'], resultado_dict['tipoContribuyente'],
            resultado_dict['nombreComercial'], resultado_dict['fechaInscripcion'],
            resultado_dict['fechaInicioActividades'], resultado_dict['estadoContribuyente'],
            resultado_dict['condicionContribuyente'], resultado_dict['domicilioFiscal'],
            resultado_dict['sistemaEmisionComprobante'], resultado_dict['actividadComercioInterior'],
            resultado_dict['sistemaContabilidad'], resultado_dict['actividadesEconomicas'],
            resultado_dict['emisorElectronicoDesde'], resultado_dict['comprobantesElectronicos'],
            resultado_dict['afiliadoAlPLEDesde'], resultado_dict['padrones'],
            resultado_dict['importante']
        )

        # Ejecutar la consulta de inserción
        cursor.execute(consulta_insercion, valores)
        print("Datos insertados correctamente.")

    except psycopg2.Error as e:
        print(f"Error durante la inserción de datos: {e}")        

        
if __name__ == "__main__":
    conectar_bd()