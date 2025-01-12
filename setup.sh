#!/bin/sh

KOKORO_DIR=Kokoro-82M
WHISPER_DIR=whisper

if [ ! -d "$KOKORO_DIR" ]; then
    git clone https://huggingface.co/hexgrad/Kokoro-82M
fi

if [ ! -d "$WHISPER_DIR" ]; then
    git clone https://github.com/openai/whisper.git
fi

#python3 -m venv venv

#source venv/bin/activate


echo "You need to install ffmpeg, git-lfs, python3, python3-venv, and espeak-ng"
echo "Then to: "
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install phonemizer torch transformers scipy munch openai-whisper"
echo "Then you ready to run -> python3 run.py"
