# AI-powered quote extractor tool made for streamlining quote usage decisions

A small anthropic powered AI tool that helps journalists cut down the time spent re-reading raw interview transcripts looking for the strongest, most quotable lines.

Paste a transcript in, get back the top quotes, who said them, and a short note on why each one is worth using after getting a hold of your narrative tone. This features allows it to be effortlessly dropped into a draft. 

## Why

Anyone who's transcribed an interview knows the real work is tediously re-reading forty-five minutes of conversation to find the
five lines that actually make it into the piece. This automates that first pass so the writer can spend their time on judgment calls and reinforcing the language or points instead of scanning piles upon piles of transcripts.

## How it works

The transcript is sent to identify the strongest quotes (by criteria like surprise, emotional weight, and concision), attribute
each to a speaker, and explain briefly why it stands out. Results are shown in the app and can be exported as a `.txt` file.

## Tech

- Python
- Streamlit (UI)
- Anthropic API (quote extraction)

## Possible next steps

- Support audio upload with transcription built in
- Let users tune the "voice" of extracted quotes (hard news vs. feature style)
- Batch mode for multiple transcripts at once
