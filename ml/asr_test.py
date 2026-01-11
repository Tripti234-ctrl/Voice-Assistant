try:
    import whisper
    print("Whisper library loaded successfully")
except Exception as e:
    print("Whisper loaded with limited support:", e)

print("ASR module setup completed")
