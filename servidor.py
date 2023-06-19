import logging
import xmlrpc.server
import os
import azure.cognitiveservices.speech as speechsdk


logging.basicConfig(filename='C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/log/server.log', level=logging.DEBUG,filemode='w', 
                    format='%(asctime)s | %(levelname)s:%(message)s | %(threadName)s | %(funcName)s | %(lineno)d|')

def reconoce(audio_file):
    logging.info(f"Transcribiendo audio {audio_file}")
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_key = 'bb8bd625ed4e4a4ba60392152e02eb7c'
    speech_region = 'eastus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "es-MX"
    logging.debug(f"speech_config: {speech_config}")
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    logging.debug("Transcribiendo audio...")
    print("Transcribiendo audio...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Reconoci esto: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return result.text


# Ruta del archivo de audio que deseas transcribir
#audio_file = "C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/txt.wav"

# Llamar a la función de reconocimiento de voz desde el archivo de audio
# reconoce(audio_file)

def handle_connection(client_ip):
    # Registra la conexión en la bitácora
    logging.info(f"Cliente {client_ip} se ha conectado")

try:
    logging.debug("Iniciando servidor")
    server = xmlrpc.server.SimpleXMLRPCServer(("192.168.1.183", 3312))
    logging.debug("Servidor iniciado")
except:
    logging.debug("No se pudo iniciar el servidor")
    print("No se pudo iniciar el servidor")

print("Esperando transcripciones de audios... en la IP: 192.168.1.75 y puerto: 3312")

server.register_function(handle_connection, "_dispatch")

server.register_function(reconoce, "reconoce")

server.serve_forever()

