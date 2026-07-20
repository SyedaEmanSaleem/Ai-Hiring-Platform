"""
Optional LLM plug-in point.

The platform works fully offline using rule-based logic (see
question_generator.py and interview_conductor.py). If you want smarter,
more natural question generation and answer scoring, set an API key as an
environment variable and flip USE_LLM = True.

This wrapper is provider-agnostic on purpose. Fill in `call_llm` with
whichever SDK you use (Anthropic, OpenAI, etc). Example for Anthropic is
sketched below (commented out) so you can wire it up quickly.
"""
import os

USE_LLM = False  # flip to True once you've configured a provider below


def call_llm(prompt: str, max_tokens: int = 400) -> str:
    """
    Sends `prompt` to an LLM and returns the text response.
    Replace the body with a real API call. Example (Anthropic):

        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text

    Until configured, this raises so callers fall back to rule-based logic.
    """
    if not USE_LLM:
        raise RuntimeError("LLM disabled (USE_LLM=False) — using rule-based fallback.")
    raise NotImplementedError("Wire up your LLM provider in llm_client.call_llm().")
