import whisper

model = whisper.load_model("base")
result = model.transcribe("ml/sample_audio/test.wav")

print("Recognized Text:")
print(result["text"])
