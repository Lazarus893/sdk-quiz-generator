# createOHLCVProvider API Documentation

## Overview

`createOHLCVProvider` creates a custom OHLCV (Open, High, Low, Close, Volume) data provider for financial charting and analysis.

## Function Signature

```typescript
function createOHLCVProvider(config: OHLCVProviderConfig): OHLCVProvider
```

## Parameters

### config: OHLCVProviderConfig

Configuration object for the OHLCV provider.

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| `dataSource` | `string` | Data source identifier (e.g., "yahoo", "alpha-vantage") |
| `symbol` | `string` | Stock symbol or ticker (e.g., "AAPL", "GOOGL") |
| `interval` | `string` | Time interval for candles: "1m", "5m", "15m", "1h", "1d", "1w", "1M" |

**Optional fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `startDate` | `Date \| string` | 1 year ago | Start date for historical data |
| `endDate` | `Date \| string` | now | End date for historical data |
| `apiKey` | `string` | undefined | API key for data source (required for some sources) |
| `adjustForSplits` | `boolean` | true | Whether to adjust prices for stock splits |
| `adjustForDividends` | `boolean` | true | Whether to adjust prices for dividends |
| `limit` | `number` | 1000 | Maximum number of candles to fetch |

## Return Value

### OHLCVProvider

Object containing OHLCV data and metadata.

**Structure:**

```typescript
interface OHLCVProvider {
  data: OHLCVCandle[];
  metadata: {
    symbol: string;
    interval: string;
    dataSource: string;
    fetchedAt: Date;
    count: number;
  };
  refresh(): Promise<void>;
}

interface OHLCVCandle {
  timestamp: Date;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

**Fields:**

- `data`: Array of OHLCV candles sorted by timestamp (ascending)
- `metadata`: Information about the dataset
  - `symbol`: The requested symbol
  - `interval`: The time interval used
  - `dataSource`: Which data source provided the data
  - `fetchedAt`: When the data was fetched
  - `count`: Number of candles returned
- `refresh()`: Async method to fetch updated data

## Example Usage

```typescript
// Basic usage
const provider = createOHLCVProvider({
  dataSource: "yahoo",
  symbol: "AAPL",
  interval: "1d"
});

console.log(provider.data.length); // Number of daily candles
console.log(provider.data[0].close); // Closing price of first candle

// Advanced usage with custom date range
const provider = createOHLCVProvider({
  dataSource: "alpha-vantage",
  symbol: "MSFT",
  interval: "5m",
  startDate: "2024-01-01",
  endDate: "2024-01-31",
  apiKey: process.env.ALPHA_VANTAGE_KEY,
  limit: 500
});

// Refresh data
await provider.refresh();
```

## Error Conditions

| Error | Condition | Solution |
|-------|-----------|----------|
| `InvalidSymbolError` | Symbol not found or invalid format | Verify symbol exists and format is correct |
| `APIKeyRequiredError` | Data source requires API key but none provided | Provide `apiKey` in config |
| `RateLimitError` | Too many requests to data source | Wait and retry, or upgrade API plan |
| `DateRangeError` | `startDate` is after `endDate` | Ensure `startDate` < `endDate` |
| `InvalidIntervalError` | Unsupported interval for data source | Check supported intervals for your data source |

## Performance Considerations

- Smaller intervals (1m, 5m) return more data; use `limit` to control size
- Some data sources charge per API call; use caching when possible
- `refresh()` makes a new API call; avoid calling too frequently
- Stock split/dividend adjustments add processing time

## Data Source Support

| Source | Intervals | API Key Required | Rate Limit |
|--------|-----------|------------------|------------|
| yahoo | 1m, 5m, 15m, 1h, 1d, 1w, 1M | No | ~2000/hour |
| alpha-vantage | 1m, 5m, 15m, 30m, 60m, 1d | Yes | 5/min (free), 75/min (premium) |
| binance | 1m, 5m, 15m, 1h, 4h, 1d, 1w | No | 1200/min |
