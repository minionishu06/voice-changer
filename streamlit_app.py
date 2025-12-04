import streamlit as st
import io
from pydub import AudioSegment

st.title("🎵 Voice Changer Web App")
st.write("Upload an MP3 or WAV file, adjust speed and pitch, then download the modified audio.")

uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav'])

if uploaded_file:
    # Load original audio
    sound = AudioSegment.from_file(uploaded_file)
    st.success(f"✅ Loaded audio duration: {len(sound)/1000:.1f} seconds")
    st.audio(uploaded_file)
    
    # Speed and pitch controls
    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Speed (0.5 = slow, 2 = fast)", 0.5, 2.0, 1.0, 0.1)
    with col2:
        pitch = st.slider("Pitch (0.5 = deeper, 1.5 = higher)", 0.5, 1.5, 1.0, 0.1)
    
    if st.button("🎵 Modify & Download"):
        with st.spinner("Processing audio..."):
            # Change speed
            new_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
            # Change pitch
            new_sound = new_sound._spawn(new_sound.raw_data, overrides={"frame_rate": int(new_sound.frame_rate * pitch)})
            # Reset frame rate
            new_sound = new_sound.set_frame_rate(sound.frame_rate)
            
            # Export to buffer
            buffer = io.BytesIO()
            new_sound.export(buffer, format="wav")
            buffer.seek(0)
            
            # Playback and download
            st.audio(buffer)
            st.download_button(
                label="📥 Download Modified Audio",
                data=buffer,
                file_name="modified_audio.wav",
                mime="audio/wav"
            )
            st.balloons()
