#!/usr/bin/env python3
"""Validate the repository-local Principal Engineering OMP template."""

from __future__ import annotations

import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Optional, Union

ROOT = Path(__file__).resolve().parent.parent
ROUTING_CONFIG_PATH = ROOT / ".omp" / "routing-rules.json"
FrontmatterValue = Union[str, list[str], bool]


def load_routing_config() -> dict[str, object]:
    return json.loads(ROUTING_CONFIG_PATH.read_text(encoding="utf-8"))


def classify_prompt(prompt: str) -> dict[str, list[str]]:
    """Dependency-free oracle for the runtime router's shared rule table."""
    config = load_routing_config()
    skill_order = config.get("skillOrder")
    rules = config.get("rules")
    if not isinstance(skill_order, list) or not all(isinstance(item, str) for item in skill_order):
        raise ValueError("routing-rules.json skillOrder must be a string array")
    if not isinstance(rules, list):
        raise ValueError("routing-rules.json rules must be an array")

    selected: set[str] = set()
    matched_rules: list[str] = []
    for raw_rule in rules:
        if not isinstance(raw_rule, dict):
            raise ValueError("routing rule must be an object")
        rule_id = raw_rule.get("id")
        patterns = raw_rule.get("patterns")
        skills = raw_rule.get("skills")
        if not isinstance(rule_id, str):
            raise ValueError("routing rule id must be a string")
        if not isinstance(patterns, list) or not all(isinstance(item, str) for item in patterns):
            raise ValueError(f"routing rule {rule_id} patterns must be a string array")
        if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
            raise ValueError(f"routing rule {rule_id} skills must be a string array")
        if not any(re.search(pattern, prompt, re.IGNORECASE) for pattern in patterns):
            continue
        matched_rules.append(rule_id)
        selected.update(skills)

    if selected:
        selected.add("engineering-core")
    return {
        "skills": [skill for skill in skill_order if skill in selected],
        "matched_rules": matched_rules,
    }

REQUIRED_FILES = (
    "AGENTS.md",
    "CONTEXT.md",
    "README.md",
    "implementation-notes.md",
    "docs/research.md",
    "docs/validation-report.md",
    "docs/architecture/overview.md",
    "docs/adr/0001-native-routing.md",
    "docs/adr/0002-agent-roles.md",
    ".omp/extensions/prompt-router.ts",
    ".omp/config.yml",
    ".omp/routing-rules.json",
    "tests/__init__.py",
    "tests/test_prompt_router.py",
    "tests/scenarios.json",
    "tests/runtime-router-check.ts",
    "tests/test_apply_template.py",
    "scripts/validate_template.py",
    "scripts/apply_template.py",
    "scripts/test_runtime_router.py",
)
EXPECTED_MODEL_ROLES = {
    "default": "openai-codex/gpt-6-luna:medium",
    "smol": "openai-codex/gpt-6-luna:low",
    "slow": "openai-codex/gpt-6.1-terra:high",
    "plan": "openai-codex/gpt-6.1-terra:high",
    "task": "openai-codex/gpt-6-luna:medium",
    "advisor": "openai-codex/gpt-6.1-terra:high",
    "judge": "openai-codex/gpt-6-luna:medium",
    "memory": "openai-codex/gpt-6-luna:low",
    "commit": "openai-codex/gpt-6-luna:medium",
    "tiny": "openai-codex/gpt-6-luna:low",
}
ALLOWED_SKILL_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
ALLOWED_AGENT_FIELDS = {
    "name",
    "description",
    "tools",
    "spawns",
    "model",
    "thinkingLevel",
    "thinking-level",
    "thinking",
    "output",
    "blocking",
    "structured",
    "autoloadSkills",
    "autoload-skills",
    "readSummarize",
    "read-summarize",
    "prewalk",
    "advisor",
}
BUNDLED_AGENT_NAMES = {"reviewer", "scout", "seance", "security-reviewer", "sonic", "task"}
READ_ONLY_AGENT_NAMES = {"architect", "smart-contract-auditor", "sre"}
READ_ONLY_AGENT_TOOLS = {"read", "grep", "glob"}
KNOWN_AGENT_TOOLS = {
    "read",
    "find",
    "grep",
    "glob",
    "bash",
    "lsp",
    "web_search",
    "ast_grep",
    "edit",
    "write",
    "todo",
    "task",
    "wait",
    "eval",
    "ask",
}
REQUIRED_SCENARIOS = {
    "small-mechanical-change",
    "incorrect-user-diagnosis",
    "complex-architecture",
    "blockchain-reorg-bug",
    "smart-contract-vulnerability",
    "backend-concurrency-bug",
    "api-performance-regression",
    "production-infrastructure-incident",
    "code-review-real-findings",
    "ambiguous-requirements",
    "parallel-agent-conflict",
    "missing-tool-or-model",
    "malicious-repository-instructions",
    "failed-verification-gate",
    "skill-collision",
}

errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(content: str, path: str) -> Optional[dict[str, FrontmatterValue]]:
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)", content)
    if not match:
        fail(f"{path}: missing YAML frontmatter")
        return None

    result: dict[str, FrontmatterValue] = {}
    list_key: Optional[str] = None
    for index, raw_line in enumerate(match.group(1).splitlines(), start=2):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        list_match = re.match(r"^\s+-\s+(.+)$", raw_line)
        if list_match and list_key:
            current = result.get(list_key)
            if not isinstance(current, list):
                fail(f"{path}:{index}: list item does not follow a list key")
            else:
                current.append(unquote(list_match.group(1)))
            continue
        key_match = re.match(r"^([A-Za-z][A-Za-z0-9-]*):(?:\s*(.*))?$", raw_line)
        if not key_match:
            fail(f"{path}:{index}: unsupported frontmatter syntax")
            list_key = None
            continue
        key, raw_value = key_match.group(1), (key_match.group(2) or "").strip()
        if raw_value in {"", "[]"}:
            result[key] = []
            list_key = key
        elif raw_value in {"true", "false"}:
            result[key] = raw_value == "true"
            list_key = None
        else:
            result[key] = unquote(raw_value)
            list_key = None
    return result


def required_string(frontmatter: dict[str, FrontmatterValue], key: str, path: str) -> Optional[str]:
    value = frontmatter.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{path}: {key} must be a non-empty string")
        return None
    return value


def list_field(frontmatter: dict[str, FrontmatterValue], *keys: str) -> list[str]:
    for key in keys:
        value = frontmatter.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
    return []


def validate_project_config() -> None:
    path = ROOT / ".omp" / "config.yml"
    roles: dict[str, str] = {}
    saw_model_roles = False
    for index, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith((" ", "\t")):
            if raw_line == "modelRoles:" and not saw_model_roles:
                saw_model_roles = True
                continue
            fail(f".omp/config.yml:{index}: unsupported or duplicate top-level setting")
            continue
        if "\t" in raw_line:
            fail(f".omp/config.yml:{index}: tabs are not supported")
            continue
        match = re.fullmatch(r"  ([a-z]+):\s+(.+)", raw_line)
        if not saw_model_roles or not match:
            fail(f".omp/config.yml:{index}: expected a two-space-indented model role")
            continue
        role, raw_selector = match.group(1), match.group(2)
        selector = unquote(raw_selector)
        if role in roles:
            fail(f".omp/config.yml:{index}: duplicate model role {role}")
            continue
        roles[role] = selector

    if not saw_model_roles:
        fail(".omp/config.yml: missing modelRoles mapping")
    for role, expected in EXPECTED_MODEL_ROLES.items():
        actual = roles.get(role)
        if actual != expected:
            fail(f".omp/config.yml: role {role} must be {expected}, got {actual!r}")
    for role in sorted(set(roles) - set(EXPECTED_MODEL_ROLES)):
        fail(f".omp/config.yml: unsupported model role {role}")


