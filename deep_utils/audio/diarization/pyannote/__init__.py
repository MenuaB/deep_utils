try:
    from deep_utils._dummy_objects.audio.diarization.pyannote import PyannoteAudioDiarization
    from .pyannote_audio_diarization import PyannoteAudioDiarization
except ModuleNotFoundError:
    pass
