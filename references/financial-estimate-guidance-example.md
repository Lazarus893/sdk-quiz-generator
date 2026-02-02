# Financial Estimate & Guidance API Documentation

## Overview

Two related APIs for accessing FactSet consensus estimates and company-provided guidance data.

---

# 1. Financial Estimate API

## Purpose

Fetch analyst consensus estimates for financial metrics (revenue, EPS, EBITDA, etc.) from FactSet.

## Function Signature

```typescript
async function financialEstimate(params: FinancialEstimateParams): Promise<FinancialEstimateResponse>
```

## Parameters

### FinancialEstimateParams

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | `string` | ✅ | Stock ticker symbol (e.g., "AAPL", "MSFT") |
| `metrics` | `string[]` | ❌ | Array of metrics to fetch (default: all available) |
| `observedAtStart` | `string` | ❌ | ISO date string - start of observation window |
| `observedAtEnd` | `string` | ❌ | ISO date string - end of observation window |
| `fiscalYear` | `number` | ❌ | Filter by fiscal year (e.g., 2024) |
| `fiscalQuarter` | `number` | ❌ | Filter by fiscal quarter (1-4) |
| `periodicity` | `"annual" \| "quarterly"` | ❌ | Filter by reporting period type |
| `limit` | `number` | ❌ | Maximum number of records to return (default: 100) |

**Available metrics:**
- `revenue` - Total revenue
- `eps` - Earnings per share
- `ebitda` - Earnings before interest, taxes, depreciation, amortization
- `netIncome` - Net income
- `operatingIncome` - Operating income

**Notes:**
- `observedAtStart` and `observedAtEnd` define when the estimate was recorded (not the fiscal period)
- If `fiscalYear` is provided, `fiscalQuarter` can narrow down to a specific quarter
- `periodicity` filters estimates by whether they're annual or quarterly forecasts

## Response Structure

### FinancialEstimateResponse

```typescript
interface FinancialEstimateResponse {
  estimates: EstimateRecord[];
  metadata: {
    symbol: string;
    totalRecords: number;
    fetchedAt: string;
  };
}

interface EstimateRecord {
  // Identification
  symbol: string;
  metric: string;
  fiscalYear: number;
  fiscalQuarter?: number;
  periodicity: "annual" | "quarterly";
  observedAt: string; // ISO date when estimate was recorded
  
  // Consensus statistics
  mean: number;
  median: number;
  standardDeviation: number;
  high: number;
  low: number;
  
  // Analyst activity
  estimateCount: number; // Total number of analyst estimates
  up: number;            // Analysts who revised upward
  down: number;          // Analysts who revised downward
}
```

**Field descriptions:**

- **mean**: Average of all analyst estimates
- **median**: Middle value when estimates are sorted
- **standardDeviation**: Measure of estimate dispersion (higher = more disagreement)
- **high/low**: Highest and lowest analyst estimates
- **estimateCount**: Total number of analysts covering this metric
- **up/down**: Number of analysts who revised their estimate up/down since last period

## Example Usage

```typescript
// Fetch Q4 2024 revenue estimates for Apple
const response = await financialEstimate({
  symbol: "AAPL",
  metrics: ["revenue"],
  fiscalYear: 2024,
  fiscalQuarter: 4,
  periodicity: "quarterly"
});

console.log(response.estimates[0].mean); // Average revenue estimate
console.log(response.estimates[0].estimateCount); // Number of analysts

// Track estimate changes over time
const january = await financialEstimate({
  symbol: "AAPL",
  metrics: ["eps"],
  observedAtStart: "2024-01-01",
  observedAtEnd: "2024-01-31"
});

const february = await financialEstimate({
  symbol: "AAPL",
  metrics: ["eps"],
  observedAtStart: "2024-02-01",
  observedAtEnd: "2024-02-28"
});

// Compare mean EPS estimate changes
const drift = february.estimates[0].mean - january.estimates[0].mean;
```

---

# 2. Guidance API

## Purpose

Fetch company-provided guidance and compare it with analyst consensus estimates.

## Function Signature

```typescript
async function guidance(params: GuidanceParams): Promise<GuidanceResponse>
```

## Parameters

### GuidanceParams

**Same parameters as Financial Estimate API** (see above).

The only difference is the response structure, which includes guidance-specific fields.

## Response Structure

### GuidanceResponse

```typescript
interface GuidanceResponse {
  guidanceRecords: GuidanceRecord[];
  metadata: {
    symbol: string;
    totalRecords: number;
    fetchedAt: string;
  };
}

interface GuidanceRecord {
  // Identification (same as EstimateRecord)
  symbol: string;
  metric: string;
  fiscalYear: number;
  fiscalQuarter?: number;
  periodicity: "annual" | "quarterly";
  observedAt: string;
  
  // Company guidance
  guidanceMidpoint: number;    // Midpoint of company's guidance range
  guidanceLow: number;         // Lower bound of guidance
  guidanceHigh: number;        // Upper bound of guidance
  
  // Consensus comparison
  meanBefore: number;          // Analyst mean BEFORE guidance was issued
  meanAfter: number;           // Analyst mean AFTER guidance was issued
  meanSurpriseAmt: number;     // Difference (guidance - meanBefore)
  meanSurprisePct: number;     // Percentage difference
  
  // Previous guidance
  prevMidpoint?: number;       // Previous quarter's guidance midpoint
  guidanceChange?: number;     // Change from previous guidance
  guidanceChangePct?: number;  // Percentage change from previous
}
```

