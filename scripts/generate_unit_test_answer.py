#!/usr/bin/env python3
"""
Generate Unit Test answers by calling SDK gateway and using LLM to generate natural language answers.

Flow:
1. User provides SDK doc
2. Generate question + query parameters  
3. Call gateway with parameters (request_url provided by user)
4. Get SDK raw response
5. Question + response → LLM → natural language answer

Output:
{
  "question": "...",
  "query_params": {...},
  "sdk_raw_response": {
    "request_url": "...",      // Full URL with query params
    "status_code": 200,        // HTTP status code
    "response_headers": {...}, // HTTP response headers
    "body": {...}              // Actual SDK response data
  },
  "answer": "..."
}
"""

import requests
import json
import sys
import os
from typing import Dict, Any, Optional

def call_gateway(request_url: str, api_key: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call SDK gateway with query parameters.
    
    Args:
        request_url: Full gateway URL (e.g., "https://data-gateway.prd.space.id/api/v1/etf/country-weightings")
        api_key: API key for authentication
        query_params: Query parameters to send
    
    Returns:
        SDK raw response with full HTTP details
    """
    headers = {
        "accept": "application/json",
        "X-API-Key": api_key
    }
    
    response = requests.get(request_url, headers=headers, params=query_params)
    response.raise_for_status()
    
    # Return raw response with full HTTP details
    return {
        "request_url": response.url,  # Full URL with query params
        "status_code": response.status_code,
        "response_headers": dict(response.headers),
        "body": response.json()
    }


def generate_answer_with_llm(question: str, sdk_response: Dict[str, Any], openai_api_key: str) -> str:
    """
    Generate natural language answer using GPT-5.2.
    
    Args:
        question: The natural language question
        sdk_response: Raw SDK response (contains body with actual data)
        openai_api_key: OpenAI API key
    
    Returns:
        Natural language answer
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    
    # Use the body for LLM context (the actual response data)
    response_body = sdk_response.get("body", sdk_response)
    
    prompt = f"""You are answering a financial data question based on SDK response data.

Question: {question}

SDK Response:
{json.dumps(response_body, indent=2)}

Provide a clear, concise natural language answer to the question based on the SDK response data. Include specific numbers and details from the response."""
    
    payload = {
        "model": "gpt-5.2",
        "messages": [
            {"role": "system", "content": "You are a financial data expert who provides clear, accurate answers based on API response data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,  # Low temperature for factual answers
        "max_completion_tokens": 500  # GPT-5.2 uses max_completion_tokens instead of max_tokens
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    answer = result["choices"][0]["message"]["content"].strip()
    
    return answer


def generate_unit_test(
    question: str,
    query_params: Dict[str, Any],
    request_url: str,
    api_key: str,
    openai_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate complete Unit Test with question, params, SDK response, and answer.
    
    Args:
        question: Natural language question
        query_params: Query parameters for SDK
        request_url: SDK gateway endpoint URL
        api_key: API key for gateway
        openai_api_key: OpenAI API key for answer generation (optional)
    
    Returns:
        Complete unit test dictionary
    """
    # Step 1: Call gateway
    sdk_response = call_gateway(request_url, api_key, query_params)
    
    # Step 2: Generate answer with GPT-5.2 or leave empty
    if openai_api_key:
        answer = generate_answer_with_llm(question, sdk_response, openai_api_key)
    else:
        answer = ""
    
    # Step 3: Return complete unit test
    return {
        "question": question,
        "query_params": query_params,
        "sdk_raw_response": sdk_response,  # Contains: request_url, status_code, response_headers, body
        "answer": answer
    }


def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_unit_test_answer.py <question> <request_url> <param_key=value> ...")
        print("\nEnvironment Variables Required:")
        print("  OPENAI_API_KEY: OpenAI API key for GPT-5.2")
        print("  SID_API_KEY: (optional) SID Gateway API key")
        print("\nExample:")
        print('  export OPENAI_API_KEY="sk-..."')
        print('  python generate_unit_test_answer.py \\')
        print('    "What is QQQ\'s largest country weighting?" \\')
        print('    "https://data-gateway.prd.space.id/api/v1/etf/country-weightings" \\')
        print('    symbol=QQQ')
        sys.exit(1)
    
    question = sys.argv[1]
    request_url = sys.argv[2]
    
    # Parse query params from command line
    query_params = {}
    for arg in sys.argv[3:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            query_params[key] = value
    
    # Get API keys from environment
    sid_api_key = os.environ.get("SID_API_KEY", "2f21e762-fa1c-4eb8-a8ce-ec8c1e138812")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Note: OPENAI_API_KEY not set, answer will be empty.", file=sys.stderr)
        print("You can generate the answer using an LLM with the question + sdk_response.", file=sys.stderr)
    
    try:
        result = generate_unit_test(question, query_params, request_url, sid_api_key, openai_api_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
