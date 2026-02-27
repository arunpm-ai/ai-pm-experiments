"""
Simple AI Text Insight Analyzer
--------------------------------
A beginner-friendly Streamlit app that turns long text into:
1) A short summary
2) Key insights
3) Action items
"""

from collections import Counter
from typing import List
import re
import streamlit as st


# -----------------------------
# Helper function: break text into sentences
# -----------------------------
def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using simple punctuation rules."""
    cleaned = re.sub(r"\s+", " ", text.strip())
    if not cleaned:
        return []
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]


# -----------------------------
# Helper function: create a short summary
# -----------------------------
def generate_summary(sentences: List[str], max_sentences: int = 2) -> str:
    """Create a short summary by taking the first few sentences."""
    if not sentences:
        return "Please paste some text first."
    return " ".join(sentences[:max_sentences])


# -----------------------------
# Helper function: extract key insights
# -----------------------------
def generate_key_insights(text: str, top_n: int = 5) -> List[str]:
    """Find simple keyword-based insights from repeated important words."""
    stop_words = {
        "the", "a", "an", "and", "or", "but", "if", "then", "for", "to", "of", "in",
        "on", "with", "at", "by", "from", "is", "are", "was", "were", "be", "been", "being",
        "it", "this", "that", "these", "those", "as", "we", "you", "they", "he", "she", "i",
        "our", "your", "their", "not", "can", "could", "should", "would", "will", "may", "might",
    }

    words = re.findall(r"[A-Za-z']+", text.lower())
    important_words = [w for w in words if w not in stop_words and len(w) > 2]

    if not important_words:
        return ["Not enough meaningful words to extract insights yet."]

    most_common = Counter(important_words).most_common(top_n)
    return [f"'{word}' is a repeated theme (mentioned {count} times)." for word, count in most_common]


# -----------------------------
# Helper function: identify action items
# -----------------------------
def generate_action_items(sentences: List[str]) -> List[str]:
    """Create action items by picking sentences that sound like tasks."""
    action_triggers = (
        "should", "need to", "must", "action", "todo", "follow up", "next step", "assign", "deadline"
    )

    actions = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(trigger in lower for trigger in action_triggers):
            actions.append(sentence)

    # Fallback if no clear action language is found
    if not actions:
        actions = [
            "Review the text and identify the top 1–2 priorities.",
            "Assign an owner for each priority.",
            "Set a target date for completion.",
        ]

    return actions[:5]


# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="AI Text Insight Analyzer", page_icon="📝", layout="centered")

st.title("📝 AI Text Insight Analyzer")
st.write(
    "Paste any notes, report, or meeting text below. "
    "Click **Analyze Text** to get a summary, insights, and action items."
)


# -----------------------------
# Main input area
# -----------------------------
user_text = st.text_area(
    "Paste your text here:",
    height=220,
    placeholder="Example: Meeting notes, project update, customer feedback...",
)


# -----------------------------
# Analyze button logic
# -----------------------------
if st.button("Analyze Text"):
    if not user_text.strip():
        st.warning("Please paste some text before clicking Analyze Text.")
    else:
        sentences = split_into_sentences(user_text)
        summary = generate_summary(sentences)
        insights = generate_key_insights(user_text)
        actions = generate_action_items(sentences)

        st.subheader("1) Short Summary")
        st.write(summary)

        st.subheader("2) Key Insights")
        for insight in insights:
            st.markdown(f"- {insight}")

        st.subheader("3) Action Items")
        for item in actions:
            st.markdown(f"- {item}")


# -----------------------------
# Extra help for first-time users
# -----------------------------
with st.expander("How this works (simple explanation)"):
    st.write(
        "This app uses very simple text rules (not a complex AI model):\n"
        "- Summary: first 1–2 sentences\n"
        "- Key insights: repeated important words\n"
        "- Action items: sentences that look like tasks"
    )
