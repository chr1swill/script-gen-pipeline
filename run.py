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
    if text_arr[i].isspace():
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
][0]    # 0 (f) and 4 (m) sound the best to me
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

comment = "# " + time.strftime("%Y-%m-%d--%H-%M") + \
    " Audio inputs to join together\n"

try:
    os.makedirs(wav_pieces_dir)
except: 
    pass

ffmpeg_inputs_file = open(ffmpeg_inputs_file_path, "a")
ffmpeg_inputs_file.write(comment)
print(f"Create file: {ffmpeg_inputs_file_path} with timestamp commnet")

i = 0
for sentence in text_arr:
    audio, out_ps = generate(MODEL, sentence, VOICEPACK, lang=VOICE_NAME[0])

    file_path = wav_pieces_dir + str(i) + ".wav"
    write(file_path, rate=24000, data=audio)
    print(f"Wrote audio data to file: {file_path}")

    current_input = "file '" + str(i) + ".wav" + "'\n"
    ffmpeg_inputs_file.write(current_input)
    print(f"Added input file: {file_path} to ffmpeg inputs file")
    i += 1

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
