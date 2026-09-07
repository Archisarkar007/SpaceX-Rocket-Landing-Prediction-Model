# Data dictionary

## `launches_dashboard.csv`

| Column | Description |
|---|---|
| Flight Number | Sequential flight identifier used in the dashboard dataset |
| Date | Launch date matched by flight number |
| Launch Site | Launch site associated with the flight |
| Landing Success | Binary target: 1 = successful landing, 0 = failure |
| Outcome Label | Human-readable success/failure label |
| Payload Mass (kg) | Payload mass in kilograms |
| Booster Version | Booster identifier/version |
| Booster Version Category | Grouped booster generation |
| Orbit | Target orbit |
| Customer | Customer listed in the scraped launch history |
| Launch outcome | Mission-level launch outcome |
| Booster landing | Landing outcome from the scraped history |

The repository also preserves the original intermediate datasets used by the supplied notebooks.
