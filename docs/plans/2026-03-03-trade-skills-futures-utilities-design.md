# Trade Skills Futures Utilities - Design Document

**Date:** 2026-03-03
**Author:** Claude Code
**Status:** Approved

## Overview

Add two futures-related utility functions to the trade-skills skill:

1. **Trading Hours Check** - Determine if a futures contract is currently in trading hours
2. **Dominant Contract Query** - Get the dominant (main) contract for a futures variety

Both features will be implemented via scripts in the trade-skills directory.

---

## Requirements

### Requirement 1: Trading Hours Check

**Input:** Futures contract symbol (e.g., `SHFE.rb2601`)
**Output:** JSON indicating whether the contract is currently tradable

```json
{
  "trading": true,
  "session": "night",
  "symbol": "SHFE.rb2601"
}
```

**Key Considerations:**
- Each futures variety has different trading hours
- Must handle day sessions, night sessions, and cross-midnight ranges (e.g., 21:00-01:00)
- Use China Standard Time (Asia/Shanghai timezone)

---

### Requirement 2: Dominant Contract Query

**Input:** Variety code (e.g., `rb`, `cu`, `IF`)
**Output:** JSON with the dominant contract for that variety

```json
{
  "symbol": "rb",
  "dominant": "rb2505",
  "exchange": "SHFE"
}
```

**Key Considerations:**
- Dominant contract determined by highest open interest
- Data must be refreshable via manual update command
- Balance between data freshness and query performance

---

## Architecture

### Directory Structure

```
trade-skills/
├── scripts/
│   ├── trade_utils.py              # Main CLI script (~300 lines)
│   ├── generate_trading_hours.py   # One-time data conversion (~80 lines)
│   ├── data/
│   │   ├── trading_hours.json      # Trading hours config (~500 lines)
│   │   └── dominant_contracts.json # Dominant contracts cache (~50 lines)
│   └── tests/                      # Optional test files
│       ├── test_trading_hours.py
│       ├── test_dominant_contract.py
│       └── test_integration.py
├── SKILL.md                        # Updated with scripts documentation
└── TEST.md
```

---

### CLI Commands

**Command 1: is-trading**
```bash
python3 scripts/trade_utils.py is-trading <EXCHANGE>.<SYMBOL>
```
Example: `python3 scripts/trade_utils.py is-trading SHFE.rb2601`

**Command 2: dominant-contract**
```bash
python3 scripts/trade_utils.py dominant-contract <VARIETY>
```
Example: `python3 scripts/trade_utils.py dominant-contract rb`

**Command 3: update-dominant**
```bash
python3 scripts/trade_utils.py update-dominant [--varieties rb,cu,al]
```
Updates dominant contracts database via tianqin-data API calls

---

## Data Design

### trading_hours.json Structure

```json
{
  "SHFE": {
    "rb": {
      "name": "螺纹钢",
      "call_auction": ["20:55-21:00", "08:55-09:00"],
      "day": ["09:00-10:15", "10:30-11:30", "13:30-15:00"],
      "night": ["21:00-23:00"]
    },
    "cu": {
      "name": "铜",
      "call_auction": ["20:55-21:00", "08:55-09:00"],
      "day": ["09:00-10:15", "10:30-11:30", "13:30-15:00"],
      "night": ["21:00-01:00"]
    }
  },
  "CFFEX": {
    "IF": {
      "name": "沪深300指数",
      "call_auction": ["09:25-09:30"],
      "day": ["09:30-11:30", "13:00-15:00"],
      "night": null
    }
  }
}
```

**Data Source:** Generated from `akshare-data/references/futures.md` trading hours table
**Update Frequency:** Static (update only when exchange changes trading hours)

---

### dominant_contracts.json Structure

```json
{
  "rb": {
    "dominant": "rb2505",
    "exchange": "SHFE",
    "updated_at": "2026-03-03T10:30:00"
  },
  "cu": {
    "dominant": "cu2504",
    "exchange": "SHFE",
    "updated_at": "2026-03-03T10:30:00"
  }
}
```

**Data Source:** Updated via `update-dominant` command (queries tianqin-data API)
**Update Frequency:** Manual (recommended weekly, or when contract rolls occur)

---

## Implementation Details

### 1. Trading Hours Check Logic

**Algorithm:**

1. Parse input symbol: `SHFE.rb2601` → exchange=`SHFE`, variety=`rb`
2. Load trading hours config from `trading_hours.json`
3. Get current time in China timezone (Asia/Shanghai)
4. Check if current time falls within any day/night session time ranges
5. Handle cross-midnight ranges (e.g., 21:00-01:00)

