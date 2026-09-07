"""The fixed schema the labeller must speak, and nothing else.

Two rules from CLAUDE.md are enforced here rather than hoped for:

* **The labeller never emits a verdict.** There is no "malicious", no score, no severity in
  this schema — only atomic observations. Judgement is the engine's, downstream, on facts
  it can audit. A model that tries to conclude has nowhere to put the conclusion.
* **Off-schema output is dropped, not repaired.** `parse_labels` validates against these
  models and silently discards anything that does not fit, because the thing being labelled
  is adversarial and a "helpful" coercion of malformed output is an injection foothold.

Each predicate mirrors one the design calls for (Imperative, TargetsSensitive, Egress,
AuthorityClaim, Concealment, Persistence). The labeller reports a `quote` — the exact
substring it is reacting to — which is how an LLM assertion earns a real source span:
the quote is located back in the chunk, so a hallucinated quote simply fails to anchor.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# The closed vocabulary. A label naming anything else is discarded.
Predicate = Literal[
    "Imperative",  # the chunk tells the agent to *do* something
    "TargetsSensitive",  # it concerns a credential / key / private resource
    "Egress",  # it moves data outward (network, email, external write)
    "AuthorityClaim",  # it asserts authority over the agent ("ignore previous", "you are now")
    "Concealment",  # it asks to hide, suppress, or not mention something
    "Persistence",  # it asks to write to agent memory / config / autostart
]

SENSITIVE_KINDS = frozenset(
    {
        "credential",
        "ssh_key",
        "api_key",
        "token",
        "password",
        "env_secret",
        "private_file",
        "browser_data",
        "wallet",
        "system_file",
        "other",
    }
)


class Label(BaseModel):
    """One observation about one chunk."""

    model_config = {"extra": "forbid"}

    predicate: Predicate
    quote: str = Field(min_length=1, max_length=600)
    confidence: float = Field(ge=0.0, le=1.0)
    detail: str = Field(default="", max_length=120)


class ChunkLabels(BaseModel):
    """The labeller's entire allowed response for one chunk."""

    model_config = {"extra": "forbid"}

    labels: list[Label] = Field(default_factory=list, max_length=24)


def parse_labels(raw: object) -> list[Label]:
    """Validate model output into labels, discarding anything off-schema.

    Never raises: an adversarial sample may drive the model to emit garbage, and the
    correct response to garbage is to keep the labels that do validate and drop the rest,
    not to fail the whole scan.
    """
    if not isinstance(raw, dict):
        return []
    labels = raw.get("labels")
    if not isinstance(labels, list):
        return []
    out: list[Label] = []
    for item in labels:
        try:
            out.append(Label.model_validate(item))
        except ValidationError:
            continue
    return out
