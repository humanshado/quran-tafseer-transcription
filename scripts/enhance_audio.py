#!/usr/bin/env python3
"""Create speech-enhanced WAV/MP3 derivatives without changing the source."""
import argparse, subprocess
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('input', type=Path)
p.add_argument('output_dir', type=Path)
a=p.parse_args(); a.output_dir.mkdir(parents=True, exist_ok=True)
stem=a.input.stem+'_enhanced'
wav=a.output_dir/(stem+'.wav'); mp3=a.output_dir/(stem+'.mp3')
subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(a.input),'-af','highpass=f=70,lowpass=f=5000,afftdn=nr=6:nf=-30,loudnorm=I=-18:TP=-2:LRA=9','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)],check=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(wav),'-c:a','libmp3lame','-b:a','64k','-ar','16000','-ac','1',str(mp3)],check=True)
print(wav); print(mp3)
