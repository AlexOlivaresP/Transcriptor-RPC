import os
import azure.cognitiveservices.speech as speechsdk

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_key = 'bb8bd625ed4e4a4ba60392152e02eb7c'
    speech_region = 'eastus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

    speech_config.speech_recognition_language="es-MX"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Habla a tu microfono.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Escuche: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No pude reconocer: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Cancelado: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error: {}".format(cancellation_details.error_details))
            print("Tas bien mano?")

recognize_from_microphone()