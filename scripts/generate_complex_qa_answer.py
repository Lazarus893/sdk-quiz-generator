#!/usr/bin/env python3
"""
Generate Complex QA answers by calling SDK gateway multiple times and using LLM to generate
natural language answers that require multi-step calculations.

Key differences from Unit Test:
- Multiple API calls per question (multi-hop queries)
- Solution steps describing what to extract and how to calculate
- Answer requires computation, not direct lookup

Flow:
1. User provides SDK doc(s)
2. Generate question + multiple query parameter sets + solution steps
3. Call gateway for EACH query parameter set
4. Get multiple SDK raw responses
5. Question + all responses + solution steps → LLM → calculated answer

Input (JSON file or stdin):
{
  "question": "...",
  "solution_steps": [
    "Step 1: From query 1, extract ...",
    "Step 2: From query 2, extract ...",
    "Step 3: Calculate ... using formula ..."
  ],
  "queries": [
    {
      "request_url": "https://...",
      "params": {"symbol": "AAPL", ...}
    },
    {
      "request_url": "https://...",
      "params": {"symbol": "AAPL", ...}
    }
  ]
}

Output:
{
  "question": "...",
  "solution_steps": [...],
  "queries": [...],
  "sdk_responses": [{...}, {...}],
  "answer": "..."
}
"""

import requests
import json
import sys
import os
from typing import Dict, Any, List


def call_gateway(request_url: str, api_key: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call SDK gateway with query parameters.

    Args:
        request_url: Full gateway URL
        api_key: API key for authentication
        query_params: Query parameters to send

    Returns:
        SDK raw response
    """
    headers = {
        "accept": "application/json",
        "X-API-Key": api_key
    }

    response = requests.get(request_url, headers=headers, params=query_params)
    response.raise_for_status()

    return response.json()


def call_all_queries(queries: List[Dict[str, Any]], api_key: str) -> List[Dict[str, Any]]:
    """
    Execute all queries sequentially and collect responses.

    Args:
        queries: List of query configs, each with request_url and params
        api_key: API key for authentication

    Returns:
        List of SDK responses in the same order as queries
    """
    responses = []
    for i, query in enumerate(queries):
        request_url = query["request_url"]
        params = query.get("params", {})

        try:
            resp = call_gateway(request_url, api_key, params)
            responses.append(resp)
        except Exception as e:
            responses.append({"error": str(e), "query_index": i})

    return responses


def generate_answer_with_llm(
    question: str,
    solution_steps: List[str],
    queries: List[Dict[str, Any]],
    sdk_responses: List[Dict[str, Any]],
    openai_api_key: str
) -> str:
    """
    Generate natural language answer using GPT-5.2 based on multiple SDK responses
    and solution steps.

    Args:
        question: The natural language question
        solution_steps: Step-by-step approach to solve the question
        queries: The query configurations used
        sdk_responses: Raw SDK responses (one per query)
        openai_api_key: OpenAI API key

    Returns:
        Natural language answer with calculations
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    # Build context with all queries and responses paired together
    data_context = ""
    for i, (query, resp) in enumerate(zip(queries, sdk_responses)):
        data_context += f"\n--- Query {i + 1} ---\n"
        data_context += f"Endpoint: {query['request_url']}\n"
        data_context += f"Parameters: {json.dumps(query.get('params', {}))}\n"
        data_context += f"Response:\n{json.dumps(resp, indent=2)}\n"

    solution_text = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(solution_steps))

    prompt = f"""You are answering a financial data question that requires multi-step calculation based on multiple SDK responses.

Question: {question}

Suggested Solution Steps:
{solution_text}

SDK Data:
{data_context}

Instructions:
- Follow the solution steps to extract the required data points from each SDK response.
- Perform the calculations described in the solution steps.
- Show your work: state the values extracted and the formula used.
- Provide a clear, concise final answer with specific numbers.
- If any data is missing or an error occurred, explain what went wrong."""

    payload = {
        "model": "gpt-5.2",
        "messages": [
            {
                "role": "system",
                "content": "You are a financial data expert who provides clear, accurate answers based on API response data. You always show your calculation steps and use precise numbers from the data."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_completion_tokens": 800
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    answer = result["choices"][0]["message"]["content"].strip()

    return answer


def generate_complex_qa(
    question: str,
    solution_steps: List[str],
    queries: List[Dict[str, Any]],
    api_key: str,
    openai_api_key: str
) -> Dict[str, Any]:
    """
    Generate complete Complex QA with question, solution steps, multiple SDK responses, and answer.

    Args:
        question: Natural language question requiring calculation
        solution_steps: Step-by-step approach to solve
        queries: List of query configs (each with request_url and params)
        api_key: API key for SDK gateway
        openai_api_key: OpenAI API key for answer generation

    Returns:
        Complete Complex QA dictionary
    """
    # Step 1: Call all queries
    sdk_responses = call_all_queries(queries, api_key)

    # Step 2: Generate answer with GPT-5.2
    answer = generate_answer_with_llm(question, solution_steps, queries, sdk_responses, openai_api_key)

    # Step 3: Return complete result
    return {
        "question": question,
        "solution_steps": solution_steps,
        "queries": queries,
        "sdk_responses": sdk_responses,
        "answer": answer
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_complex_qa_answer.py <input.json>")
        print("       echo '{...}' | python generate_complex_qa_answer.py -")
        print()
        print("Input JSON format:")
        print(json.dumps({
            "question": "What was AAPL's EPS growth rate from Q1 to Q2 2024?",
            "solution_steps": [
                "From query 1, extract the mean EPS for Q1 2024",
                "From query 2, extract the mean EPS for Q2 2024",
                "Calculate growth rate: (Q2_EPS - Q1_EPS) / Q1_EPS × 100%"
            ],
            "queries": [
                {
                    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
                    "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 1}
                },
                {
                    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
                    "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 2}
                }
            ]
        }, indent=2))
        print()
        print("Environment Variables Required:")
        print("  OPENAI_API_KEY: OpenAI API key for GPT-5.2")
        print("  SID_API_KEY: (optional) SID Gateway API key")
        sys.exit(1)

    # Read input JSON
    if sys.argv[1] == "-":
        input_data = json.load(sys.stdin)
    else:
        with open(sys.argv[1], "r") as f:
            input_data = json.load(f)

    # Validate required fields
    required_fields = ["question", "solution_steps", "queries"]
    for field in required_fields:
        if field not in input_data:
            print(f"Error: Missing required field '{field}' in input JSON", file=sys.stderr)
            sys.exit(1)

    if not isinstance(input_data["queries"], list) or len(input_data["queries"]) < 1:
        print("Error: 'queries' must be a non-empty array", file=sys.stderr)
        sys.exit(1)

    for i, query in enumerate(input_data["queries"]):
        if "request_url" not in query:
            print(f"Error: Query {i} missing 'request_url'", file=sys.stderr)
            sys.exit(1)

    # Get API keys from environment
    sid_api_key = os.environ.get("SID_API_KEY", "2f21e762-fa1c-4eb8-a8ce-ec8c1e138812")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable is required", file=sys.stderr)
        print("Set it with: export OPENAI_API_KEY='sk-...'", file=sys.stderr)
        sys.exit(1)

    try:
        result = generate_complex_qa(
            question=input_data["question"],
            solution_steps=input_data["solution_steps"],
            queries=input_data["queries"],
            api_key=sid_api_key,
            openai_api_key=openai_api_key
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
