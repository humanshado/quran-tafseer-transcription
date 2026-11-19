#!/usr/bin/env python3
"""Validate a merged transcript JSON without judging uncertain wording."""
import argparse, json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('json_file',type=Path); a=p.parse_args()
d=json.loads(a.json_file.read_text(encoding='utf-8')); s=d.get('segments',[])
assert s, 'no segments'
assert all(x.get('text','').strip() for x in s), 'empty display text'
assert all(s[i]['start'] <= s[i+1]['start'] for i in range(len(s)-1)), 'segments not chronological'
assert all(s[i]['end'] <= s[i+1]['start'] for i in range(len(s)-1)), 'overlapping segments'
print('segments=',len(s))
print('first_start=',s[0]['start'],'last_end=',s[-1]['end'])
print('low_confidence=',sum(x.get('confidence')=='low' for x in s))
print('arabic_fields=',sum(bool(x.get('arabicText')) for x in s))
print('source_chunks=',sorted({x.get('sourceChunk') for x in s}))
