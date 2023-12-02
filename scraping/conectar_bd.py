import psycopg2
from psycopg2 import sql
from datetime import datetime

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
            "TERMINADO", datetime.now(),
            proceso_dict['registros_procesados'], proceso_dict['registros_no_procesados'],
            proceso_dict['id_proceso']
        )

        # Ejecutar la consulta de inserción
        cursor.execute(sql, valores)
        conexion.commit()
        cursor.close()
        print("DATOS ACTUALIZADOS CORREXCTAMENTE")

    except psycopg2.Error as e:
        print(f"Error durante la inserción de datos: {e}")   
    finally:
        if conexion is not None:
            conexion.close()  
        
def obtenerUsuario(usuario):
    select_query = sql.SQL("SELECT * FROM tb_sunat_usuario WHERE usuario = {}").format(sql.Literal(usuario['usuario']))

    try:

        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        cursor = conexion.cursor()
        cursor.execute(select_query)
        usuario = cursor.fetchone()

        return usuario
    except:
        print("Error al obtenr usuario")

def obtenerEstadoProceso(idProceso):

    query = sql.SQL("SELECT * FROM tb_sunat_proceso WHERE id = {}").format(sql.Literal(idProceso))

    try:

        conexion = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )

        cursor = conexion.cursor()
        cursor.execute(query)
        proceso = cursor.fetchone()

        obj_proceso = {
            "id":proceso[0],
            "fecha_creacion":proceso[1],
            "fecha_finalizacion":proceso[2],
            "estado":proceso[3],
            "registros_procesados":proceso[4],
            "registros_no_procesados":proceso[5],
            "id_usuario":proceso[6],            
        }

        return obj_proceso
    except:
        print("Error al obtenr usuario")

if __name__ == "__main__":
    conectar_bd()