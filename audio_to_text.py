import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


def convert_audio_to_text(file_path):
    recognizer = sr.Recognizer()

    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Split the audio into chunks based on silence
    chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=-40)

    transcript = ""

    for i, chunk in enumerate(chunks):
        # Check the length of the chunk
        if len(chunk) < 1000:  # Less than 1 second
            print("Skipping chunk because it's too short")
            continue

        chunk.export("temp_chunk.wav", format="wav")

        with sr.AudioFile("temp_chunk.wav") as source:
            # Read the entire audio file
            audio_data = recognizer.record(source)

            # Recognize the speech in the audio chunk
            try:
                audio_text = recognizer.recognize_google(audio_data)
                transcript += f"{audio_text} "
            except sr.UnknownValueError:
                print("Could not understand the audio")
            except sr.RequestError as e:
                print(f"Error occurred: {str(e)}")

    return transcript


if __name__ == "__main__":
    file_path = "Recording.wav"  # Replace this with the path to your audio file
    transcript = convert_audio_to_text(file_path)

    # Write the transcript to a .txt file
    with open("transcript.txt", "w") as file:
        file.write(transcript)

    # print(transcript)
