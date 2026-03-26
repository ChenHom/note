# tw-swing-trading Mini Eval Rubric v2

## Goal

Check whether the skill boundary is clear and whether the skill is the right tool for Taiwan swing-trading requests.

## Pass Conditions

### Positive Cases
The skill should clearly trigger for:
- 台股波段計畫
- breakout / pullback / trend review
- stop / trim / hold management
- Minervini-style momentum checks
- watchlist quality vs entry quality judgments
- false breakout vs healthy pullback distinctions
- turning stock ideas into rule-based swing plans

### Boundary Cases
The skill should not be the preferred skill for:
- pure當沖 execution and supplement logic
- skill creation / benchmark / description rewrite work
- intraday signal file debugging
- pure financial statement or sentiment summarization without a trade plan

### Negative Cases
The skill should stay quiet for unrelated requests.

## Failure Signs

- The skill tries to absorb intraday supplement / force-exit / event-sync tasks.
- The skill tries to absorb skill-authoring tasks.
- The skill acts like a generic finance summary skill instead of a Taiwan swing-trading skill.
- The skill cannot distinguish watchlist quality from entry quality.
- The skill has no language for fake breakouts, loose structure, or constructive pullbacks.
