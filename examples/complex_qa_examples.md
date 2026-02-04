# Complex QA Question Examples

Complex QA questions require **multi-hop queries** and **calculations** across multiple data points. They often specify data selection criteria (e.g., "use closest date to...").

## Example 1: Multi-Step Calculation with Date Requirement

**Question:** What was Apple's Free Cash Flow per Share for fiscal year 2024? Outstanding shares count should use the closest to its fiscal year-end date (September 30, 2024).

**Query Steps:**
1. Get Free Cash Flow for fiscal year 2024
2. Get outstanding shares count closest to September 30, 2024
3. Calculate: Free Cash Flow / Outstanding Shares

**Answer:** Apple's Free Cash Flow per Share for fiscal year 2024 was $6.82. This is calculated by dividing the Free Cash Flow of $108.5B by the outstanding shares count of 15.9B as of September 30, 2024 (the closest date to fiscal year-end).

---

## Example 2: Ratio Calculation Across Quarters

**Question:** What is the revenue growth rate between Q3 2024 and Q4 2024 for Microsoft?

**Query Steps:**
1. Get Q3 2024 revenue
2. Get Q4 2024 revenue
3. Calculate: (Q4 - Q3) / Q3 * 100%

**Answer:** Microsoft's revenue grew 12.3% from Q3 2024 ($56.2B) to Q4 2024 ($63.1B), calculated as (63.1 - 56.2) / 56.2 * 100% = 12.28%.

---

## Example 3: Combined Metric from Multiple Sources

**Question:** What is Tesla's operating margin for fiscal year 2024? Use operating income and total revenue for the full year.

**Query Steps:**
1. Get total revenue for fiscal year 2024
2. Get operating income for fiscal year 2024
3. Calculate: Operating Income / Total Revenue * 100%

**Answer:** Tesla's operating margin for fiscal year 2024 was 14.2%, calculated from operating income of $13.8B divided by total revenue of $97.2B.

---

## Example 4: Year-over-Year Comparison

**Question:** How did Google's R&D spending as a percentage of revenue change from 2023 to 2024?

**Query Steps:**
1. Get 2023 R&D spending and revenue
2. Get 2024 R&D spending and revenue
3. Calculate R&D % for both years
4. Compare the difference

**Answer:** Google's R&D spending as a percentage of revenue increased from 15.2% in 2023 ($21.5B / $141.5B) to 16.1% in 2024 ($25.8B / $160.2B), an increase of 0.9 percentage points.

---

## Example 5: Weighted Average Calculation

**Question:** What is the weighted average P/E ratio of the top 5 holdings in QQQ by market cap as of December 31, 2024?

**Query Steps:**
1. Get top 5 holdings by market cap
2. Get P/E ratio for each holding
3. Get weight of each holding in QQQ
4. Calculate weighted average: Σ(P/E × weight)

**Answer:** The weighted average P/E ratio of QQQ's top 5 holdings (AAPL, MSFT, GOOGL, AMZN, NVDA) as of December 31, 2024 was 32.4, calculated as: (28.5 × 0.112) + (35.2 × 0.089) + (26.8 × 0.065) + (45.1 × 0.054) + (38.9 × 0.048) = 32.4.

---

## Example 6: Debt-to-Equity Trend Analysis

**Question:** What is the trend in Amazon's debt-to-equity ratio from Q1 2024 to Q4 2024? Calculate the ratio for each quarter.

**Query Steps:**
1. Get total debt and total equity for Q1, Q2, Q3, Q4 2024
2. Calculate D/E ratio for each quarter
3. Analyze trend (increasing/decreasing)

**Answer:** Amazon's debt-to-equity ratio showed a declining trend in 2024:
- Q1 2024: 0.82 ($185B debt / $226B equity)
- Q2 2024: 0.78 ($182B / $233B)
- Q3 2024: 0.74 ($180B / $243B)
- Q4 2024: 0.71 ($179B / $252B)
The ratio decreased 0.11 points over the year, indicating improved leverage.

---

## Example 7: Multi-Company Comparison

**Question:** Among the "Magnificent 7" tech stocks (AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META), which had the highest earnings growth rate in fiscal year 2024 compared to 2023?

**Query Steps:**
1. Get fiscal 2023 and 2024 earnings for all 7 companies
2. Calculate growth rate for each: (2024 - 2023) / 2023 * 100%
3. Rank and identify the highest

**Answer:** NVDA had the highest earnings growth rate at 118.5%, growing from $29.8B in fiscal 2023 to $65.1B in fiscal 2024. The full ranking:
1. NVDA: +118.5%
2. META: +52.3%
3. TSLA: +38.7%
4. AMZN: +24.1%
5. GOOGL: +18.9%
6. MSFT: +16.2%
7. AAPL: +12.4%

---

## Example 8: Time-Series Aggregation

**Question:** What was the total cumulative dividend payout by Apple over the past 4 years (2021-2024)? Adjust for the 4-for-1 stock split in August 2020.

**Query Steps:**
1. Get dividend per share for each year 2021-2024
2. Get shares outstanding for each year
3. Adjust for stock split if needed
4. Calculate: Σ(dividend per share × shares outstanding) for each year

**Answer:** Apple's cumulative dividend payout from 2021-2024 was $60.4B:
- 2021: $14.5B ($0.82/share × 17.7B shares)
- 2022: $14.9B ($0.85/share × 17.5B shares)
- 2023: $15.2B ($0.90/share × 16.9B shares)
- 2024: $15.8B ($0.94/share × 16.8B shares)
Total: $60.4B

---

## Key Characteristics of Complex QA

1. **Multi-hop queries** - Requires combining data from 2+ API calls or fields
2. **Calculations** - Involves arithmetic operations (division, percentages, growth rates)
3. **Data selection criteria** - Specifies which data to use (e.g., "closest to date", "top N by...")
4. **Time-based comparisons** - Quarter-over-quarter, year-over-year trends
5. **Cross-entity analysis** - Comparing multiple companies or instruments
6. **Aggregations** - Sums, averages, weighted calculations
7. **Adjustments** - Stock splits, currency conversion, inflation adjustment

## Answer Requirements

- Show **step-by-step calculations**
- Cite **specific numbers** from source data
- Include **dates** when relevant
- Explain **methodology** (which data was selected and why)
- Present **final result** clearly with units