**Cross-Midnight Handling:**
```python
def is_cross_midnight(start: time, end: time) -> bool:
    """Check if time range crosses midnight"""
    return start > end

def is_in_time_range(current: time, time_range: str) -> bool:
    start, end = parse_time_range(time_range)

    if is_cross_midnight(start, end):
        # Example: 21:00-01:00
        return current >= start or current <= end
    else:
        # Example: 09:00-10:15
        return start <= current <= end
```

---

### 2. Dominant Contract Query Logic

**Algorithm:**

1. Read cached data from `dominant_contracts.json`
2. Lookup variety in cache
3. If found, return dominant contract with metadata
4. If not found, prompt user to run `update-dominant` first

**Simple and Fast:** Pure local file lookup, no API calls.

---

### 3. Dominant Contract Update Logic

**Algorithm:**

1. Determine update scope (all varieties or specified via `--varieties`)
2. For each variety:
   - Generate candidate contract codes (next 6 months)
   - Call tianqin-data API to get open interest for each contract
   - Find contract with highest open interest
3. Update `dominant_contracts.json` with results
4. Return summary: `{"updated": N, "failed": M, "timestamp": "..."}`

**Contract Code Generation:**
```python
def generate_contract_codes(variety: str, exchange: str) -> List[str]:
    """
    Generate contracts for next 6 months
    Example for 'rb' in March 2026:
      [rb2603, rb2604, rb2605, rb2610, rb2611, rb2612]
    """
    contracts = []
    current_date = datetime.now()

    for i in range(6):
        future_date = current_date + timedelta(days=30 * i)
        year = future_date.year % 100  # Last 2 digits
        month = future_date.month

        if exchange == "CZCE":
            contract = f"{variety.upper()}{month:02d}"
        else:
            contract = f"{variety.lower()}{year:02d}{month:02d}"

        contracts.append(contract)

    return contracts
```

**API Integration:**
```python
def get_contract_open_interest(exchange: str, contract: str) -> Optional[int]:
    """Query open interest via tianqin-data"""
    symbol = f"{exchange}.{contract}"
    tq_cli_path = "../../tianqin-data/scripts/tq_cli.py"

    result = subprocess.run(
        ["python3", tq_cli_path, "quote", symbol],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data.get("open_interest") or data.get("持仓量")

    return None
```

---

### 4. Data Initialization

**Step 1: Generate trading_hours.json**

Run `generate_trading_hours.py` to parse `akshare-data/references/futures.md`:

```python
def parse_trading_hours_table(md_file: Path) -> dict:
    """
    Parse trading hours table from futures.md
    Extract: exchange, variety, call_auction, day_hours, night_hours
    Convert to nested JSON structure
    """
    # Regex to find table
    # Parse each row
    # Build nested dict: {exchange: {variety: {sessions}}}
    return config
```

**Step 2: Initialize dominant_contracts.json**

Create empty file `{}`, then run:
```bash
python3 trade_utils.py update-dominant
```

---

## Dependencies

### Python Libraries

- `argparse` - CLI argument parsing (stdlib)
- `json` - JSON handling (stdlib)
- `datetime` - Time operations (stdlib)
- `subprocess` - Call tianqin-data CLI (stdlib)
- `pathlib` - File path handling (stdlib)

**No external dependencies required** (all standard library)

**Optional for production:**
- `pytz` - Explicit timezone handling (if system timezone not reliable)

---

### Skill Dependencies

**Required:**
- **tianqin-data** - For `update-dominant` command to query open interest

**Data Source:**
- **akshare-data** - For `generate_trading_hours.py` to read futures.md table

---

## Data Flow

### Trading Hours Check Flow

```
User: is-trading SHFE.rb2601
    ↓
[1] Parse symbol → exchange="SHFE", variety="rb"
    ↓
[2] Load trading_hours.json
    ↓
[3] Get current time (Asia/Shanghai)
    ↓
[4] Check if in day/night sessions
    ↓
[5] Return: {"trading": true/false, "session": "day"/"night"/null}
```

**Performance:** <1ms (local file read + time calculation)

---

### Dominant Contract Query Flow

```
User: dominant-contract rb
    ↓
[1] Load dominant_contracts.json
    ↓
[2] Lookup variety "rb"
    ↓
[3] Found? → Return {"symbol": "rb", "dominant": "rb2505", ...}
    Not Found? → Error: "Run 'update-dominant' first"
```

**Performance:** <1ms (local file read + dict lookup)

---

### Dominant Contract Update Flow

```
User: update-dominant [--varieties rb,cu]
    ↓
[1] Determine update scope (all or specified)
    ↓
[2] For each variety:
    ├─ Generate candidate contracts (rb2603, rb2604, ...)
    ├─ Call tianqin API: quote for each contract
    ├─ Parse open_interest from response
    └─ Find contract with max open_interest
    ↓
[3] Write results to dominant_contracts.json
    ↓
[4] Return: {"updated": N, "failed": M, "timestamp": "..."}
```

