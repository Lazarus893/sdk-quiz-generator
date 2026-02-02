# Unit Test Question Examples

This file demonstrates diverse Unit Test questions with varied symbols and fields.

## Example 1: Largest Value Query (QQQ)

**Question:** What is QQQ's largest country weighting?

**Query Params:**
```json
{"symbol": "QQQ"}
```

**Answer:** United States is QQQ's largest country weighting at 94.66%.

---

## Example 2: Specific Field Lookup (SPY)

**Question:** What is the United Kingdom's weight percentage in SPY?

**Query Params:**
```json
{"symbol": "SPY"}
```

**Answer:** The United Kingdom's weight percentage in SPY is 1.02%.

---

## Example 3: Count Aggregation (IWM)

**Question:** How many countries are represented in IWM's holdings?

**Query Params:**
```json
{"symbol": "IWM"}
```

**Answer:** IWM's holdings are represented across 7 country categories.

---

## Example 4: Top-N Ranking (DIA)

**Question:** What are the top three countries by weighting in DIA?

**Query Params:**
```json
{"symbol": "DIA"}
```

**Answer:** The top three countries by weighting in DIA are: 1) United States at 98.12%, 2) United Kingdom at 0.95%, and 3) Netherlands at 0.48%.

---

## Example 5: Comparison Between Values (VTI)

**Question:** What is the difference in weight percentage between Canada and Ireland in VTI?

**Query Params:**
```json
{"symbol": "VTI"}
```

**Answer:** The difference in weight percentage between Canada (2.15%) and Ireland (0.62%) in VTI is 1.53 percentage points.

---

## Example 6: Smallest Value Query (VOO)

**Question:** What is VOO's smallest non-zero country weighting (excluding "Other")?

**Query Params:**
```json
{"symbol": "VOO"}
```

**Answer:** VOO's smallest non-zero country weighting (excluding "Other") is Australia at 0.08%.

---

## Example 7: Presence Check (ARKK)

**Question:** Does ARKK have any exposure to Switzerland?

**Query Params:**
```json
{"symbol": "ARKK"}
```

**Answer:** Yes, ARKK has exposure to Switzerland at 0.32% of the portfolio.

---

## Example 8: Combined Weight (EEM)

**Question:** What is the combined weight of all Asian countries in EEM?

**Query Params:**
```json
{"symbol": "EEM"}
```

**Answer:** The combined weight of Asian countries (China, South Korea, Taiwan, India) in EEM is 78.45%.

---

## Key Variations Demonstrated

1. **Symbol diversity:** QQQ, SPY, IWM, DIA, VTI, VOO, ARKK, EEM
2. **Query types:**
   - Largest/smallest value
   - Specific field lookup
   - Count aggregation
   - Top-N ranking
   - Comparison between fields
   - Presence check
   - Combined calculation
3. **Different countries tested:** US, UK, Netherlands, Canada, Ireland, Australia, Switzerland, Asian countries
4. **Edge cases:** Non-zero values, excluding categories, combined weights
