import whisper

model = whisper.load_model("base")

audio_path = "mlsample_audio/garhwali_sample.wav"

result = model.transcribe(audio_path)

print("Detected Text:")
print(result["text"])
