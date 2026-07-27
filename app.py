"""
Quote Extractor for Journalists
--------------------------------
Paste a raw interview transcript and get back the strongest,
most publishable quotes -- with speaker attribution and a short
note on *why* each quote is strong.

Run locally:
    streamlit run app.py

Requires an Anthropic API key set as the ANTHROPIC_API_KEY
environment variable (see README.md for setup).
"""

import os
import json
import streamlit as st
import anthropic


# ---------- Page setup ----------

st.set_page_config(
    page_title="Quote Extractor",
    page_icon="📝",
    layout="centered",
)

st.title("📝 Quote Extractor")
st.caption("Paste a messy interview transcript. Get back the lines worth quoting.")


# ---------- API client ----------

def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error(
            "No API key found. Set the ANTHROPIC_API_KEY environment variable "
            "before running the app (see README.md)."
        )
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


# ---------- Core extraction logic ----------

EXTRACTION_PROMPT = """You are helping a journalist quickly find the best quotes \
in a raw interview transcript.

Read the transcript below and select the {num_quotes} strongest, most \
publishable quotes. For each one:
- Attribute it to a speaker if the transcript makes that identifiable \
(otherwise use "Unknown speaker").
- Give a short reason (5-12 words) why it's strong: e.g. surprising, \
concise, emotionally charged, controversial, quotable soundbite, reveals \
character, etc.
- Quote the speaker's words as closely to verbatim as the transcript allows, \
lightly cleaned of filler words ("um", "you know") but not paraphrased.

Return ONLY valid JSON, no other text, no markdown code fences, in this \
exact shape:

{{
  "quotes": [
    {{"speaker": "...", "quote": "...", "reason": "..."}}
  ]
}}

Transcript:
---
{transcript}
---
"""


def extract_quotes(client, transcript: str, num_quotes: int = 5) -> list:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_PROMPT.format(
                    num_quotes=num_quotes, transcript=transcript
                ),
            }
        ],
    )

    raw_text = "".join(
        block.text for block in message.content if block.type == "text"
    ).strip()

    # Models sometimes wrap JSON in code fences despite instructions -- strip them.
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.lower().startswith("json"):
            raw_text = raw_text[4:].strip()

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        st.error("Couldn't parse a response. Try again, or shorten the transcript.")
        st.code(raw_text)
        return []

    return data.get("quotes", [])


# ---------- UI ----------

with st.form("transcript_form"):
    transcript = st.text_area(
        "Paste your transcript here",
        height=300,
        placeholder=(
            "SPEAKER A: So when did you first realize the project wasn't "
            "going to work?\n\nSPEAKER B: Honestly? Week two. Everyone else "
            "kept saying it would turn around, but I already knew..."
        ),
    )
    num_quotes = st.slider("Number of quotes to extract", min_value=3, max_value=10, value=5)
    submitted = st.form_submit_button("Extract quotes", type="primary")

if submitted:
    if not transcript.strip():
        st.warning("Paste a transcript first.")
    else:
        client = get_client()
        with st.spinner("Reading through the transcript..."):
            quotes = extract_quotes(client, transcript, num_quotes)

        if quotes:
            st.subheader(f"Top {len(quotes)} quotes")
            for i, q in enumerate(quotes, start=1):
                with st.container(border=True):
                    st.markdown(f"**\u201c{q.get('quote', '')}\u201d**")
                    st.caption(
                        f"— {q.get('speaker', 'Unknown speaker')} · "
                        f"{q.get('reason', '')}"
                    )

            # Let the journalist copy everything at once
            export_text = "\n\n".join(
                f'"{q.get("quote", "")}" — {q.get("speaker", "Unknown speaker")}'
                for q in quotes
            )
            st.download_button(
                "Download as .txt",
                data=export_text,
                file_name="extracted_quotes.txt",
                mime="text/plain",
            )
