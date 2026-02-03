#!/usr/bin/env python3
"""
Generate Complex QA answers: single or batch, LLM or programmatic.

Usage:
  # Single question with LLM
  python3 generate_complex_qa_answer.py input.json

  # Batch with LLM
  python3 generate_complex_qa_answer.py batch.json --batch

  # Batch with programmatic solvers (no LLM needed)
  python3 generate_complex_qa_answer.py batch.json --batch --no-llm
"""

import requests
import json
import sys
import os
import math
from typing import Dict, Any, List, Callable, Optional


API_KEY = os.environ.get("SID_API_KEY", "2f21e762-fa1c-4eb8-a8ce-ec8c1e138812")
HEADERS = {"accept": "application/json", "X-API-Key": API_KEY}


# =============================================================================
# Gateway Client
# =============================================================================

def call_gateway(request_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.get(request_url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def call_all_queries(queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    responses = []
    for i, query in enumerate(queries):
        try:
            resp = call_gateway(query["request_url"], query.get("params", {}))
            responses.append(resp)
        except Exception as e:
            responses.append({"error": str(e), "query_index": i})
    return responses


# =============================================================================
# LLM Answer Generator
# =============================================================================

def generate_answer_llm(
    question: str,
    solution_steps: List[str],
    queries: List[Dict[str, Any]],
    sdk_responses: List[Dict[str, Any]],
) -> str:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY required for LLM mode")

    data_context = ""
    for i, (query, resp) in enumerate(zip(queries, sdk_responses)):
        data_context += f"\n--- Query {i + 1} ---\n"
        data_context += f"Endpoint: {query['request_url']}\n"
        data_context += f"Parameters: {json.dumps(query.get('params', {}))}\n"
        data_context += f"Response:\n{json.dumps(resp, indent=2)}\n"

    solution_text = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(solution_steps))

    prompt = f"""You are answering a financial data question that requires multi-step calculation.

Question: {question}

Solution Steps:
{solution_text}

SDK Data:
{data_context}

Instructions:
- Follow the solution steps to extract data from each SDK response.
- Perform the calculations described.
- Show your work: state values extracted and formula used.
- Provide a clear, concise final answer with specific numbers."""

    payload = {
        "model": "gpt-5.2",
        "messages": [
            {"role": "system", "content": "You are a financial data expert. Show calculation steps and use precise numbers."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_completion_tokens": 800
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"},
        json=payload
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


# =============================================================================
# Programmatic Solvers (by question ID)
# =============================================================================

def solve_q1(responses):
    """Forward P/E Ratio: price_close / epsAvg"""
    fe = responses[0]["data"][0]
    eps_avg = float(fe["epsAvg"])
    kline_data = responses[1]["response"]["data"]
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
    sum_tp_vol = sum((c["price_high"] + c["price_low"] + c["price_close"]) / 3 * c["volume_traded"] for c in candles)
    sum_vol = sum(c["volume_traded"] for c in candles)
    if sum_vol == 0:
        return "No volume data available"
    vwap = sum_tp_vol / sum_vol
    return f"AMD hourly candles: {len(candles)} candles\nTotal volume: {sum_vol:,}\nVWAP = ${vwap:.4f}"


def solve_q3(responses):
    """Operating Margin YoY"""
    fy24, fy25 = responses[0]["data"][0], responses[1]["data"][0]
    margin_24 = float(fy24["ebitAvg"]) / float(fy24["revenueAvg"]) * 100
    margin_25 = float(fy25["ebitAvg"]) / float(fy25["revenueAvg"]) * 100
    change = margin_25 - margin_24
    return f"CRM FY2024 margin = {margin_24:.2f}%\nCRM FY2025 margin = {margin_25:.2f}%\nYoY change: {change:+.2f} pp"


def solve_q4(responses):
    """EPS spread vs price spread"""
    fe = responses[0]["data"][0]
    eps_high, eps_low, eps_avg = float(fe["epsHigh"]), float(fe["epsLow"]), float(fe["epsAvg"])
    eps_spread = (eps_high - eps_low) / eps_avg * 100
    candles = responses[1]["response"]["data"]
    max_high = max(c["price_high"] for c in candles)
    min_low = min(c["price_low"] for c in candles)
    avg_close = sum(c["price_close"] for c in candles) / len(candles)
    price_spread = (max_high - min_low) / avg_close * 100
    more = "EPS analyst disagreement" if eps_spread > price_spread else "price action"
    return f"EPS spread = {eps_spread:.2f}%\nPrice spread = {price_spread:.2f}%\nMore uncertainty: {more}"


def solve_q5(responses):
    """Quarterly EPS growth trajectory"""
    eps = [(r["data"][0]["fiscalQuarter"], float(r["data"][0]["epsAvg"])) for r in responses]
    growths = [(eps[i][1] - eps[i-1][1]) / eps[i-1][1] * 100 for i in range(1, len(eps))]
    if all(growths[i] > growths[i-1] for i in range(1, len(growths))):
        trajectory = "accelerating"
    elif all(growths[i] < growths[i-1] for i in range(1, len(growths))):
        trajectory = "decelerating"
    else:
        trajectory = "uneven"
    lines = [f"{q}: ${e:.5f}" for q, e in eps]
    return f"AAPL EPS: {', '.join(lines)}\nTrajectory: {trajectory}"


def solve_q6(responses):
    """Annualized volatility"""
    candles = sorted(responses[0]["response"]["data"], key=lambda c: c["time_open"])
    closes = [c["price_close"] for c in candles]
    if len(closes) < 2:
        return "Not enough data"
    log_returns = [math.log(closes[i] / closes[i-1]) for i in range(1, len(closes))]
    n = len(log_returns)
    mean_r = sum(log_returns) / n
    variance = sum((r - mean_r) ** 2 for r in log_returns) / (n - 1)
    annualized = math.sqrt(variance) * math.sqrt(252) * 100
    return f"JPM: {len(closes)} days, annualized volatility = {annualized:.2f}%"


def solve_q7(responses):
    """SGA efficiency comparison"""
    amzn, wmt = responses[0]["data"][0], responses[1]["data"][0]
    amzn_ratio = float(amzn["sgaExpenseAvg"]) / float(amzn["revenueAvg"]) * 100
    wmt_ratio = float(wmt["sgaExpenseAvg"]) / float(wmt["revenueAvg"]) * 100
    more_efficient = "WMT" if wmt_ratio < amzn_ratio else "AMZN"
    return f"AMZN SGA ratio = {amzn_ratio:.2f}%\nWMT SGA ratio = {wmt_ratio:.2f}%\n{more_efficient} more efficient"


def solve_q8(responses):
    """Incremental margin"""
    fy24, fy25 = responses[0]["data"][0], responses[1]["data"][0]
    rev_24, ni_24 = float(fy24["revenueAvg"]), float(fy24["netIncomeAvg"])
    rev_25, ni_25 = float(fy25["revenueAvg"]), float(fy25["netIncomeAvg"])
    inc_margin = (ni_25 - ni_24) / (rev_25 - rev_24) * 100 if rev_25 != rev_24 else 0
    overall_24 = ni_24 / rev_24 * 100
    leverage = "positive" if inc_margin > overall_24 else "negative"
    return f"MSFT incremental margin = {inc_margin:.2f}% vs FY24 margin {overall_24:.2f}%\nOperating leverage: {leverage}"


def solve_q9(responses):
    """Weekly ATR%"""
    candles = responses[0]["response"]["data"]
    trs = [c["price_high"] - c["price_low"] for c in candles]
    atr = sum(trs) / len(trs)
    avg_close = sum(c["price_close"] for c in candles) / len(candles)
    atr_pct = atr / avg_close * 100
    return f"TSLA: {len(candles)} weeks, ATR = ${atr:.2f}, ATR% = {atr_pct:.2f}%"


def solve_q10(responses):
    """PEG Ratio"""
    fy24, fy25 = responses[0]["data"][0], responses[1]["data"][0]
    kline = responses[2]["response"]["data"]
    eps_24, eps_25 = float(fy24["epsAvg"]), float(fy25["epsAvg"])
    growth = (eps_25 - eps_24) / eps_24 * 100
    avg_close = sum(c["price_close"] for c in kline) / len(kline)
    forward_pe = avg_close / eps_25
    peg = forward_pe / growth if growth != 0 else float('inf')
    valuation = "undervalued" if peg < 1 else "premium"
    return f"NVDA EPS growth = {growth:.2f}%\nForward P/E = {forward_pe:.2f}x\nPEG = {peg:.2f} ({valuation})"


SOLVERS: Dict[int, Callable] = {
    1: solve_q1, 2: solve_q2, 3: solve_q3, 4: solve_q4, 5: solve_q5,
    6: solve_q6, 7: solve_q7, 8: solve_q8, 9: solve_q9, 10: solve_q10,
}


# =============================================================================
# Main Processing
# =============================================================================

def process_question(q: Dict[str, Any], use_llm: bool = True, skip_llm: bool = False) -> Dict[str, Any]:
    """Process a single question, return result with answer."""
    sdk_responses = call_all_queries(q["queries"])

    if skip_llm:
        # No OPENAI_API_KEY, leave answer empty
        answer = ""
    elif use_llm:
        answer = generate_answer_llm(q["question"], q["solution_steps"], q["queries"], sdk_responses)
    else:
        solver = SOLVERS.get(q.get("id"))
        if solver:
            try:
                answer = solver(sdk_responses)
            except Exception as e:
                answer = f"[Calculation error: {e}]"
        else:
            answer = "[No solver for this question ID]"

    result = {
        "question": q["question"],
        "solution_steps": q["solution_steps"],
        "queries": q["queries"],
        "sdk_responses": sdk_responses,
        "answer": answer
    }
    # Preserve extra fields
    for key in ["id", "type", "difficulty", "financial_concept"]:
        if key in q:
            result[key] = q[key]
    return result


def main():
    args = sys.argv[1:]
    if not args or args[0] in ["-h", "--help"]:
        print("Usage:")
        print("  python3 generate_complex_qa_answer.py input.json           # Single, LLM")
        print("  python3 generate_complex_qa_answer.py batch.json --batch   # Batch, LLM")
        print("  python3 generate_complex_qa_answer.py batch.json --batch --no-llm  # Batch, programmatic")
        print("  cat input.json | python3 generate_complex_qa_answer.py -   # Stdin")
        sys.exit(0)

    batch_mode = "--batch" in args
    use_llm = "--no-llm" not in args
    input_file = [a for a in args if not a.startswith("--")][0]

    # Check OPENAI_API_KEY for LLM mode
    skip_llm = False
    if use_llm and not os.environ.get("OPENAI_API_KEY"):
        print("Note: OPENAI_API_KEY not set, answer will be empty.", file=sys.stderr)
        print("You can generate the answer using an LLM with question + solution_steps + sdk_responses.", file=sys.stderr)
        skip_llm = True

    # Read input
    if input_file == "-":
        data = json.load(sys.stdin)
    else:
        with open(input_file) as f:
            data = json.load(f)

    # Process
    if batch_mode or isinstance(data, list):
        questions = data if isinstance(data, list) else [data]
        results = []
        for i, q in enumerate(questions):
            print(f"Processing {i+1}/{len(questions)}: Q{q.get('id', i+1)}...", file=sys.stderr)
            results.append(process_question(q, use_llm, skip_llm))
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        result = process_question(data, use_llm, skip_llm)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