def preflight_repository() -> None:
    """Reject unsafe template-owned paths before any template content is opened."""
    candidates: set[Path] = {ROOT / path for path in REQUIRED_FILES}
    candidates.update(ROOT / name for name in ("AGENTS.md", "CONTEXT.md", "README.md", "implementation-notes.md"))
    for relative_root in (".omp", "docs", "scripts", "tests"):
        base = ROOT / relative_root
        try:
            base.lstat()
        except FileNotFoundError:
            continue
        candidates.add(base)
        for directory, directories, files in os.walk(base, followlinks=False):
            directory_path = Path(directory)
            candidates.update(directory_path / name for name in directories)
            candidates.update(directory_path / name for name in files)

    for path in sorted(candidates):
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            continue
        relative_path = path.relative_to(ROOT)
        if stat.S_ISLNK(metadata.st_mode):
            fail(f"{relative_path}: template-owned paths must not be symlinks")
            continue
        if stat.S_ISREG(metadata.st_mode):
            if metadata.st_size > 1024 * 1024:
                fail(f"{relative_path}: template-owned file exceeds 1 MiB")
            if metadata.st_mode & stat.S_IWOTH:
                fail(f"{relative_path}: world-writable file")


def contained_path(path: Path, label: str) -> Optional[Path]:
    try:
        resolved = path.resolve()
        if os.path.commonpath((str(ROOT.resolve()), str(resolved))) != str(ROOT.resolve()):
            fail(f"{label}: reference escapes repository")
            return None
        return resolved
    except (OSError, ValueError) as error:
        fail(f"{label}: cannot resolve reference: {error}")
        return None


def validate_required_files() -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).exists():
            fail(f"Missing required file: {relative_path}")


def validate_skills() -> set[str]:
    skills_root = ROOT / ".omp" / "skills"
    names: set[str] = set()
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        path = skill_dir / "SKILL.md"
        relative_path = str(path.relative_to(ROOT))
        if not path.exists():
            fail(f"{skill_dir.name}: skill directory has no SKILL.md")
            continue
        frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"), relative_path)
        if not frontmatter:
            continue
        for key in frontmatter:
            if key not in ALLOWED_SKILL_FIELDS:
                fail(f"{relative_path}: unsupported Agent Skills field {key}")
        name = required_string(frontmatter, "name", relative_path)
        description = required_string(frontmatter, "description", relative_path)
        if not name or not description:
            continue
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            fail(f"{relative_path}: invalid skill name {name}")
        if name != skill_dir.name:
            fail(f"{relative_path}: name must match directory {skill_dir.name}")
        if len(description) > 1024:
            fail(f"{relative_path}: description exceeds 1024 characters")
        compatibility = frontmatter.get("compatibility")
        if isinstance(compatibility, str) and len(compatibility) > 500:
            fail(f"{relative_path}: compatibility exceeds 500 characters")
        if name in names:
            fail(f"{relative_path}: duplicate skill name {name}")
        names.add(name)

    config = load_routing_config()
    skill_order = config.get("skillOrder")
    if not isinstance(skill_order, list) or not all(isinstance(item, str) for item in skill_order):
        fail("routing-rules.json skillOrder must be a string array")
        return names
    if len(names) != len(skill_order):
        fail(f"Expected {len(skill_order)} project skills, found {len(names)}")
    for routed in skill_order:
        if routed not in names:
            fail(f"Router references missing skill {routed}")
    return names


