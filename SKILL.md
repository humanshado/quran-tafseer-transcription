---
name: quran-tafseer-transcription
description: Transcribe multilingual Quran tafsir audio while preserving Hausa commentary, enhancing difficult recordings, rewriting Arabic-script Hausa into Latin Hausa, restoring identifiable Quran quotations to verified Arabic text, and producing structured study notes. Use for Hausa-Arabic Islamic lecture transcription, re-transcription, speaker/event correction, verse correction, tafsir summaries, revision guides, or examination notes.
---

# Quran Tafsir Transcription

Use this skill for audio commentary that combines Hausa explanation with Arabic Quran recitation or quotations. Preserve the speaker’s Hausa meaning, distinguish recitation from commentary, and clearly separate verified Quran text from editorial normalization.

## Core workflow

1. **Inspect and preserve the source.** Locate the audio, check duration, codec, sample rate, channels, size, and loudness with `ffprobe`/FFmpeg. Never overwrite the original.
2. **Enhance conservatively when requested or when recognition is poor.** Use `scripts/enhance_audio.py` to create a mono 16 kHz WAV and a 64 kbps MP3 derivative. The default chain is mild high-pass/low-pass filtering, noise reduction, and loudness normalization. Enhancement cannot restore information absent from a low-bitrate recording.
3. **Probe before spending a full transcription pass.** Transcribe a short 30–60 second sample. If the service reports insufficient credits, stop and report the blocker; do not retry repeatedly. If accepted, continue.
4. **Transcribe service-safe aligned chunks.** Use `scripts/transcribe_aligned_chunks.py` on the enhanced MP3, normally with five-minute chunks. Keep chunk order and cumulative offsets. If a chunk returns an empty result despite containing audio, retry only that chunk in 60-second subchunks. Preserve every raw `.txt` and JSON output.
5. **Merge without losing content.** Combine timestamped segments chronologically, add cumulative offsets, retain raw ASR text, and never silently delete uncertain speech. Validate with `scripts/validate_transcript.py`.
6. **Separate languages carefully.** The speech-to-text language label may be wrong for mixed Hausa-Arabic audio. Treat the actual words and context as primary. Latin Hausa commentary is the display default; Quran and verified Arabic quotations remain Arabic script.
7. **Normalize Arabic-script Hausa.** When Hausa is emitted in Arabic/Arabic-like characters, do not apply a mechanical character substitution. Use contextual re-transcription or careful normalization into standard Latin Hausa. Preserve `rawText`, write normalized Hausa in `text`/`latinHausa`, record `confidence` and `note`, and mark doubtful words for human review. Never present a guess as certain.
8. **Classify events.** Use `quran_arabic`/`recitation` for identifiable Quran, `hadith_or_arabic_quote` for other Arabic quotations, `commentary` for Hausa explanation, and `uncertain` when classification or wording is unresolved. Do not label Arabic-script Hausa as unmatched recitation merely because its script is Arabic.
9. **Identify Quran quotations.** Match recognizable phonetic or partial Arabic quotations to the likely surah and ayah. Verify with authoritative Quran sources such as Quran.com or Tanzil. Never invent or improve an uncertain quotation.
10. **Present verified Arabic separately.** Put corrected Quran text in a dedicated verse section with surah and ayah references. In the timestamped transcript retain the raw text and editorial correction relationship.
11. **Create educational notes when requested.** Organize notes by surah and ayah, then add meaning, tafsir themes, theological distinctions, practical lessons, revision points, examination questions, a practice quiz with model answers, and a glossary. Place the quiz and answers immediately before the glossary.
12. **Verify and deliver.** Check file existence, segment count, chunk coverage, duration, ordering, overlap, Arabic references, low-confidence flags, and that all source chunks are represented. Deliver Markdown for reading and JSON for application use; package both only when useful.

## Credit and failure handling

- Run a small probe before a full service call.
- On `402 Payment Required` or an explicit insufficient-credit response, stop the batch and report it. Do not keep retrying.
- On empty output with non-silent audio, retry that chunk with shorter subchunks; do not redo successful chunks.
- Keep the original audio, enhanced audio, raw ASR, normalized JSON, and final Markdown as separate artifacts.

## Quran text and theology safeguards

- Preserve Quran in Arabic script, not only transliteration.
- Include surah name, number, and ayah number for every quoted passage.
- Do not attribute tafsir opinion to the Quran itself; label it as commentary.
- Distinguish major hypocrisy (`نفاق أكبر`) from practical hypocrisy (`نفاق عملي`) when the commentary makes that distinction.
- Avoid declaring a named person a disbeliever or hypocrite; explain categories and traits academically.
- When explaining divine attributes, preserve the commentary’s intended distinction between attributes of perfection and contextual expressions of recompense.
- Quote hadith only when wording is well known or verified; otherwise identify it as a hadith reference mentioned in the lecture.
- If an Arabic verse is not confidently identified, keep it uncertain rather than fabricating a correction.

## Recommended output structure

For a complete transcript:

```markdown
# Tafsir Audio Transcript — [filename]
## Processing note
[Source, enhancement, chunking, and normalization method]
## Verified Quranic Text
[Arabic verses with references]
## Complete Timestamped Transcription
[raw/normalized text in chronological order]
## Editorial note
[what was corrected, what remains uncertain, and source policy]
## Sources
[Quran verification links]
```

For application JSON, retain at minimum: `id`, `start`, `end`, `rawText`, `text`, `type`, `arabicText`, `confidence`, `note`, and `sourceChunk`.

## Quality checklist

Before delivery, confirm:

- The complete audio was transcribed, including every chunk and any recovered subchunks.
- Hausa commentary is in Latin Hausa unless the user explicitly requests another script.
- Arabic Quran quotations are verified, in Arabic, and referenced.
- Original timestamps remain available and chronological.
- No overlapping merged segments were introduced.
- Raw ASR remains available for audit.
- Uncertain Hausa is marked rather than guessed silently.
- Arabic-script Hausa is not misclassified as unmatched recitation.
- Educational summaries distinguish Quranic text, tafsir explanation, and editorial additions.
- Student notes include a revision quiz with answers before the glossary.
