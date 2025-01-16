import time
from scipy.io.wavfile import write
import sys
import torch
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Kokoro-82M'))
from models import build_model
from kokoro import generate

if len(sys.argv) != 3:
    argc = len(sys.argv)
    print("argc: ")
    print(argc)
    print("Ussage: python3 run.py [path/to/output/dir] '[INPUT_STR]'")
    exit()
else:
    output_path = sys.argv[1]
    text = sys.argv[2]
    print(f'output_path={output_path}')
    print(f'text="{text}"')

if output_path[len(output_path)-1] != '/':
    output_path += '/'
    print(f"Updated output_path to have trailing slash: {output_path}")

text_arr = text.split(".")
print(
    f"Splitting input string into array of senetence for processing:\n{
        text_arr}"
)

i = 0
while (i < len(text_arr)):
    if text_arr[i].isspace() or text_arr[i].strip() == '':
        print(f"Index={i}, value={
            text_arr[i]
        } contained an lonely space char which has been removed"
        )
        text_arr.pop(i)
        continue
    else:
        i += 1

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

MODEL = build_model('Kokoro-82M/kokoro-v0_19.pth', device)
# you can easily test voices here
# -> https://huggingface.co/spaces/hexgrad/Kokoro-TTS
VOICE_NAME = [
    'af',
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', 'af_sky',
][4]    # 0 (f) and 4 (m) sound the best to me
VOICEPACK = torch.load(
    f'Kokoro-82M/voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')


wav_pieces_dir = output_path + "wav-pieces/"
ffmpeg_inputs_file_path = wav_pieces_dir + "myinput.txt"
try:
    os.stat(ffmpeg_inputs_file_path)
    os.remove(ffmpeg_inputs_file_path)
    print(f"File already exists, removing it: {ffmpeg_inputs_file_path}")
except:
    print(f"Creating file: {ffmpeg_inputs_file_path}")
    pass

comment = "# " + time.strftime("%Y-%m-%d--%H-%M") + \
    " Audio inputs to join together\n"

try:
    os.makedirs(wav_pieces_dir)
except:
    pass

ffmpeg_inputs_file = open(ffmpeg_inputs_file_path, "a")
ffmpeg_inputs_file.write(comment)
print(f"Create file: {ffmpeg_inputs_file_path} with timestamp commnet")

# i = 0
print(text_arr)
for i in range(len(text_arr)):
    sentence = text_arr[i]
    print(f"sentence: {sentence}")
    audio, out_ps = generate(MODEL, sentence, VOICEPACK, lang=VOICE_NAME[0], speed=1.5)
    print(f"audio: {audio}")
    print(f"out_ps: {out_ps}")

    file_path = wav_pieces_dir + str(i) + ".wav"
    write(file_path, rate=24000, data=audio)
    print(f"Wrote audio data to file: {file_path}")

    current_input = "file '" + str(i) + ".wav" + "'\n"
    ffmpeg_inputs_file.write(current_input)
    print(f"Added input file: {file_path} to ffmpeg inputs file")
    # i += 1

ffmpeg_inputs_file.close()
ffmpeg_command = "ffmpeg -f concat -safe 0 -i " + ffmpeg_inputs_file_path + \
    " -c copy " + output_path + "final_output.wav"
print(f"Executing ffmpeg command:\n\t{ffmpeg_command}")
os.system(ffmpeg_command)

whisper_command = "whisper " + output_path + \
    "final_output.wav --model tiny --output_dir " + \
    output_path + "subtitles"
print(f"Executing whisper command:\n\t{whisper_command}")
os.system(whisper_command)

# TTS_FILEPATH="code/ai/script-gen-pipeline/output/_intro/final_output.wav"
# TTS_FILEPATH="$ROOT$TTS_FILEPATH"
tts_filepath = output_path + "final_output.wav"

# SUBTITLES_FILEPATH='code/ai/script-gen-pipeline/output/_intro/subtitles/final_output.vtt'
# SUBTITLES_FILEPATH="$ROOT$SUBTITLES_FILEPATH"
subtitle_filepath = output_path + "subtitles/" + "final_output.vtt"

# VIDEO_FILEPATH='Videos/stock-clips/purple-fluid-60.mp4'
# VIDEO_FILEPATH="$ROOT$VIDEO_FILEPATH"
video_filepath = "$HOME/Videos/stock-clips/purple-fluid-60.mp4"

# MUSIC_FILEPATH='Music/royalty-free/caves-of-dawn-10376-reduced-75.mp3'
# MUSIC_FILEPATH="$ROOT$MUSIC_FILEPATH"
music_filepath = "$HOME/Music/royalty-free/caves-of-dawn-10376-reduced-75.mp3"

# OUTPUT_FILEPATH='Downloads/output.mp4'
# OUTPUT_FILEPATH="$ROOT$OUTPUT_FILEPATH"
try:
    os.makedirs(output_path+"final/")
except:
    pass

final_output_filepath = output_path + "final/output.mp4"

# TTS_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ${TTS_FILEPATH})
tts_duration = f"$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {tts_filepath})"

# SUBTITLE_STYLE="force_style='Alignment=10,FontSize=18,FontName=Helvetica,Outline=4,OutlineColor=&HFFFFFFFF,PrimaryColor=&HF00000000'"
subtitle_style = "force_style='Alignment=10,FontSize=18,FontName=Helvetica,Outline=4,OutlineColor=&HFFFFFFFF,PrimaryColor=&HF00000000'"

# ffmpeg -stream_loop -1 -i ${VIDEO_FILEPATH} -i ${TTS_FILEPATH} -i ${MUSIC_FILEPATH} -lavfi "[0:v]subtitles=${SUBTITLES_FILEPATH}:${SUBTITLE_STYLE}[v];[1:a][2:a]amix=inputs=2:duration=longest[a]" -map "[v]" -map "[a]" -t ${TTS_DURATION} -c:v libx264 -c:a aac -b:a 192k ${OUTPUT_FILEPATH}

video_create_command = f"ffmpeg -stream_loop -1 -i {video_filepath} -i {tts_filepath} -i {music_filepath} -lavfi \"[0:v]subtitles={subtitle_filepath}:{subtitle_style}[v];[1:a][2:a]amix=inputs=2:duration=longest[a]\" -map \"[v]\" -map \"[a]\" -t {tts_duration} -c:v libx264 -c:a aac -b:a 192k {final_output_filepath}"

print(f"Executing command to create final video\n\t{video_create_command}")
os.system(video_create_command)
