import principalPromptRouter, { classifyPrompt } from "../.omp/extensions/prompt-router.ts";
import scenarios from "./scenarios.json";

type Handler = (event: { reason: string; prompt: string }, context: { agent: { kind: string } }) => unknown;

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

function assertJsonEqual(actual: unknown, expected: unknown, label: string): void {
  const actualJson = JSON.stringify(actual);
  const expectedJson = JSON.stringify(expected);
  assert(actualJson === expectedJson, `${label}: expected ${expectedJson}, got ${actualJson}`);
}

function createHandler(): Handler {
  let handler: Handler | undefined;
  const api = {
    setLabel: (_label: string) => undefined,
    on: (event: string, candidate: Handler) => {
      if (event === "before_agent_start") handler = candidate;
    },
  };
  principalPromptRouter(api as never);
  assert(handler, "router did not register before_agent_start");
  return handler;
}

const main = { agent: { kind: "main" } };
const sub = { agent: { kind: "sub" } };
const engineering = "Rename a TypeScript variable and run the focused test.";
const architecture = "Design a distributed system with explicit failure modes.";
const unrelated = "Write a short poem about rain.";

for (const scenario of scenarios) {
  assertJsonEqual(classifyPrompt(scenario.prompt).skills, scenario.expectedSkills, `scenario ${scenario.id}`);
}

const firstHandler = createHandler();
const first = firstHandler({ reason: "prompt", prompt: engineering }, main) as Record<string, any>;
assert(first?.message?.customType === "principal-routing", "missing principal-routing message");
assert(first.message.display === false, "routing message must stay hidden");
assertJsonEqual(first.message.details.skills, ["engineering-core"], "routing message details");
assert(first.message.content.includes("skill://engineering-core"), "routing message omits selected skill URI");
assert(firstHandler({ reason: "prompt", prompt: engineering }, main) === undefined, "A→A must suppress the second route");

const gapHandler = createHandler();
assert(gapHandler({ reason: "prompt", prompt: engineering }, main), "A→none→A first route missing");
assert(gapHandler({ reason: "prompt", prompt: unrelated }, main) === undefined, "no-route prompt injected metadata");
assert(gapHandler({ reason: "prompt", prompt: engineering }, main), "A→none→A must reinject A");

const changedHandler = createHandler();
assert(changedHandler({ reason: "prompt", prompt: engineering }, main), "A→B→A first route missing");
assert(changedHandler({ reason: "prompt", prompt: architecture }, main), "A→B→A B route missing");
assert(changedHandler({ reason: "prompt", prompt: engineering }, main), "A→B→A final route missing");

const bypassHandler = createHandler();
assert(bypassHandler({ reason: "prompt", prompt: engineering }, main), "bypass setup route missing");
assert(bypassHandler({ reason: "prompt", prompt: architecture }, sub) === undefined, "subagent prompt must bypass routing");
assert(bypassHandler({ reason: "resume", prompt: architecture }, main) === undefined, "non-prompt event must bypass routing");
assert(bypassHandler({ reason: "prompt", prompt: engineering }, main) === undefined, "bypassed events must not mutate duplicate state");

process.stdout.write(`Runtime router checks passed: ${scenarios.length} scenarios and handler transitions.\n`);

export default function runtimeRouterCheck(): void {
  // The checks already executed during module load under OMP's embedded Bun runtime.
}
