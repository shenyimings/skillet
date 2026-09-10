"""Direct-LLM control: same snapshot/Pi loop, no static facts or Datalog verdict."""

from .host import AgentHost


class PureHost(AgentHost):
    pipeline_mode = "pure"

    def __init__(self, *args, **kwargs):
        self.decision = None
        super().__init__(*args, **kwargs)

    def _finish(self, verdict, reason, confidence, **extra):
        if extra or verdict not in {"benign", "malicious", "unknown"}:
            raise ValueError("direct verdict must be benign, malicious or unknown")
        if not isinstance(reason, str) or not 1 <= len(reason) <= 2000:
            raise ValueError("reason must contain 1..2000 characters")
        if type(confidence) not in (int, float) or not 0 <= confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
        self.decision = {"verdict": verdict, "reason": reason, "confidence": confidence}
        self.status = "completed"
        self.event("direct_decision", **self.decision)
        return {"finished": True, "decision": self.decision}

    def report(self):
        return {**super().report(), "direct_decision": self.decision}
