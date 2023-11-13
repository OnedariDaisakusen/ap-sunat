
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
    PROXY = "123.30.154.171:7777"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    #Usamos firefox como navegador
    # options = webdriver.FirefoxOptions()

    # # Usamos chrome como navegador
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument('--proxy-server=%s' % PROXY)    
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

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
    # imput_ruc.send_keys('20487988023')
    imput_ruc.send_keys('20469378561')

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
        cod_result_bloque1 = 0
        cod_result_bloque2 = 0
        cod_result_bloque3 = 0
       
        for fila in filas_resultado:
            try:
                # Cada list-group-item puede tener uno o mas rows#driver.quit()
                elemento_row = fila.find_element(By.CLASS_NAME, "row")
                # print('Se ingreso en el bloque 1')
                # print('elemento_row', elemento_row.text)

                # # Este bloque try obtiene de la etiqueta row las etiquetas col-sm-5 / col-sm-7
                cod_result_bloque1 = obtenerValoresComunesBloque1(elemento_row)

                if cod_result_bloque1 == 1:
                    #cod_result_bloque2 = obtenerValoresComunesBloque2(elemento_row)
                    #print('Se ingreso en el bloque 2')
                    #print(elemento_row.text)
                    nombre_valor = elemento_row.find_element(By.CLASS_NAME, "col-sm-3")
                    print('col-sm-3 - campos',nombre_valor.text )

                # if cod_result_bloque2 == 1:
                #     print('Se ingreso en el bloque 3')
                # # Este bloque try obtiene de la etiqueta row las etiquetas col-sm-5 / col-sm-7
                # try:
                #     nombre_valor = elemento_row.find_element(By.CLASS_NAME, "col-sm-5")
                #     nombre_valor_text = nombre_valor.text.replace(':', '')

                #     valor = elemento_row.find_element(By.CLASS_NAME, "col-sm-7")
                #     valor_text = valor.text

                #     resultado[mapeo_resultado(nombre_valor_text)] = valor_text
                # except NoSuchElementException:
                #     print("No se encontró el elemento col-sm-5 / col-sm-7 en esta fila.")
                #     # Este bloque try obtiene de la etiqueta row las etiquetas col-sm-3, que es exclusivo del campo Fecha de Inscripción:/ Fecha de Inicio de Actividades:
                #     try:
                #         fechas_ins_act = elemento_row.find_element(By.CLASS_NAME, "col-sm-3")
                #         print('Aqui esta el elemento que buscas: ', fechas_ins_act.text)
                #         # for fecha in fechas_ins_act:
                #         #     fecha_h4 = fecha.find_element(By.TAG_NAME, "h4")
                #         #     fecha_h4_text = fecha_h4.text.replace(':', '')

                #         #     fecha_p = fecha.find_element(By.TAG_NAME, "p")
                #         #     fecha_p_text = fecha_p.text.replace(':', '')                        

                #         #     resultado[mapeo_resultado(fecha_h4_text)] = fecha_p_text

                #     except NoSuchElementException:
                #         print("No se encontró el elemento col-sm-3 en esta fila.")   

               
            except NoSuchElementException:
                print("No se encontró el elemento row en esta fila.")
            cod_result_bloque1 = 0
            cod_result_bloque2 = 0
            cod_result_bloque3 = 0
        #agregar_valores_defecto('20487988023')
        #print(resultado)
        #insertar_resultado(resultado)                            
    except NoSuchElementException: 
        print("Hubo un error al obtener el elemento list-group") 
        #driver.quit()

    #driver.quit()  
    # time.sleep(random.randint(1, 10))
    driver.quit()  



def obtenerValoresComunesBloque1(row):
    try:
        nombre_valor = row.find_element(By.CLASS_NAME, "col-sm-5")
        nombre_valor_text = nombre_valor.text.replace(':', '')

        valor = row.find_element(By.CLASS_NAME, "col-sm-7")
        valor_text = valor.text

        resultado[mapeo_resultado(nombre_valor_text)] = valor_text
        return 0 # Si todo es correcto
    except NoSuchElementException:
        print("No se encontró el elemento row en esta fila.")
        return 1 # Si hubo un error
    
def obtenerValoresComunesBloque2(row):
    try:
        nombre_valor = row.find_element(By.CLASS_NAME, "col-sm-3")
        print('col-sm-3 - campos',nombre_valor.text )
        return 0 # Si todo es correcto
    except NoSuchElementException:
        print("No se encontró el elemento col-sm-3 en esta fila.")
        return 1 # Si hubo un error    
    
def agregar_valores_defecto(ruc):
    resultado['fechaBusqueda'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado['numeroRuc'] = ruc
    resultado['fechaInscripcion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado['fechaInicioActividades'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado['sistemaEmisionComprobante'] = ''
    resultado['actividadComercioInterior'] = ''
    resultado['importante'] = ''
    
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
        nombreValor = 'domicilioFiscal'           
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



iniciarProceso()