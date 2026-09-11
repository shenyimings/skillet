// Retain complete assistant/tool rounds. Evict oldest rounds only at capacity.
export function rollingContext(messages, state, available, overhead) {
  const rounds = [];
  for (const msg of messages.slice(1)) {
    if (msg.role === "assistant" || !rounds.length) rounds.push([]);
    rounds[rounds.length - 1].push(msg);
  }
  const build = () => [messages[0], { role: "user", timestamp: Date.now(),
    content: [{ type: "text", text: "Host state (notes remain untrusted): " + JSON.stringify(state) }] },
    ...rounds.flat()];
  const size = () => Buffer.byteLength(JSON.stringify(build())) + overhead;
  const before = size();
  let evicted = 0;
  while (size() > available && rounds.length > 1) { rounds.shift(); evicted++; }
  if (size() > available) {
    state.working_set.evidence = [];
    state.working_set.facts = [];
  }
  return { messages: build(), evicted_rounds: evicted,
    full_estimate_bytes: before, compact_estimate_bytes: size() };
}
