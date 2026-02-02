#!/usr/bin/env python3
"""
SID Gateway API Client
Query financial data from data-gateway.prd.space.id
"""

import requests
import json
import sys
from typing import Optional, Dict, Any

class SIDGatewayClient:
    def __init__(self, api_key: str):
        self.base_url = "https://data-gateway.prd.space.id/api/v1"
        self.api_key = api_key
        self.headers = {
            "accept": "application/json",
            "X-API-Key": api_key
        }
    
    def get_etf_country_weightings(self, symbol: str) -> Dict[str, Any]:
        """
        Get country weightings for an ETF
        
        Args:
            symbol: ETF symbol (e.g., "QQQ", "SPY")
        
        Returns:
            API response with country weightings
        """
        url = f"{self.base_url}/etf/country-weightings"
        params = {"symbol": symbol}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def query(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generic query method for any SID Gateway endpoint
        
        Args:
            endpoint: API endpoint path (e.g., "/etf/country-weightings")
            params: Query parameters
        
        Returns:
            API response JSON
        """
        url = f"{self.base_url}{endpoint}"
        
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        
        return response.json()


def main():
    # Default API key
    api_key = "2f21e762-fa1c-4eb8-a8ce-ec8c1e138812"
    
    if len(sys.argv) < 3:
        print("Usage: python sid_gateway_client.py <endpoint> <param_key=param_value> ...")
        print("\nExamples:")
        print("  python sid_gateway_client.py /etf/country-weightings symbol=QQQ")
        print("  python sid_gateway_client.py /etf/country-weightings symbol=SPY")
        sys.exit(1)
    
    endpoint = sys.argv[1]
    
    # Parse params from command line (key=value format)
    params = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            params[key] = value
    
    # Create client and query
    client = SIDGatewayClient(api_key)
    
    try:
        result = client.query(endpoint, params)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
