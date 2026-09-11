"""The fixed schema the labeller must speak, in the v2 primitive vocabulary.

The labeller now emits the *same primitives the static scanner does* — reads of a sensitive
resource, an outward send, an execution, a write to agent state, and the framing claims —
so a resource or channel the model recognises but the regexes did not lands on the exact
predicates the rules compose. This is where the LLM covers static's blind spots (an OOD
credential store, an unusual egress, a novel injection phrasing) instead of running as a
parallel, differently-shaped labeller.

The two hard rules from CLAUDE.md still hold and are enforced here:

* **No verdict.** The vocabulary is observations only — there is no "malicious", no score.
* **Off-schema output is dropped, not repaired**, because the labelled text is adversarial.

Each label carries the exact `quote` it reacts to, so the fact earns a real source span
(the quote is located back in the chunk) and a fabricated quote simply fails to anchor.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError

# The closed label vocabulary. Each maps to a primitive fact in labeller._LABEL_MAP. Flat
# labels (rather than predicate+args) keep the model's job simple and validation strict.
Observation = Literal[
    "reads_sensitive",  # reads credentials, keys, tokens, secrets
    "reads_personal",  # reads user PII, conversation/context, browser data
    "sends_outward",  # transmits data out of the environment (any channel)
    "fetches_remote",  # pulls code or data in from the network
    "executes_code",  # runs code, a shell, or a subprocess
    "writes_agent_state",  # writes agent memory/config (CLAUDE.md, .claude, shell rc)
    "overrides_constraints",  # directs the agent to disregard governing instructions
    "claims_authority",  # asserts control over the agent / precedence over the user
    "asks_to_conceal",  # asks to hide or not mention something to the user
    "claims_persistent",  # declares its instructions standing/binding beyond the task
    "misrepresents",  # tells the user it does one thing while doing another
    "instructs_agent",  # directs the agent to perform an action
]


class Label(BaseModel):
    model_config = {"extra": "forbid"}

    observation: Observation
    quote: str = Field(min_length=1, max_length=600)
    confidence: float = Field(ge=0.0, le=1.0)
    detail: str = Field(default="", max_length=120)


class ChunkLabels(BaseModel):
    model_config = {"extra": "forbid"}

    labels: list[Label] = Field(default_factory=list, max_length=24)


def parse_labels(raw: object) -> list[Label]:
    """Validate model output into labels, discarding anything off-schema. Never raises."""
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
