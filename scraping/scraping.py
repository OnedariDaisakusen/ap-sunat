
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
from conectar_bd import conectar_bd, insertar_resultado
from datetime import datetime

# Variable que devolvera el metodo iniciarProceso()
resultado = {}

def iniciarProceso():

    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #Usamos firefox como navegador
    # options = webdriver.FirefoxOptions()

    # # Usamos chrome como navegador
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    #options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--start-maximized")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')

    # Se agregan opciones si son necesarias
    # driver = webdriver.Firefox(options=options)

    # # Se agregan opciones si son necesarias
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe")

    # driver.delete_all_cookies()

    # Indicamos la pagina a hacer el scraping
    # driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias')
    driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')

    # Buscamos el imput para el ruc
    imput_ruc = driver.find_element(By.ID, 'txtRuc')
    # Le digito un valor
    time.sleep(random.randint(1, 10))
    imput_ruc.send_keys('20487988023')

    # Buscamos el boton para el submit
    boton_buscar = driver.find_element(By.ID, 'btnAceptar')
    # Hacemos click
    time.sleep(random.randint(1, 10))
    boton_buscar.click()

    time.sleep(random.randint(1, 10))

    try:
        # Aqui se tiene el contenedor de todos los valores requeridos
        tabla_resultado = driver.find_element(By.CLASS_NAME, 'list-group') 
        # Aqui se obtiene la lista de items que tiene el contendor
        filas_resultado = tabla_resultado.find_elements(By.CLASS_NAME, 'list-group-item')

        for fila in filas_resultado:
            try:
                # Cada list-group-item puede tener uno o mas rows#driver.quit()
                elemento_row = fila.find_element(By.CLASS_NAME, "row")
                try:
                    nombre_valor = elemento_row.find_element(By.CLASS_NAME, "col-sm-5")
                    nombre_valor_text = nombre_valor.text.replace(':', '')

                    valor = elemento_row.find_element(By.CLASS_NAME, "col-sm-7")
                    valor_text = valor.text
                    
                    resultado[nombre_valor_text] = valor_text
                    mapeo_resultado(resultado,'20487988023')
                    insertar_resultado(resultado)
                except NoSuchElementException:
                    print("No se encontró el elemento col-sm-5 / col-sm-7 en esta fila.")            
                    #driver.quit()
            except NoSuchElementException:
                print("No se encontró el elemento row en esta fila.")
                #driver.quit()                     
    except NoSuchElementException: 
        print("Hubo un error al obtener el elemento") 
        #driver.quit()

    #driver.quit()  
    time.sleep(random.randint(1, 10))
    driver.quit()  

    print(resultado)

    return resultado


# def mapeoVariables(nombreValor, valor):
#     if nombreValor == 'Número de RUC:':
#         resultado[nombreValor] = valor
#     if nombreValor == 'Tipo Contribuyente:':
#         resultado[nombreValor] = valor        

def insertar_resultado(resultado):
    # Establecer conexión y obtener el cursor
    conexion, cursor = conectar_bd()

    # Llamamos a la función para insertar los datos
    insertar_resultado(cursor, resultado)

    # Confirmar la transacción y cerrar el cursor y la conexión
    conexion.commit()
    cursor.close()
    conexion.close()

def mapeo_resultado(resultado, ruc):
    resultado['fechaBusqueda'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado['numeroRuc'] = ruc
    
iniciarProceso()