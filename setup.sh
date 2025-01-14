#!/bin/sh

set -xe

KOKORO_DIR=Kokoro-82M
WHISPER_DIR=whisper

OS=$(uname)
if [ "$OS" == "Darwin" ]; then
  echo "Running on Darwin, using brew to install packages"
fi

if [ "$OS" == "Linux" ]; then
  echo "Running on Linux, using apt to install packages"
else
  echo "No setup script for you plateform"
  exit 1
fi

if [ ! -d "$KOKORO_DIR" ]; then
  if which git-lfs >/dev/null; then
    echo "You have git-lfs installed already"
  else
    echo "You don't have git-lfs installed, installing it now"

    if [ "$OS" == "Darwin" ]; then
      brew install git-lfs
    else 
      sudo apt install git-lfs -y
    fi
  fi

  echo "Cloning kokoro repo"
  git clone https://huggingface.co/hexgrad/Kokoro-82M
fi

if [ ! -d "$WHISPER_DIR" ]; then
  echo "Cloning whisper repo"
  git clone https://github.com/openai/whisper.git
fi

if which ffmpeg >/dev/null; then
  echo "You have ffmpeg installed"
else
  echo "You don't have ffmpeg installed, installing it now"

  if [ "$OS" == "Darwin" ]; then
    brew install ffmpeg
  else
    sudo apt install ffmpeg -y
  fi
fi

if which python3 >/dev/null; then
  echo "You have python3 installed"
else
  echo "You don't have python3 installed, installing it now"

  if [ "$OS" == "Darwin" ]; then
    brew install python3
  else
    sudo apt install python3 -y
  fi
fi

if which python3-venv >/dev/null; then
  echo "You have python3-venv installed"
else
  echo "You don't have python3-venv installed, installing it now"

  if [ "$OS" == "Darwin" ]; then
    brew install python3-venv
  else
    sudo apt install python3-venv -y
  fi
fi

if which espeak-ng >/dev/null; then
  echo "You have espeak-ng installed"
else
  echo "You don't have espeak-ng installed, installing it now"

  if [ "$OS" == "Darwin" ]; then
    brew install espeak-ng
  else
    sudo apt install espeak-ng -y
  fi
fi

#echo "You need to install ffmpeg, git-lfs, python3, python3-venv, and espeak-ng"
echo "Then to: "
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install phonemizer torch transformers scipy munch openai-whisper"
if [ "$OS" == "Darwin" ]; then
  echo "Warning: You may need to build some python3 packages from source for this to work"
fi
echo "Then you ready to run -> python3 run.py"
