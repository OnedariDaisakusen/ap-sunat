
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from conectar_bd import insertar_resultado
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variable que devolvera el metodo iniciarProceso()
resultado = {}
# variable_ruc = "20519223105"
# lista_rucs = ["20600869095","20601033021","20600864735"]

def iniciarProceso(lista_rucs,idProceso):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #Usamos firefox como navegador
    # options = webdriver.FirefoxOptions()

    # # Usamos chrome como navegador
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    # options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    # options.add_argument('--proxy-server=%s' % proxy_address)  
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    # Se agregan opciones si son necesarias
    # driver = webdriver.Firefox(options=options)

    # # Se agregan opciones si son necesarias
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=options)

    # driver = webdriver.Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe")

    # Indicamos la pagina a hacer el scraping
    # driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias')
    driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')

    driver.delete_all_cookies()

    print("Se abrio la pagina:")

    for ruc in lista_rucs:
        # Buscamos el imput para el ruc
        imput_ruc = driver.find_element(By.ID, 'txtRuc')
        # Le digito un valor
        imput_ruc.send_keys(ruc)
        # imput_ruc.send_keys('20469378561')
        # Buscamos el boton para el submit
        boton_buscar = driver.find_element(By.ID, 'btnAceptar')
        # Hacemos click
        boton_buscar.click()

        time.sleep(5)

        try:
            # Aqui se tiene el contenedor de todos los valores requeridos
            tabla_resultado = driver.find_element(By.CLASS_NAME, 'list-group') 
            # Aqui se obtiene la lista de items que tiene el contendor
            filas_resultado = tabla_resultado.find_elements(By.CLASS_NAME, 'list-group-item')
            cod_resultado_mapeo_valores_sm5_sm7 = 0
            cod_resultado_mapeo_valores_sm3 = 0
            cod_resultado_mapeo_valores_sm12 = 0

            for fila in filas_resultado:
                try:
                    # Cada list-group-item puede tener uno o mas rows#driver.quit()
                    elemento_row = fila.find_element(By.CLASS_NAME, "row")

                    # Este bloque try obtiene de la etiqueta row las etiquetas col-sm-5 / col-sm-7
                    cod_resultado_mapeo_valores_sm5_sm7 = mapeo_valores_sm5_sm7(elemento_row)

                    if cod_resultado_mapeo_valores_sm5_sm7 == 1:
                        cod_resultado_mapeo_valores_sm3 = mapeo_valores_sm3(elemento_row)

                    if cod_resultado_mapeo_valores_sm3 == 1:
                        cod_resultado_mapeo_valores_sm12 = mapeo_valores_sm12(elemento_row)                
                
                except NoSuchElementException:
                    print("No se encontró el elemento row en esta fila.")
                cod_result_bloque1 = 0
                cod_result_bloque2 = 0
            agregar_valores_defecto(ruc)
            print(resultado)
            insertar_resultado(resultado, idProceso)         

            boton_volver = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btnNuevaConsulta"))
            )

            # Hacer clic en el botón
            boton_volver.click()
            time.sleep(2)                   
        except NoSuchElementException: 
            print("Hubo un error al obtener el elemento list-group")
            driver.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/FrameCriterioBusquedaWeb.jsp')
            driver.delete_all_cookies()

    # time.sleep(random.randint(1, 10))
    driver.quit()  



def mapeo_valores_sm5_sm7(row):
    try:
        nombre_valor = row.find_element(By.CLASS_NAME, "col-sm-5")
        nombre_valor_text = nombre_valor.text.replace(':', '')

        valor = row.find_element(By.CLASS_NAME, "col-sm-7")
        valor_text = valor.text

        resultado[mapeo_resultado(nombre_valor_text)] = valor_text
        return 0 # Si todo es correcto
    except NoSuchElementException:
        return 1 # Si hubo un error
    
def mapeo_valores_sm3(row):
    try:

        lista_elementos = row.find_elements(By.CLASS_NAME, "col-sm-3")

        for indice, elemento in enumerate(lista_elementos):

            if elemento.text == 'Fecha de Inscripción:':
                resultado[mapeo_resultado(elemento.text.replace(':', ''))] = lista_elementos[indice + 1].text
            if elemento.text == 'Fecha de Inicio de Actividades:':
                resultado[mapeo_resultado(elemento.text.replace(':', ''))] = lista_elementos[indice + 1].text
            if elemento.text == 'Sistema Emisión de Comprobante:':
                resultado[mapeo_resultado(elemento.text.replace(':', ''))] = lista_elementos[indice + 1].text
            if elemento.text == 'Actividad Comercio Exterior:':
                resultado[mapeo_resultado(elemento.text.replace(':', ''))] = lista_elementos[indice + 1].text                          

        return 0 # Si todo es correcto
    except NoSuchElementException:
        print("No se encontró el elemento col-sm-3 en esta fila.")
        return 1 # Si hubo un error    
    

def mapeo_valores_sm12(row):
    try:
        elemento__sm_12 = row.find_element(By.CLASS_NAME, "col-sm-12")
        resultado["importante"] = elemento__sm_12.text                          

    except NoSuchElementException:
        print("No se encontró el elemento col-sm-12 en esta fila.")
        return 1 # Si hubo un error   
    
def agregar_valores_defecto(variable_ruc):
    resultado['fechaBusqueda'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado['numeroRuc'] = variable_ruc

    if 'importante' in resultado:
        print("El valor IMPORTANTE EXISTE")
    else:
        print("El valor IMPORTANTE NO EXISTE")
        resultado["importante"] = ''
    
def mapeo_resultado(nombreValor):
    if nombreValor == 'Número de RUC':
        nombreValor = 'razonSocial'
    elif nombreValor == 'Tipo Contribuyente':
        nombreValor = 'tipoContribuyente'
    elif nombreValor == 'Nombre Comercial':
        nombreValor = 'nombreComercial'
    elif nombreValor == 'Fecha de Inscripción':
        nombreValor = 'fechaInscripcion'
    elif nombreValor == 'Fecha de Inicio de Actividades':
        nombreValor = 'fechaInicioActividades'   
    elif nombreValor == 'Estado del Contribuyente':
        nombreValor = 'estadoContribuyente'   
    elif nombreValor == 'Condición del Contribuyente':
        nombreValor = 'condicionContribuyente'   
    elif nombreValor == 'Domicilio Fiscal':
        nombreValor = 'domicilioFiscal'    
    elif nombreValor == 'Sistema Emisión de Comprobante':
        nombreValor = 'sistemaEmisionComprobante'           
    elif nombreValor == 'Actividad Comercio Exterior':
        nombreValor = 'actividadComercioInterior'       
    elif nombreValor == 'Sistema Contabilidad':
        nombreValor = 'sistemaContabilidad'
    elif nombreValor == 'Actividad(es) Económica(s)':
        nombreValor = 'actividadesEconomicas'    
    elif nombreValor == 'Emisor electrónico desde':
        nombreValor = 'emisorElectronicoDesde'
    elif nombreValor == 'Comprobantes Electrónicos':
        nombreValor = 'comprobantesElectronicos' 
    elif nombreValor == 'Afiliado al PLE desde':
        nombreValor = 'afiliadoAlPLEDesde'     
    elif nombreValor == 'Padrones':
        nombreValor = 'padrones'   
    elif nombreValor == 'Importante':
        nombreValor = 'importante'                                                                            
    return nombreValor    

# iniciarProceso()