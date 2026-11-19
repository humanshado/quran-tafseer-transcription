#!/usr/bin/env python3
"""Split an enhanced MP3 into service-safe chunks and transcribe each chunk."""
import argparse, subprocess
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('audio', type=Path)
p.add_argument('output_dir', type=Path)
p.add_argument('--chunk-seconds', type=int, default=300)
a=p.parse_args(); a.output_dir.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(a.audio),'-f','segment','-segment_time',str(a.chunk_seconds),'-reset_timestamps','1','-c:a','copy',str(a.output_dir/'chunk_%02d.mp3')],check=True)
chunks=sorted(a.output_dir.glob('chunk_*.mp3'))
for i,c in enumerate(chunks,1):
    out=a.output_dir/(c.stem+'.txt')
    print(f'TRANSCRIBING {i}/{len(chunks)} {c.name}',flush=True)
    with out.open('w',encoding='utf-8') as h:
        subprocess.run(['manus-speech-to-text',str(c),'--granularity','segment','--terminal-max-len-single','5000'],stdout=h,stderr=subprocess.STDOUT,check=True)
print(f'Completed {len(chunks)} chunks')