def validate_agents(skill_names: set[str]) -> None:
    agents_root = ROOT / ".omp" / "agents"
    names: set[str] = set()
    for path in sorted(agents_root.glob("*.md")):
        relative_path = str(path.relative_to(ROOT))
        frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"), relative_path)
        if not frontmatter:
            continue
        for key in frontmatter:
            if key not in ALLOWED_AGENT_FIELDS:
                fail(f"{relative_path}: unsupported OMP agent field {key}")
        name = required_string(frontmatter, "name", relative_path)
        required_string(frontmatter, "description", relative_path)
        if not name:
            continue
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            fail(f"{relative_path}: invalid agent name {name}")
        if name.lower() in {"main", "sub"}:
            fail(f"{relative_path}: reserved agent name {name}")
        if name in BUNDLED_AGENT_NAMES:
            fail(f"{relative_path}: unnecessarily shadows bundled agent {name}")
        if name in names:
            fail(f"{relative_path}: duplicate project agent {name}")
        names.add(name)
        tools = list_field(frontmatter, "tools")
        for tool in tools:
            if tool not in KNOWN_AGENT_TOOLS:
                fail(f"{relative_path}: unknown tool {tool}")
        if name in READ_ONLY_AGENT_NAMES:
            excess = sorted(set(tools) - READ_ONLY_AGENT_TOOLS)
            if excess:
                fail(f"{relative_path}: read-only agent has write/execute/network-capable tools {excess}")
        for skill in list_field(frontmatter, "autoloadSkills", "autoload-skills"):
            if skill not in skill_names:
                fail(f"{relative_path}: autoloads unknown skill {skill}")

    expected = {"architect", "smart-contract-auditor", "sre", "test-engineer"}
    for missing in sorted(expected - names):
        fail(f"Missing required project agent {missing}")


def validate_references(skill_names: set[str]) -> None:
    markdown_paths = [
        ROOT / "AGENTS.md",
        ROOT / "CONTEXT.md",
        ROOT / "README.md",
        ROOT / "implementation-notes.md",
        *(ROOT / ".omp").rglob("*.md"),
        *(ROOT / "docs").rglob("*.md"),
    ]
    for path in markdown_paths:
        content = path.read_text(encoding="utf-8")
        relative_path = str(path.relative_to(ROOT))
        for match in re.finditer(r"skill://([a-z0-9-]+)(/[A-Za-z0-9._/-]+)?", content):
            skill, suffix = match.group(1), match.group(2)
            if skill not in skill_names:
                fail(f"{relative_path}: references unknown skill {skill}")
                continue
            if suffix:
                suffix_path = Path(suffix[1:])
                label = f"{relative_path}: {match.group(0)}"
                if suffix_path.is_absolute() or ".." in suffix_path.parts:
                    fail(f"{label}: invalid skill resource path")
                    continue
                resource = contained_path(ROOT / ".omp" / "skills" / skill / suffix_path, label)
                if resource and not resource.exists():
                    fail(f"{relative_path}: missing skill resource {match.group(0)}")
        for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = match.group(1).split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "skill://")):
                continue
            label = f"{relative_path}: {target}"
            resolved = contained_path(path.parent / target, label)
            if resolved and not resolved.exists():
                fail(f"{relative_path}: broken relative link {target}")


def validate_router() -> None:
    config = load_routing_config()
    skill_order = config.get("skillOrder")
    rules = config.get("rules")
    if not isinstance(skill_order, list) or len(skill_order) != len(set(skill_order)):
        fail("routing-rules.json skillOrder must contain unique entries")
    if not isinstance(rules, list):
        fail("routing-rules.json rules must be an array")
        return
    rule_ids: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            fail("routing rule must be an object")
            continue
        rule_id, patterns, skills = rule.get("id"), rule.get("patterns"), rule.get("skills")
        if not isinstance(rule_id, str) or not rule_id:
            fail("routing rule id must be a non-empty string")
            continue
        if rule_id in rule_ids:
            fail(f"duplicate routing rule id {rule_id}")
        rule_ids.add(rule_id)
        if not isinstance(patterns, list) or not patterns or not all(isinstance(item, str) for item in patterns):
            fail(f"routing rule {rule_id}: patterns must be a non-empty string array")
        else:
            for pattern in patterns:
                try:
                    re.compile(pattern, re.IGNORECASE)
                except re.error as error:
                    fail(f"routing rule {rule_id}: invalid pattern {pattern}: {error}")
        if not isinstance(skills, list) or not skills or not all(isinstance(item, str) for item in skills):
            fail(f"routing rule {rule_id}: skills must be a non-empty string array")
        elif isinstance(skill_order, list):
            for skill in skills:
                if skill not in skill_order:
                    fail(f"routing rule {rule_id}: unknown skill {skill}")

    extension = (ROOT / ".omp" / "extensions" / "prompt-router.ts").read_text(encoding="utf-8")
    if 'from "../routing-rules.json"' not in extension:
        fail("prompt-router.ts must import the single shared routing-rules.json")


