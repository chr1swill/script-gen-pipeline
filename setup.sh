#!/bin/sh

KOKORO_DIR=Kokoro-82M
WHISPER_DIR=whisper

if [ ! -d "$KOKORO_DIR" ]; then
    if which git-lfs >/dev/null; then
      git clone https://huggingface.co/hexgrad/Kokoro-82M
    else
      sudo apt install git-lfs -y
      git clone https://huggingface.co/hexgrad/Kokoro-82M
    fi
fi

if [ ! -d "$WHISPER_DIR" ]; then
    git clone https://github.com/openai/whisper.git
fi

if which ffmpeg >/dev/null; then
  echo "You have ffmpeg installed"
else
  echo "You don't have ffmpeg installed, installing it now"
  sudo apt install ffmpeg -y
fi

if which python3 >/dev/null; then
  echo "You have python3 installed"
else
  echo "You don't have python3 installed, installing it now"
  sudo apt install python3 -y
fi

if which python3-venv >/dev/null; then
  echo "You have python3-venv installed"
else
  echo "You don't have python3-venv installed, installing it now"
  sudo apt install python3-venv -y
fi

if which espeak-ng >/dev/null; then
  echo "You have espeak-ng installed"
else
  echo "You don't have espeak-ng installed, installing it now"
  sudo apt install espeak-ng -y
fi

#echo "You need to install ffmpeg, git-lfs, python3, python3-venv, and espeak-ng"
echo "Then to: "
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install phonemizer torch transformers scipy munch openai-whisper"
echo "Then you ready to run -> python3 run.py"
