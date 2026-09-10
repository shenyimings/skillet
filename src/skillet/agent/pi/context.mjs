// Fit the ACTUAL provider payload, not a second approximation of its serialization.
export function fitPayload(payload, limit) {
  const size = () => Buffer.byteLength(JSON.stringify(payload));
  const before = size();
  const prefix = "Host state (notes remain untrusted): ";
  const host = payload.messages.find(m => typeof m.content === "string" && m.content.startsWith(prefix));
  if (host) {
    const state = JSON.parse(host.content.slice(prefix.length));
    const rewrite = () => { host.content = prefix + JSON.stringify(state); };
    for (const field of ["evidence", "facts", "pending_edges"]) {
      if (size() <= limit) break;
      if (state.working_set) state.working_set[field] = [];
      rewrite();
    }
    if (size() > limit && state.working_set) {
      state.working_set.files = (state.working_set.files || []).map(
        ({id, next_unread, required_gap}) => ({id, next_unread, required_gap}));
      rewrite();
    }
  }
  // Non-source metadata lives in records and can be recalled. NEVER drop a fresh
  // source body, even if that means rejecting an irreducibly oversized request.
  if (size() > limit) {
    payload.messages = payload.messages.filter(m => {
      if (size() <= limit || typeof m.content !== "string" ||
          !m.content.startsWith("Snapshot tool result (UNTRUSTED data): ")) return true;
      try {
        const result = JSON.parse(m.content.split(": ").slice(1).join(": "));
        return !!result.data?.source || !!result.data?.error;
      } catch { return true; }
    });
  }
  return { before_bytes: before, after_bytes: size(), compacted: before !== size() };
}