**Field descriptions:**

- **guidanceMidpoint**: Middle of the company's guidance range (average of low and high)
- **guidanceLow/High**: The range provided by the company
- **meanBefore**: What analysts expected BEFORE company announced guidance
- **meanAfter**: What analysts expect AFTER guidance (often converges toward guidance)
- **meanSurpriseAmt**: How much guidance differs from pre-announcement consensus (positive = beat expectations)
- **prevMidpoint**: Last guidance midpoint (for tracking guidance revisions)
- **guidanceChange**: Difference from previous guidance

## Example Usage

```typescript
// Check if Apple's Q1 2024 guidance beat expectations
const response = await guidance({
  symbol: "AAPL",
  metrics: ["revenue"],
  fiscalYear: 2024,
  fiscalQuarter: 1
});

const record = response.guidanceRecords[0];

console.log(`Guidance: ${record.guidanceMidpoint}`);
console.log(`Analyst expectation before: ${record.meanBefore}`);
console.log(`Surprise: ${record.meanSurprisePct}%`);

if (record.meanSurprisePct > 0) {
  console.log("Company guided ABOVE analyst expectations! 📈");
} else {
  console.log("Company guided BELOW analyst expectations 📉");
}

// Track guidance revisions over time
const q1 = await guidance({
  symbol: "AAPL",
  fiscalYear: 2024,
  fiscalQuarter: 1
});

const q2 = await guidance({
  symbol: "AAPL",
  fiscalYear: 2024,
  fiscalQuarter: 2
});

console.log(`Q1 guidance: ${q1.guidanceRecords[0].guidanceMidpoint}`);
console.log(`Q2 guidance: ${q2.guidanceRecords[0].guidanceMidpoint}`);
console.log(`Change: ${q2.guidanceRecords[0].guidanceChange}`);
```

## Common Use Cases

### 1. Estimate Momentum Analysis
Track how analyst estimates change over time (are they getting more optimistic or pessimistic?).

```typescript
const estimates = await financialEstimate({
  symbol: "TSLA",
  metrics: ["eps"],
  observedAtStart: "2024-01-01",
  observedAtEnd: "2024-12-31",
  fiscalYear: 2025
});

// Analyze up/down revisions
const totalRevisions = estimates.estimates.reduce((sum, e) => sum + e.up + e.down, 0);
const positiveRevisions = estimates.estimates.reduce((sum, e) => sum + e.up, 0);
const revisionRatio = positiveRevisions / totalRevisions;

console.log(`${(revisionRatio * 100).toFixed(1)}% of revisions were positive`);
```

### 2. Guidance Surprise Detection
Identify when companies provide guidance significantly different from expectations.

```typescript
const guidanceData = await guidance({
  symbol: "NVDA",
  fiscalYear: 2024,
  periodicity: "quarterly"
});

const surprises = guidanceData.guidanceRecords
  .filter(r => Math.abs(r.meanSurprisePct) > 10) // >10% surprise
  .sort((a, b) => Math.abs(b.meanSurprisePct) - Math.abs(a.meanSurprisePct));

console.log("Biggest guidance surprises:");
surprises.forEach(s => {
  console.log(`Q${s.fiscalQuarter} ${s.metric}: ${s.meanSurprisePct.toFixed(1)}% surprise`);
});
```

### 3. Estimate Consensus Strength
Measure analyst agreement (low standard deviation = strong consensus).

```typescript
const estimates = await financialEstimate({
  symbol: "AAPL",
  metrics: ["revenue"],
  fiscalYear: 2024,
  fiscalQuarter: 4
});

const record = estimates.estimates[0];
const coefficientOfVariation = (record.standardDeviation / record.mean) * 100;

if (coefficientOfVariation < 5) {
  console.log("Strong consensus - analysts agree closely");
} else if (coefficientOfVariation > 15) {
  console.log("Weak consensus - wide disagreement among analysts");
}
```

## Error Handling

```typescript
try {
  const estimates = await financialEstimate({
    symbol: "INVALID",
    fiscalYear: 2024
  });
} catch (error) {
  if (error.code === "SYMBOL_NOT_FOUND") {
    console.error("Invalid stock symbol");
  } else if (error.code === "NO_DATA_AVAILABLE") {
    console.error("No estimates available for this period");
  } else if (error.code === "RATE_LIMIT_EXCEEDED") {
    console.error("Too many requests - wait and retry");
  }
}
```

## Rate Limits

- **Free tier**: 100 requests per day
- **Pro tier**: 1,000 requests per day
- **Enterprise**: Unlimited

## Data Freshness

- Estimates are updated every 24 hours
- Guidance data is updated within 1 hour of company announcements
