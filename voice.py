import os
import io
import wave
import tempfile

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def record_audio(filename='recording.wav', duration=30):
    """Record audio from microphone and save to file."""
    if not PYAUDIO_AVAILABLE:
        raise RuntimeError("PyAudio not installed. Please use file upload instead.")

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )

    frames = []
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename


def transcribe_audio_file(audio_file) -> str:
    """
    Transcribe audio using Groq Whisper API.
    audio_file: file-like object or path string
    Returns Urdu transcript text.
    """
    if isinstance(audio_file, str):
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()
        filename = os.path.basename(audio_file)
    else:
        audio_bytes = audio_file.read()
        filename = getattr(audio_file, 'name', 'audio.wav')

    # Groq expects a tuple: (filename, bytes, content_type)
    response = client.audio.transcriptions.create(
        model='whisper-large-v3',
        file=(filename, audio_bytes, 'audio/wav'),
        language='ur'
    )
    return response.text


def transcribe_bytes(audio_bytes: bytes, filename: str = 'audio.wav') -> str:
    """Transcribe raw audio bytes."""
    response = client.audio.transcriptions.create(
        model='whisper-large-v3',
        file=(filename, audio_bytes, 'audio/wav'),
        language='ur'
    )
    return response.text
