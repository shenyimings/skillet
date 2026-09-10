import { Type } from "typebox";
const string = (maxLength = 120) => Type.String({ minLength: 1, maxLength });
const optional = Type.Optional;
const fileId = () => Type.String({ pattern: "^f[0-9]+$", description: "Snapshot ID such as f0; never a path." });
const integer = (maximum) => Type.Integer({ minimum: 0, ...(maximum == null ? {} : { maximum }) });
const object = fields => Type.Object(fields, { additionalProperties: false });
const page = { offset: optional(integer()) };
const anchor = { source: string(), offset: optional(integer()) };
const labels = ["reads_sensitive", "reads_personal", "sends_outward", "fetches_remote",
  "executes_code", "writes_agent_state", "claims_authority", "asks_to_conceal",
  "claims_persistent", "misrepresents", "instructs_agent"];
// Each action has its own exact argument schema, including the closed label vocabulary.
export const actions = {
  files: object(page), facts: object({ ...page, predicate: optional(string()) }),
  gaps: object(page),
  read: object({ file: fileId(), start: optional(integer()),
    size: optional(Type.Integer({ minimum: 1, maximum: 2400 })), gap: optional(string()) }),
  search: object({ file: fileId(), text: string(), start: optional(integer()), gap: optional(string()) }),
  remember: object({ text: Type.String({ maxLength: 1000 }) }),
  recall: object({ record: string(), start: optional(integer()),
    size: optional(Type.Integer({ minimum: 1, maximum: 1000 })) }),
  review: object({ file: fileId(), reason: string(300) }),
  observe: object({ ...anchor, label: object({
    observation: Type.Union(labels.map(value => Type.Literal(value))),
    quote: string(600), confidence: Type.Number({ minimum: 0, maximum: 1 }),
    detail: optional(Type.String({ maxLength: 120 })),
  }) }),
  edge: object({ ...anchor, source_locus: string(400), target_locus: string(400),
    confirmed: Type.Boolean(), quote: string(600), reason: string(300) }),
  finish: object({}),
};
// Retain the audit's action/args RPC shape; exposed functions have typed parameters.

actions.finish = object({
  observations: optional(Type.Array(actions.observe, { maxItems: 6 })),
  edges: optional(Type.Array(actions.edge, { maxItems: 6 })),
  reason: optional(string(1000)),
});
