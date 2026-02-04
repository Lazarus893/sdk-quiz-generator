# Unit Test Question Examples

This file demonstrates diverse Unit Test questions with varied symbols and fields.

**Note:** All questions use 2024 historical data to ensure stable, unique answers.

## Example 1: Largest Value Query (QQQ)

**Question:** As of December 31, 2024, what is QQQ's largest country weighting?

**Query Params:**
```json
{"symbol": "QQQ", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, United States is QQQ's largest country weighting at 94.66%.

---

## Example 2: Specific Field Lookup (SPY)

**Question:** As of December 31, 2024, what is the United Kingdom's weight percentage in SPY?

**Query Params:**
```json
{"symbol": "SPY", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, the United Kingdom's weight percentage in SPY is 1.02%.

---

## Example 3: Count Aggregation (IWM)

**Question:** As of December 31, 2024, how many countries are represented in IWM's holdings?

**Query Params:**
```json
{"symbol": "IWM", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, IWM's holdings are represented across 7 country categories.

---

## Example 4: Top-N Ranking (DIA)

**Question:** As of December 31, 2024, what are the top three countries by weighting in DIA?

**Query Params:**
```json
{"symbol": "DIA", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, the top three countries by weighting in DIA are: 1) United States at 98.12%, 2) United Kingdom at 0.95%, and 3) Netherlands at 0.48%.

---

## Example 5: Comparison Between Values (VTI)

**Question:** As of December 31, 2024, what is the difference in weight percentage between Canada and Ireland in VTI?

**Query Params:**
```json
{"symbol": "VTI", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, the difference in weight percentage between Canada (2.15%) and Ireland (0.62%) in VTI is 1.53 percentage points.

---

## Example 6: Smallest Value Query (VOO)

**Question:** As of December 31, 2024, what is VOO's smallest non-zero country weighting (excluding "Other")?

**Query Params:**
```json
{"symbol": "VOO", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, VOO's smallest non-zero country weighting (excluding "Other") is Australia at 0.08%.

---

## Example 7: Presence Check (ARKK)

**Question:** As of December 31, 2024, does ARKK have any exposure to Switzerland?

**Query Params:**
```json
{"symbol": "ARKK", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, yes, ARKK has exposure to Switzerland at 0.32% of the portfolio.

---

## Example 8: Combined Weight (EEM)

**Question:** As of December 31, 2024, what is the combined weight of all Asian countries in EEM?

**Query Params:**
```json
{"symbol": "EEM", "as_of_date": "2024-12-31"}
```

**Answer:** As of December 31, 2024, the combined weight of Asian countries (China, South Korea, Taiwan, India) in EEM is 78.45%.

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
