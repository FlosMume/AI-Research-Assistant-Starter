"""
Minimal CLI to run the pipeline without the server.

Usage:
  python cli.py --query "Your question"
  python cli.py --audio path/to/file.wav
"""
import argparse, sys, json
from state import current_session
from tools.asr import transcribe_audio
from tools.retriever import retrieve_arxiv_passages
from tools.llm import summarize_passages
from tools.tts import speak_or_save

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", type=str, default=None)
    ap.add_argument("--audio", type=str, default=None)
    args = ap.parse_args()

    if not args.query and not args.audio:
        print("Provide --query or --audio")
        sys.exit(1)

    if args.audio:
        with open(args.audio, "rb") as f:
            q = transcribe_audio(f.read())
            current_session.add("user", f"[audio] {q}", source="audio")
    else:
        q = args.query
        current_session.add("user", q, source="text")

    passages, citations = retrieve_arxiv_passages(q)
    answer = summarize_passages(q, passages)
    wav = speak_or_save(answer)
    current_session.add("assistant", answer, citations=citations, tts=wav)

    print(json.dumps({
        "session_id": current_session.session_id,
        "query": q,
        "answer": answer,
        "citations": citations,
        "tts_wav": wav
    }, indent=2))

if __name__ == "__main__":
    main()
