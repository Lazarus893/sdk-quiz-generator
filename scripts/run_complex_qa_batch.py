#!/usr/bin/env python3
"""
Execute Complex QA batch: fetch real SDK data and compute answers.
No LLM required — answers are calculated programmatically from solution steps.
"""

import requests
import json
import sys
import math
from typing import Dict, Any, List


API_KEY = "2f21e762-fa1c-4eb8-a8ce-ec8c1e138812"
HEADERS = {
    "accept": "application/json",
    "X-API-Key": API_KEY
}


def call_gateway(request_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get(request_url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def solve_q1(responses):
    """Forward P/E Ratio: price_close / epsAvg"""
    fe = responses[0]["data"][0]
    eps_avg = float(fe["epsAvg"])

    kline_data = responses[1]["response"]["data"]
    # Sort by time_open descending (API returns newest first), take first
    latest = kline_data[0]
    price_close = latest["price_close"]

    pe = price_close / eps_avg
    return (
        f"AVGO FY2025 consensus epsAvg = ${eps_avg:.5f}\n"
        f"Most recent closing price ({latest['time_period_start'][:10]}): ${price_close:.2f}\n"
        f"Forward P/E = ${price_close:.2f} / ${eps_avg:.5f} = {pe:.2f}x"
    )


def solve_q2(responses):
    """VWAP = sum(TP * volume) / sum(volume), TP = (H+L+C)/3"""
    candles = responses[0]["response"]["data"]
    sum_tp_vol = 0
    sum_vol = 0
    for c in candles:
        tp = (c["price_high"] + c["price_low"] + c["price_close"]) / 3
        sum_tp_vol += tp * c["volume_traded"]
        sum_vol += c["volume_traded"]

    if sum_vol == 0:
        return "No volume data available"

    vwap = sum_tp_vol / sum_vol
    return (
        f"AMD hourly candles on Jan 15, 2025: {len(candles)} candles\n"
        f"Total volume: {sum_vol:,}\n"
        f"VWAP = Σ(TP × volume) / Σ(volume) = {sum_tp_vol:,.2f} / {sum_vol:,} = ${vwap:.4f}"
    )


def solve_q3(responses):
    """Operating Margin YoY: ebitAvg/revenueAvg for each year"""
    fy24 = responses[0]["data"][0]
    fy25 = responses[1]["data"][0]

    ebit_24 = float(fy24["ebitAvg"])
    rev_24 = float(fy24["revenueAvg"])
    margin_24 = ebit_24 / rev_24 * 100

    ebit_25 = float(fy25["ebitAvg"])
    rev_25 = float(fy25["revenueAvg"])
    margin_25 = ebit_25 / rev_25 * 100

    change = margin_25 - margin_24
    direction = "expansion" if change > 0 else "contraction"
    return (
        f"CRM FY2024: ebitAvg = ${ebit_24:,.0f}, revenueAvg = ${rev_24:,.0f}, operating margin = {margin_24:.2f}%\n"
        f"CRM FY2025: ebitAvg = ${ebit_25:,.0f}, revenueAvg = ${rev_25:,.0f}, operating margin = {margin_25:.2f}%\n"
        f"Year-over-year margin {direction}: {change:+.2f} percentage points"
    )


def solve_q4(responses):
    """EPS spread vs price spread"""
    fe = responses[0]["data"][0]
    eps_high = float(fe["epsHigh"])
    eps_low = float(fe["epsLow"])
    eps_avg = float(fe["epsAvg"])
    eps_spread = (eps_high - eps_low) / eps_avg * 100

    candles = responses[1]["response"]["data"]
    max_high = max(c["price_high"] for c in candles)
    min_low = min(c["price_low"] for c in candles)
    avg_close = sum(c["price_close"] for c in candles) / len(candles)
    price_spread = (max_high - min_low) / avg_close * 100

    more_uncertain = "analyst disagreement on EPS" if eps_spread > price_spread else "market price action"
    return (
        f"NFLX FY2025 EPS: high=${eps_high:.5f}, low=${eps_low:.5f}, avg=${eps_avg:.5f}\n"
        f"EPS range spread = ({eps_high:.5f} − {eps_low:.5f}) / {eps_avg:.5f} = {eps_spread:.2f}%\n"
        f"\n"
        f"NFLX Jan 2025 price: max high=${max_high:.2f}, min low=${min_low:.2f}, avg close=${avg_close:.2f}\n"
        f"Price range spread = ({max_high:.2f} − {min_low:.2f}) / {avg_close:.2f} = {price_spread:.2f}%\n"
        f"\n"
        f"More relative uncertainty: {more_uncertain} ({max(eps_spread, price_spread):.2f}% vs {min(eps_spread, price_spread):.2f}%)"
    )


def solve_q5(responses):
    """Quarterly EPS growth trajectory"""
    eps = []
    for r in responses:
        data = r["data"][0]
        eps.append((data["fiscalQuarter"], float(data["epsAvg"])))

    lines = []
    for q, e in eps:
        lines.append(f"  {q}: epsAvg = ${e:.5f}")

    growths = []
    for i in range(1, len(eps)):
        g = (eps[i][1] - eps[i-1][1]) / eps[i-1][1] * 100
        growths.append(g)
        lines.append(f"  {eps[i-1][0]}→{eps[i][0]} growth: ({eps[i][1]:.5f} − {eps[i-1][1]:.5f}) / {eps[i-1][1]:.5f} = {g:+.2f}%")

    # Determine trajectory
    if all(growths[i] > growths[i-1] for i in range(1, len(growths))):
        trajectory = "accelerating"
    elif all(growths[i] < growths[i-1] for i in range(1, len(growths))):
        trajectory = "decelerating"
    else:
        trajectory = "uneven (mixed signals)"

    lines.append(f"\nTrajectory: EPS growth is {trajectory}")
    return "AAPL FY2024 quarterly EPS:\n" + "\n".join(lines)


def solve_q6(responses):
    """Annualized historical volatility from daily log returns"""
    candles = responses[0]["response"]["data"]
    # Sort by time ascending
    candles.sort(key=lambda c: c["time_open"])
    closes = [c["price_close"] for c in candles]

    if len(closes) < 2:
        return "Not enough data points"

    # Log returns
    log_returns = [math.log(closes[i] / closes[i-1]) for i in range(1, len(closes))]
    n = len(log_returns)
    mean_r = sum(log_returns) / n
    variance = sum((r - mean_r) ** 2 for r in log_returns) / (n - 1)
    sigma = math.sqrt(variance)
    annualized = sigma * math.sqrt(252) * 100

    return (
        f"JPM November 2024: {len(closes)} trading days, {n} daily log returns\n"
        f"Mean daily log return: {mean_r:.6f}\n"
        f"Daily standard deviation: {sigma:.6f}\n"
        f"Annualized volatility = {sigma:.6f} × √252 = {annualized:.2f}%"
    )


def solve_q7(responses):
    """SGA efficiency comparison"""
    amzn = responses[0]["data"][0]
    wmt = responses[1]["data"][0]

    amzn_sga = float(amzn["sgaExpenseAvg"])
    amzn_rev = float(amzn["revenueAvg"])
    amzn_ratio = amzn_sga / amzn_rev * 100

    wmt_sga = float(wmt["sgaExpenseAvg"])
    wmt_rev = float(wmt["revenueAvg"])
    wmt_ratio = wmt_sga / wmt_rev * 100

    gap = amzn_ratio - wmt_ratio
    more_efficient = "WMT" if wmt_ratio < amzn_ratio else "AMZN"
    return (
        f"AMZN FY2025: sgaExpenseAvg = ${amzn_sga:,.0f}, revenueAvg = ${amzn_rev:,.0f}\n"
        f"  SGA ratio = {amzn_ratio:.2f}%\n"
        f"WMT FY2025: sgaExpenseAvg = ${wmt_sga:,.0f}, revenueAvg = ${wmt_rev:,.0f}\n"
        f"  SGA ratio = {wmt_ratio:.2f}%\n"
        f"\n"
        f"Efficiency gap: {gap:+.2f} pp — {more_efficient} is more efficient in controlling overhead costs"
    )


def solve_q8(responses):
    """Incremental margin (drop-through rate)"""
    fy24 = responses[0]["data"][0]
    fy25 = responses[1]["data"][0]

    rev_24 = float(fy24["revenueAvg"])
    ni_24 = float(fy24["netIncomeAvg"])
    rev_25 = float(fy25["revenueAvg"])
    ni_25 = float(fy25["netIncomeAvg"])

    inc_rev = rev_25 - rev_24
    inc_ni = ni_25 - ni_24
    inc_margin = inc_ni / inc_rev * 100 if inc_rev != 0 else 0
    overall_24 = ni_24 / rev_24 * 100

    leverage = "positive operating leverage" if inc_margin > overall_24 else "diminishing returns on incremental revenue"
    return (
        f"MSFT FY2024: revenueAvg = ${rev_24:,.0f}, netIncomeAvg = ${ni_24:,.0f} (margin: {overall_24:.2f}%)\n"
        f"MSFT FY2025: revenueAvg = ${rev_25:,.0f}, netIncomeAvg = ${ni_25:,.0f}\n"
        f"\n"
        f"Incremental revenue: ${inc_rev:,.0f}\n"
        f"Incremental net income: ${inc_ni:,.0f}\n"
        f"Incremental margin = ${inc_ni:,.0f} / ${inc_rev:,.0f} = {inc_margin:.2f}%\n"
        f"\n"
        f"Since incremental margin ({inc_margin:.2f}%) {'>' if inc_margin > overall_24 else '<'} overall FY2024 margin ({overall_24:.2f}%), "
        f"MSFT shows {leverage}"
    )


def solve_q9(responses):
    """Weekly ATR%"""
    candles = responses[0]["response"]["data"]
    trs = [c["price_high"] - c["price_low"] for c in candles]
    atr = sum(trs) / len(trs)
    avg_close = sum(c["price_close"] for c in candles) / len(candles)
    atr_pct = atr / avg_close * 100

    return (
        f"TSLA Q4 2024: {len(candles)} weekly candles\n"
        f"Weekly true ranges: {', '.join(f'${tr:.2f}' for tr in trs)}\n"
        f"ATR = ${atr:.2f}\n"
        f"Average weekly close = ${avg_close:.2f}\n"
        f"ATR% = ${atr:.2f} / ${avg_close:.2f} = {atr_pct:.2f}%"
    )


def solve_q10(responses):
    """PEG Ratio"""
    fy24 = responses[0]["data"][0]
    fy25 = responses[1]["data"][0]
    kline = responses[2]["response"]["data"]

    eps_24 = float(fy24["epsAvg"])
    eps_25 = float(fy25["epsAvg"])
    growth = (eps_25 - eps_24) / eps_24 * 100

    avg_close = sum(c["price_close"] for c in kline) / len(kline)
    forward_pe = avg_close / eps_25
    peg = forward_pe / growth if growth != 0 else float('inf')

    valuation = "undervalued relative to growth" if peg < 1 else "paying a premium above growth rate"
    return (
        f"NVDA FY2024 epsAvg = ${eps_24:.5f}\n"
        f"NVDA FY2025 epsAvg = ${eps_25:.5f}\n"
        f"EPS growth rate = ({eps_25:.5f} − {eps_24:.5f}) / {eps_24:.5f} = {growth:.2f}%\n"
        f"\n"
        f"December 2024 avg closing price = ${avg_close:.2f} ({len(kline)} trading days)\n"
        f"Forward P/E = ${avg_close:.2f} / ${eps_25:.5f} = {forward_pe:.2f}x\n"
        f"PEG Ratio = {forward_pe:.2f} / {growth:.2f} = {peg:.2f}\n"
        f"\n"
        f"PEG {'< 1' if peg < 1 else '>= 1'}: the market is {valuation}"
    )


SOLVERS = {
    1: solve_q1, 2: solve_q2, 3: solve_q3, 4: solve_q4, 5: solve_q5,
    6: solve_q6, 7: solve_q7, 8: solve_q8, 9: solve_q9, 10: solve_q10,
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_complex_qa_batch.py <input.json>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1]) as f:
        questions = json.load(f)

    results = []

    for q in questions:
        qid = q["id"]
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Q{qid}: {q['question'][:80]}...", file=sys.stderr)

        # Fetch all SDK responses
        sdk_responses = []
        for i, query in enumerate(q["queries"]):
            print(f"  Calling query {i+1}: {query['request_url']}?{query['params']}", file=sys.stderr)
            try:
                resp = call_gateway(query["request_url"], query["params"])
                sdk_responses.append(resp)
                print(f"  ✓ Success", file=sys.stderr)
            except Exception as e:
                print(f"  ✗ Error: {e}", file=sys.stderr)
                sdk_responses.append({"error": str(e)})

        # Compute answer
        try:
            solver = SOLVERS.get(qid)
            if solver:
                answer = solver(sdk_responses)
            else:
                answer = "[No solver for this question]"
            print(f"  ✓ Answer computed", file=sys.stderr)
        except Exception as e:
            answer = f"[Calculation error: {e}]"
            print(f"  ✗ Calculation error: {e}", file=sys.stderr)

        results.append({
            "id": qid,
            "type": q["type"],
            "difficulty": q["difficulty"],
            "financial_concept": q["financial_concept"],
            "question": q["question"],
            "solution_steps": q["solution_steps"],
            "queries": q["queries"],
            "sdk_responses": sdk_responses,
            "answer": answer
        })

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
