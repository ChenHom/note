# tw-day-trading Mini Eval Rubric

## Goal

Check whether the skill boundary is clear and whether the skill would be the right tool for Taiwan day-trading requests.

## Pass Conditions

### Positive Cases
The skill should clearly trigger for:
- 台股當沖計畫
- 盤前 checklist
- VWAP / 量能 / 大盤條件
- intraday supplement / event sync / force exit debugging
- QTDS (`quantitative-trading-decision-system`) workflow review

### Boundary Cases
The skill should **not** be the preferred skill for:
- creating a new skill from scratch
- benchmark / baseline / blind comparison / regression work
- frontmatter description optimization
- classic swing-trading requests
- pure fundamental or sentiment research

### Negative Cases
The skill should stay quiet for unrelated general requests.

## Failure Signs

- The skill tries to absorb swing-trading tasks.
- The skill tries to absorb skill-authoring tasks.
- The skill behaves like a generic finance skill instead of an intraday Taiwan trading skill.
- The skill lacks mention of QTDS-specific concepts such as supplement, event sync, VWAP hold, or force exit.