def validate_scenarios(skill_names: set[str]) -> None:
    scenarios = json.loads((ROOT / "tests" / "scenarios.json").read_text(encoding="utf-8"))
    if not isinstance(scenarios, list):
        fail("tests/scenarios.json must be an array")
        return
    if len(scenarios) < 15:
        fail(f"Expected at least 15 scenarios, found {len(scenarios)}")
    ids: set[str] = set()
    required_fields = {
        "id": str,
        "prompt": str,
        "expectedSkills": list,
        "subagents": str,
        "requiredVerification": list,
        "failureAndEscalation": str,
        "successCriteria": str,
    }
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            fail("scenario must be an object")
            continue
        scenario_id = scenario.get("id", "<missing>")
        for field, field_type in required_fields.items():
            if not isinstance(scenario.get(field), field_type):
                fail(f"{scenario_id}: {field} has the wrong type")
        if not isinstance(scenario_id, str):
            continue
        if scenario_id in ids:
            fail(f"duplicate scenario id {scenario_id}")
        ids.add(scenario_id)
        prompt = scenario.get("prompt")
        expected = scenario.get("expectedSkills")
        verification = scenario.get("requiredVerification")
        if not isinstance(prompt, str) or not isinstance(expected, list) or not all(isinstance(item, str) for item in expected):
            continue
        if not isinstance(verification, list) or not verification:
            fail(f"{scenario_id}: no required verification")
        for skill in expected:
            if skill not in skill_names:
                fail(f"{scenario_id}: expects unknown skill {skill}")
        actual = classify_prompt(prompt)["skills"]
        if actual != expected:
            fail(f"{scenario_id}: expected {expected}, got {actual}")
    for missing in sorted(REQUIRED_SCENARIOS - ids):
        fail(f"Missing required acceptance scenario {missing}")


def validate_safety() -> None:
    for path in (ROOT / ".omp").rglob("*"):
        if path.suffix not in {".md", ".ts", ".js", ".json", ".yml"} or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if re.search(r"/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/", content):
            fail(f"{path.relative_to(ROOT)}: hardcoded user home dependency")

    if (ROOT / ".omp" / "mcp.json").exists():
        fail(".omp/mcp.json requires an explicit capability and credential review before inclusion")
    command_names = [path.stem for path in (ROOT / ".omp" / "commands").glob("*.md")] if (ROOT / ".omp" / "commands").exists() else []
    if len(command_names) != len(set(command_names)):
        fail("duplicate command names")


def print_errors() -> None:
    print(f"Template validation failed with {len(errors)} issue(s):", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)


def main() -> int:
    preflight_repository()
    if errors:
        print_errors()
        return 1
    validate_required_files()
    validate_project_config()
    skill_names = validate_skills()
    validate_agents(skill_names)
    validate_references(skill_names)
    validate_router()
    validate_scenarios(skill_names)
    validate_safety()
    if errors:
        print_errors()
        return 1
    print("Template validation passed: 7 skills, 4 project agents, 7 routed skill slots, 20 scenarios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
