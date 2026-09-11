"""Admit each submitted item independently; malformed siblings never roll back facts."""


def finish_partial(host, observations=None, edges=None, reason="", **extra):
    accepted, rejected = [], []
    if extra:
        rejected.append(
            {"field": "top_level", "error": "unexpected fields: " + ", ".join(extra)[:160]}
        )
    if not isinstance(reason, str) or len(reason) > 1000:
        rejected.append({"field": "reason", "error": "expected at most 1000 characters"})
    for field, items, admit in (
        ("observations", observations, host._observe),
        ("edges", edges, host._edge),
    ):
        if items is None:
            continue
        if not isinstance(items, list):
            rejected.append({"field": field, "error": "expected an array"})
            continue
        if len(items) > 6:
            rejected.append({"field": field, "error": "items beyond first 6 were not admitted"})
        for index, item in enumerate(items[:6]):
            try:
                if not isinstance(item, dict):
                    raise ValueError("expected an object")
                result = admit(**item)
                accepted.append({"field": field, "index": index, **result})
            except (ValueError, TypeError, KeyError) as exc:
                rejected.append({"field": field, "index": index, "error": str(exc)[:200]})
    host.submission_errors = rejected
    host.event("submission", accepted=accepted, rejected=rejected)
    # A partial submission is useful evidence, but cannot certify a clean review.
    # Stop without more paid calls; the audit can be resumed for unresolved items.
    if host.status == "running":
        host.status = "incomplete_submission" if rejected else "completed"
    return {
        "finished": not rejected,
        "accepted": accepted,
        "rejected": rejected,
        "partial_results_retained": True,
        "coverage_complete": host.report()["coverage_complete"],
    }
