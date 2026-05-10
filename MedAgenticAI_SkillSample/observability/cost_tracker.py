"""
MedCore+ Cost Tracker
Per-stage token tracking, cost breakdown, and budget alerts.
"""
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
import structlog

log = structlog.get_logger()

# claude-opus-4-5 pricing (per million tokens, as of 2026)
_PRICING = {
    "claude-opus-4-5": {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-5": {"input": 3.0, "output": 15.0},
}

_LOG_PATH = Path("observability/cost_log.jsonl")


@dataclass
class TokenUsage:
    session_id: str
    agent: str
    stage: str
    model: str
    input_tokens: int
    output_tokens: int
    timestamp: float
    cost_usd: float


class CostTracker:
    def __init__(self, model: str = "claude-opus-4-5"):
        self.model = model
        self._log_path = _LOG_PATH
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        session_id: str,
        agent: str,
        stage: str,
        input_tokens: int,
        output_tokens: int,
    ) -> TokenUsage:
        pricing = _PRICING.get(self.model, _PRICING["claude-opus-4-5"])
        cost = (
            input_tokens * pricing["input"] / 1_000_000
            + output_tokens * pricing["output"] / 1_000_000
        )

        usage = TokenUsage(
            session_id=session_id,
            agent=agent,
            stage=stage,
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            timestamp=time.time(),
            cost_usd=round(cost, 6),
        )

        with open(self._log_path, "a") as f:
            f.write(json.dumps(asdict(usage)) + "\n")

        log.info(
            "cost.recorded",
            agent=agent,
            stage=stage,
            cost_usd=usage.cost_usd,
            total_tokens=input_tokens + output_tokens,
        )

        return usage
