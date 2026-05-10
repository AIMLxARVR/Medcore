#!/usr/bin/env bash
# MedCore+ Claude Code statusline
# Shows: env | model | last eval score | cost today

ENV=${MEDCORE_ENV:-dev}
MODEL="opus-4-5"

# Last eval score (from most recent eval result)
LAST_EVAL=$(ls -t observability/eval_results/*.json 2>/dev/null | head -1)
if [ -n "$LAST_EVAL" ]; then
  SCORE=$(python -c "import json,sys; d=json.load(open(sys.argv[1])); print(f\"{d.get('top3_acc',0):.0%}\")" "$LAST_EVAL" 2>/dev/null || echo "—")
else
  SCORE="—"
fi

# Cost today
COST=$(python -c "
import json,sys
from datetime import date
total=0
try:
  for line in open('observability/cost_log.jsonl'):
    r=json.loads(line)
    from datetime import datetime
    if datetime.fromtimestamp(r['timestamp']).date()==date.today():
      total+=r['cost_usd']
except:pass
print(f'\${total:.3f}')
" 2>/dev/null || echo "\$—")

echo "🏥 medcore | $ENV | $MODEL | eval: $SCORE | today: $COST"
