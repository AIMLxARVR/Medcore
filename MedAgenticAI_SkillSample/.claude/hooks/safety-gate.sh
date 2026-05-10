#!/usr/bin/env bash
# PreToolUse safety gate. Blocks dangerous commands.
# Runs before every tool call. No exceptions.

TOOL=$(jq -r .tool_name)
INPUT=$(jq -r .tool_input.command // "")

# Block destructive operations on data
BLOCKED_PATTERNS=(
  "rm -rf data/"
  "rm -rf evaluation/"
  "DROP TABLE"
  "DELETE FROM"
  "truncate"
  "> /dev/null 2>&1 &"
)

for PATTERN in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$INPUT" | grep -qi "$PATTERN"; then
    echo "BLOCKED: Dangerous command pattern detected: $PATTERN"
    echo "Requires explicit human approval. Aborting."
    exit 1
  fi
done

# Log all bash tool calls for audit
if [ "$TOOL" = "bash" ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) TOOL_CALL bash: $INPUT" >> observability/tool_audit.log
fi

# Hooks are your guardrails.
