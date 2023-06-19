import os
import azure.cognitiveservices.speech as speechsdk

def recognize_from_file(audio_file):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_key = 'bb8bd625ed4e4a4ba60392152e02eb7c'
    speech_region = 'eastus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "es-MX"

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

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


# Ruta del archivo de audio que deseas transcribir
audio_file = "C:/Users/jalex/Documents/ESCOM IPN/ESCOM 7TH SEM/SISTEMAS DISTRIBUIDOS/P8-AZURE/txt.wav"

# Llamar a la función de reconocimiento de voz desde el archivo de audio
recognize_from_file(audio_file)
