import psycopg2
from psycopg2 import sql

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

        cursor = conexion.cursor()

        cursor.close()
        conexion.close()

    except psycopg2.Error as e:
        print(f"Error de conexión a PostgreSQL: {e}")


def insertar_resultado(resultado_dict, idProceso):

    sql = """
            INSERT INTO tb_sunat_resultado (
                fechaBusqueda, numeroRuc, razonSocial, tipoContribuyente,
                nombreComercial, fechaInscripcion, fechaInicioActividades,
                estadoContribuyente, condicionContribuyente, domicilioFiscal,
                sistemaEmisionComprobante, actividadComercioInterior, sistemaContabilidad,
                actividadesEconomicas, emisorElectronicoDesde, comprobantesElectronicos,
                afiliadoAlPLEDesde, padrones, importante,id_proceso
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s
            );
        """
    conexion = None
    try:

        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        cursor = conexion.cursor()

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
            resultado_dict['importante'], idProceso
        )

        # Ejecutar la consulta de inserción
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        print("Datos insertados correctamente.")

    except psycopg2.Error as e:
        print(f"Error durante la inserción de datos: {e}")   
    finally:
        if conexion is not None:
            conexion.close()     

def insertar_proceso(proceso_dict):

    sql = """
            INSERT INTO tb_sunat_proceso (
            fecha_finalizacion,estado,registros_procesados,registros_no_procesados,id_usuario
            ) VALUES (
                %s, %s, %s, %s, %s
            )RETURNING id;
        """
    conexion = None
    try:

        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        cursor = conexion.cursor()

        # Extraer los valores del diccionario
        valores = (
            proceso_dict['fecha_finalizacion'], proceso_dict['estado'],
            proceso_dict['registros_procesados'], proceso_dict['registros_no_procesados'],
            proceso_dict['id_usuario']
        )

        # Ejecutar la consulta de inserción
        cursor.execute(sql, valores)
        nuevo_proceso_id = cursor.fetchone()[0]
        conexion.commit()
        cursor.close()
        print("Datos insertados correctamente.")
        return nuevo_proceso_id

    except psycopg2.Error as e:
        print(f"Error durante la inserción de datos: {e}")   
    finally:
        if conexion is not None:
            conexion.close()  

def actualizar_proceso(proceso_dict):

    sql = """
            UPDATE tb_sunat_proceso 
            SET 
                estado = %s,
                fecha_finalizacion  = %s,
                registros_procesados  = %s,
                registros_no_procesados = %s
            where id = %s
            ;
        """
    conexion = None
    try:

        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        cursor = conexion.cursor()

        # Extraer los valores del diccionario
        valores = (
            proceso_dict['fechaBusqueda'], proceso_dict['estado'],
            proceso_dict['registros_procesados'], proceso_dict['registros_no_procesados']
        )

        # Ejecutar la consulta de inserción
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        print("Datos insertados correctamente.")

    except psycopg2.Error as e:
        print(f"Error durante la inserción de datos: {e}")   
    finally:
        if conexion is not None:
            conexion.close()  
        

if __name__ == "__main__":
    conectar_bd()