**Performance:**
- Serial: ~60 seconds for 30 varieties (6 contracts each)
- Parallel (10 workers): ~10-15 seconds

---

## Error Handling

### Invalid Symbol Format

**Error:** User inputs `rb2601` instead of `SHFE.rb2601`

**Solution:**
```python
if '.' not in symbol:
    raise ValueError(
        f"Invalid symbol format: {symbol}. "
        f"Expected: EXCHANGE.SYMBOL (e.g., SHFE.rb2601)"
    )
```

---

### Variety Not Found

**Error:** Trading hours not configured for requested variety

**Solution:**
```python
if variety not in self.config[exchange]:
    raise ValueError(
        f"Variety {variety} not found in {exchange}. "
        f"Check data/trading_hours.json or run generate_trading_hours.py"
    )
```

---

### API Failures During Update

**Error:** tianqin API call fails or times out

**Solution:**
- Catch exceptions per variety, continue updating others
- Return summary with failed count
- Log warnings to stderr

```python
try:
    oi = get_contract_open_interest(exchange, contract)
except Exception as e:
    print(f"Warning: Failed to get {symbol}: {e}", file=sys.stderr)
    return None
```

---

### Missing Dominant Contract

**Error:** User queries before running `update-dominant`

**Solution:**
```python
if variety not in self.config:
    raise ValueError(
        f"Variety '{variety}' not found. "
        f"Run 'update-dominant' command first."
    )
```

---

## Testing Strategy

### Unit Tests

**test_trading_hours.py:**
- `test_parse_symbol()` - Verify symbol parsing
- `test_parse_time_range()` - Verify time range parsing
- `test_is_cross_midnight()` - Verify cross-midnight detection
- `test_is_in_time_range()` - Verify time range checking (normal & cross-midnight)

**test_dominant_contract.py:**
- `test_generate_contract_codes()` - Verify contract code generation
- `test_get_dominant()` - Verify dominant contract lookup
- `test_config_save_load()` - Verify JSON serialization

---

### Integration Tests

**test_integration.py:**
- Test full CLI: `is-trading` command
- Test full CLI: `dominant-contract` command
- Test full CLI: `update-dominant` command (with mock or test variety)

**Execution:**
```bash
cd scripts/tests
python3 test_integration.py
```

---

### Manual Testing

```bash
# Test 1: Trading hours check
python3 scripts/trade_utils.py is-trading SHFE.rb2601
python3 scripts/trade_utils.py is-trading CFFEX.IF2603

# Test 2: Update dominant contracts (1-2 varieties)
python3 scripts/trade_utils.py update-dominant --varieties rb,cu

# Test 3: Query dominant contract
python3 scripts/trade_utils.py dominant-contract rb
python3 scripts/trade_utils.py dominant-contract cu

# Test 4: Full update (optional, takes time)
# python3 scripts/trade_utils.py update-dominant
```

---

## Deployment Steps

### Step 1: Create Directory Structure

```bash
cd /Users/ppsteven/projects/skills/trade-skills
mkdir -p scripts/data
```

---

### Step 2: Implement Scripts

1. Write `scripts/trade_utils.py` (~300 lines)
2. Write `scripts/generate_trading_hours.py` (~80 lines)

---

### Step 3: Generate Trading Hours Config

```bash
cd scripts
python3 generate_trading_hours.py
```

**Expected output:**
```
Parsing futures.md...
Found 75 varieties across 6 exchanges
✅ Generated: data/trading_hours.json
```

---

### Step 4: Initialize Dominant Contracts

```bash
# Create empty file
echo '{}' > data/dominant_contracts.json

# Update with real data
export TQ_API_KEY="your_key_here"
python3 trade_utils.py update-dominant --varieties rb,cu,al
```

---

### Step 5: Update SKILL.md

Add "Scripts & Utilities" section to `trade-skills/SKILL.md` documenting:
- Trading hours check command
- Dominant contract query command
- Update dominant command
- Configuration files
- Troubleshooting guide

---

### Step 6: Commit Changes

```bash
git add scripts/ docs/plans/
git commit -m "feat(trade-skills): add futures utilities for trading hours and dominant contracts

- Add is-trading command to check if contract is currently tradable
- Add dominant-contract command to query main contract by variety
- Add update-dominant command to refresh dominant contracts via API
- Generate trading_hours.json from akshare-data/references/futures.md
- Update SKILL.md with utilities documentation"
```

---

## Performance Considerations

### Trading Hours Check
- **Query time:** <1ms
- **Method:** Local JSON file + time calculation
- **No network calls**

---

### Dominant Contract Query
- **Query time:** <1ms
- **Method:** Local JSON file lookup
- **No network calls**

---

