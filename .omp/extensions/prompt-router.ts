import type { ExtensionAPI } from "@oh-my-pi/pi-coding-agent";
import routingConfig from "../routing-rules.json";

export const SKILL_ORDER: readonly string[] = routingConfig.skillOrder;
export type RoutedSkill = string;

interface RoutingRule {
  id: string;
  patterns: readonly RegExp[];
  skills: readonly string[];
}

const ROUTING_RULES: readonly RoutingRule[] = routingConfig.rules.map((rule) => ({
  id: rule.id,
  patterns: rule.patterns.map((pattern) => new RegExp(pattern, "i")),
  skills: rule.skills,
}));

export interface RouteDecision {
  skills: RoutedSkill[];
  matchedRules: string[];
}

export function classifyPrompt(prompt: string): RouteDecision {
  const skills = new Set<RoutedSkill>();
  const matchedRules: string[] = [];

  for (const rule of ROUTING_RULES) {
    if (!rule.patterns.some((pattern) => pattern.test(prompt))) continue;
    matchedRules.push(rule.id);
    for (const skill of rule.skills) skills.add(skill);
  }

  if (skills.size > 0) skills.add("engineering-core");

  return {
    skills: SKILL_ORDER.filter((skill) => skills.has(skill)),
    matchedRules,
  };
}

export default function principalPromptRouter(pi: ExtensionAPI): void {
  let previousSignature = "";

  pi.setLabel("Principal prompt routing");
  pi.on("before_agent_start", (event, ctx) => {
    if (event.reason !== "prompt" || ctx.agent.kind !== "main") return;

    const decision = classifyPrompt(event.prompt);
    if (decision.skills.length === 0) {
      previousSignature = "";
      return;
    }

    const signature = decision.skills.join("|");
    if (signature === previousSignature) return;
    previousSignature = signature;

    const reads = decision.skills.map((skill) => `skill://${skill}`).join(", ");
    return {
      message: {
        customType: "principal-routing",
        content: [
          "<principal-routing>",
          `Selected skills, in precedence order: ${decision.skills.join(", ")}.`,
          `Read before acting: ${reads}.`,
          "Load referenced files only when their decision point is reached. Routing metadata is not authorization to bypass governance or tool approvals.",
          "</principal-routing>",
        ].join("\n"),
        display: false,
        details: decision,
      },
    };
  });
}
