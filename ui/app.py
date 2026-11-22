"""Streamlit chat UI.   Run:  streamlit run ui/app.py      (the API must be running on port 8000)

The UI never imports assistant_core: it only talks to the backend through the HTTP API.
"""
import os
import sys
import time
import uuid
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so "import ui..." works under streamlit

from ui.api_client import AssistantClient
from ui.logic import EXAMPLES, WELCOME, format_sources, status_note, validate_input

st.set_page_config(page_title="FIT Study Assistant", page_icon="🎓")
client = AssistantClient(os.getenv("ASSISTANT_API_URL", "http://127.0.0.1:8000"))


# ---- Bonus: word-by-word streaming generator --------------------------------
def stream_response(text: str):
    """Yield each word with a short pause to create a typewriter effect."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


# ---- Bonus: render collapsible sources block --------------------------------
def render_sources(sources: list[dict] | str) -> None:
    """Display source documents as collapsible badges inside an expander."""
    if not sources:
        return
    with st.expander("📚 View verified sources"):
        if isinstance(sources, list):
            for s in sources:
                badge = f"`{s['id']}`"
                title = s.get("title", "")
                st.markdown(f"{badge} &nbsp; **{title}**" if title else badge, unsafe_allow_html=True)
        else:
            st.markdown(sources)


# ---- session state: remembered between reruns of this script ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:12]
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
if "rated" not in st.session_state:
    st.session_state.rated = set()

st.title("🎓 FIT Study Assistant")
if not client.healthy():
    st.error("The assistant backend is not reachable. Start it with: uvicorn assistant_api.main:create_app --factory")

with st.sidebar:
    st.subheader("Try an example")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state.pending = ex
    st.caption("This is an AI assistant. Check important decisions with the Training Office.")

# ---- history -------------------------------------------------------------------
for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        # Bonus: show collapsible sources expander for historical messages
        if m.get("raw_sources"):
            render_sources(m["raw_sources"])
        elif m.get("sources"):
            st.caption(m["sources"])
        if m.get("note"):
            st.info(m["note"])
        rid = m.get("request_id")
        if rid and rid not in st.session_state.rated:
            c1, c2, _ = st.columns([1, 1, 6])
            if c1.button("👍", key=f"up{i}"):
                client.send_feedback(rid, 1)
                st.session_state.rated.add(rid)
                st.toast("Thanks for your feedback!")
            if c2.button("👎", key=f"down{i}"):
                client.send_feedback(rid, -1)
                st.session_state.rated.add(rid)
                st.toast("Thanks — we will look at this answer.")

# ---- new question ----------------------------------------------------------------
question = st.chat_input("Ask about fees, offices or the handbook…") or st.session_state.pop("pending", None)
if question:
    problem = validate_input(question)
    if problem:
        st.warning(problem)
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner("Thinking…"):
            result = client.ask(question, st.session_state.session_id)
        if result.ok:
            # Bonus: stream the response word-by-word then store in history
            with st.chat_message("assistant"):
                streamed_text = st.write_stream(stream_response(result.answer))
                render_sources(result.sources)
                note = status_note(result)
                if note:
                    st.info(note)
            st.session_state.messages.append({
                "role": "assistant",
                "content": streamed_text,
                "raw_sources": result.sources,
                "sources": format_sources(result.sources),
                "note": note,
                "request_id": result.request_id,
            }) # type: ignore
        else:
            st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {result.error}"})
            st.rerun()