### Dominant Contract Update
- **Base performance:** ~60 seconds for 30 varieties (serial API calls)
- **Optimization:** Use concurrent API calls (ThreadPoolExecutor)
- **Optimized performance:** ~10-15 seconds with 10 workers

**Optimization implementation:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def update_dominant_concurrent(varieties, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(update_variety, v, e): (v, e)
            for v, e in update_list
        }
        # Collect results as they complete
```

---

## Maintenance

### Weekly Tasks

Run `update-dominant` to refresh dominant contracts:
```bash
python3 scripts/trade_utils.py update-dominant
```

**Automation via cron:**
```bash
# Add to crontab: Update every Monday at 9:00 AM
0 9 * * 1 cd /path/to/trade-skills/scripts && python3 trade_utils.py update-dominant
```

---

### When Trading Hours Change

1. Update table in `akshare-data/references/futures.md`
2. Regenerate config:
   ```bash
   python3 scripts/generate_trading_hours.py
   ```
3. Commit updated `trading_hours.json`

---

### When New Varieties Launch

1. Add new row to futures.md trading hours table
2. Regenerate trading hours config
3. Run update-dominant to populate new variety

---

## Future Enhancements

### Potential Improvements

1. **Auto-detect exchange from variety code** - Avoid requiring full `EXCHANGE.SYMBOL` format
2. **Multi-language support** - Support English and Chinese output
3. **Web API wrapper** - Expose utilities as HTTP endpoints
4. **Notification system** - Alert when dominant contract changes
5. **Historical dominant contracts** - Track dominant contract changes over time

---

## Success Criteria

### Functional Requirements ✅

- [ ] `is-trading` command returns correct trading status for all varieties
- [ ] Handles cross-midnight night sessions correctly (e.g., 21:00-01:00)
- [ ] `dominant-contract` command returns cached dominant contracts
- [ ] `update-dominant` command successfully queries API and updates database
- [ ] All 75+ varieties from futures.md are supported

---

### Non-Functional Requirements ✅

- [ ] Trading hours check responds in <5ms
- [ ] Dominant contract query responds in <5ms
- [ ] Update command completes in <2 minutes
- [ ] Error messages are clear and actionable
- [ ] Documentation is complete in SKILL.md

---

## Risks & Mitigations

### Risk 1: Timezone Issues

**Risk:** System timezone differs from China timezone, causing incorrect trading status

**Mitigation:**
- Explicitly use `Asia/Shanghai` timezone
- Consider adding `pytz` for robust timezone handling

---

### Risk 2: API Rate Limiting

**Risk:** tianqin API may rate-limit during `update-dominant`

**Mitigation:**
- Add retry logic with exponential backoff
- Allow partial updates (some varieties succeed, some fail)
- Document recommended update frequency (weekly, not daily)

---

### Risk 3: Contract Month Logic

**Risk:** Different varieties have different contract month patterns (连续月 vs 季月)

**Mitigation:**
- Use simple approach: generate all months for next 6 months
- API will fail for non-existent contracts (handled gracefully)
- Most active contracts will be found within 6-month window

---

### Risk 4: Data Staleness

**Risk:** Users forget to update dominant contracts, use stale data

**Mitigation:**
- Include `updated_at` timestamp in output
- Document recommended update frequency
- Consider adding warning if data is >7 days old

---

## Alternatives Considered

### Alternative 1: Real-time API for Dominant Contracts

**Approach:** Query tianqin API on every `dominant-contract` call

**Rejected because:**
- Performance: Each query takes 200-500ms
- API quota: Wasteful of API calls
- Reliability: Single point of failure

---

### Alternative 2: Embedded Trading Hours Data

**Approach:** Hardcode trading hours in Python code instead of JSON

**Rejected because:**
- Maintainability: Harder to update when hours change
- Readability: JSON is more human-readable
- Flexibility: JSON allows easy manual edits

---

### Alternative 3: Runtime Markdown Parsing

**Approach:** Parse futures.md on every trading hours check

**Rejected because:**
- Performance: Markdown parsing adds 10-50ms overhead
- Complexity: Requires Markdown parsing library
- Dependency: Tight coupling with akshare-data directory structure

---

## Conclusion

This design provides lightweight, performant utilities for futures trading operations:

- **Trading hours check** - Fast local calculation, no API calls
- **Dominant contract management** - Cached data with manual refresh
- **Clean architecture** - Single-file implementation, clear responsibilities
- **Easy maintenance** - JSON configs, automated generation scripts

The hybrid approach (static + manual update) balances data freshness, query performance, and API quota management effectively.

---

## Next Steps

1. Review and approve this design document
2. Create implementation plan using `writing-plans` skill
3. Implement `trade_utils.py` and `generate_trading_hours.py`
4. Generate initial `trading_hours.json`
5. Test all three commands
6. Update `SKILL.md` with documentation
7. Commit and deploy
