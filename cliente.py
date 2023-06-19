import sounddevice as sd
import soundfile as sf
import datetime
import os
import concurrent.futures
import time
import xmlrpc.client
import logging

logging.basicConfig(filename='C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/log/cliente.log', level=logging.DEBUG,filemode='w', 
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

# Crear logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Crear manejador para la consola
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Formatear mensaje de log
formatter = logging.Formatter('%(levelname)s || %(message)s')
ch.setFormatter(formatter)

# Agregar manejador al logger
logger.addHandler(ch)

##############################################################################################################

#insertar el audio
def vm(ruta):
    # Crear proxy
    logging.debug("Conectando con VM...")
    #print("CONECTANDO CON VM...")
    proxy = xmlrpc.client.ServerProxy("http://192.168.1.183:3312/RPC2")
    logging.debug("Conectado con VM...")
    #print("CONECTADO CON VM.../n")
    # Llamar función del servidor
    resultado = proxy.reconoce(ruta)
    logging.debug("Respuesta terminada... ")
    #print(resultado)
    # Imprimir resultado
    return resultado


# Función para grabar audio

def record_audio(duration, save_path):
    # Configurar los parámetros de grabación
    sample_rate = 44100  # Tasa de muestreo en Hz
    channels = 2  # Número de canales de audio (estéreo)

    # Iniciar la grabación del audio desde el micrófono
    print("Grabando audio...")
    logging.debug("Grabando audio...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()  # Esperar a que finalice la grabación
    print("Audio terminado...")
    # Generar el nombre de archivo utilizando la fecha y hora actual
    #timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    logging.debug("Audio terminado...")
    file_name = "txt.wav"

    # Crear la ruta completa de guardado del archivo de audio
    save_file_path = os.path.join(save_path, file_name)

    # Guardar el audio grabado en un archivo .wav
    sf.write(save_file_path, audio, sample_rate)

    #print(f"Audio grabado y guardado en '{save_file_path}'.")
    logging.debug(f"Audio grabado y guardado en '{save_file_path}'.")

# Duración de la grabación en segundos
duration = 5

# Ruta de guardado personalizada
save_path = "C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE"

# Llamar a la función para grabar audio
logging.debug("GRABANDO...")
record_audio(duration, save_path)
logging.debug("GRABADO...")
#ejecutor se encarga de ejecutar los hilos de manera concurrente
ejecutor = concurrent.futures.ThreadPoolExecutor()
logging.debug("EJECUTOR INICIADO...")
#se ejecuta el hilo de vm
logging.debug("EJECUTANDO VM...")
hilovm = ejecutor.submit(vm,"C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/txt.wav")
logging.debug("VM EJECUTADA...")


#crear un archivo de texto para guardar el resultado
archivo = open("C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/resultado.txt", "w")
#escribir el resultado en el archivo
archivo.write(hilovm.result())
#cerrar el archivo
archivo.close()
#cerrar el ejecutor
ejecutor.shutdown()
#imprimir el resultado
print("EL RESULTADO DEL AUDIO FUE: ",hilovm.result())
logging.debug("RESULTADO IMPRESO...")
