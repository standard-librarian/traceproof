export type TraceproofRun = {
  prompt: string;
  messages: Array<Record<string, unknown>>;
  model: Record<string, unknown>;
  tool_calls?: Array<Record<string, unknown>>;
  retrieval?: Array<Record<string, unknown>>;
  output: Record<string, unknown>;
  metadata?: Record<string, unknown>;
};

export function buildRun(run: TraceproofRun): TraceproofRun {
  return {
    ...run,
    tool_calls: run.tool_calls ?? [],
    retrieval: run.retrieval ?? [],
    metadata: run.metadata ?? {},
  };
}
