# Quote Extractor

A small tool that helps journalists cut down the time spent re-reading raw
interview transcripts looking for the strongest, most quotable lines.

Paste a transcript in, get back the top quotes, who said them, and a short
note on why each one is worth using — ready to drop into a draft.

## Why

Anyone who's transcribed an interview knows the real work isn't the
transcription, it's re-reading forty-five minutes of conversation to find the
five lines that actually make it into the piece. This automates that first
pass so the writer can spend their time on judgment calls, not scanning.

## How it works

The transcript is sent to Claude with instructions to identify the strongest
quotes (by criteria like surprise, emotional weight, and concision), attribute
each to a speaker, and explain briefly why it stands out. Results are shown in
the app and can be exported as a `.txt` file.

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get an API key from [console.anthropic.com](https://console.anthropic.com)
   and set it as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```
   (On Windows: `setx ANTHROPIC_API_KEY "your-key-here"`, then restart your terminal.)

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Try it with `sample_transcript.txt` included in this repo, or paste your own.

## Tech

- Python
- Streamlit (UI)
- Anthropic API (quote extraction)

## Possible next steps

- Support audio upload with transcription built in
- Let users tune the "voice" of extracted quotes (hard news vs. feature style)
- Batch mode for multiple transcripts at once
