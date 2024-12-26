
from gradio_client import Client

# import applio
# time.sleep(7)
client = Client("http://127.0.0.1:6969/")


def cara_tts(text, name): 
    result = client.predict(
    tts_text=text,                         # Text to Synthesize
    tts_voice="en-US-AriaNeural",           # TTS Voice
    tts_rate=0,                             # TTS Rate
    f0up_key=6,                             # Pitch
    filter_radius=3,                        # Filter Radius
    index_rate=0.75,                        # Search Feature Ratio
    rms_mix_rate=1,                         # Volume Envelope
    protect=0.5,                            # Protect Voiceless Consonants
    hop_length=128,                         # Hop Length
    f0method="rmvpe",                       # Pitch extraction algorithm
    output_tts_path="tts_output.wav",       # Output Path for TTS Audio
    output_rvc_path=f"../{name}",              # Output Path for RVC Audio
    pth_path="logs\\Cd\\CD.pth",            # Voice Model
    index_path="logs\\Cd\\CD.index",        # Index File
    split_audio=False,                      # Split Audio
    f0autotune=False,                       # Autotune
    clean_audio=True,                       # Clean Audio
    clean_strength=0.5,                     # Clean Strength
    export_format="WAV",                    # Export Format
    embedder_model="contentvec",            # Embedder Model
    embedder_model_custom=None,             # Custom Embedder Model (if any)
    upscale_audio=False,                    # Upscale Audio
    api_name="/run_tts_script"              # API name
)
    
    return result[1]


cara_tts("Hello", "Hello.wav")