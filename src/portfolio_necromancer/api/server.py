#!/usr/bin/env python
"""
Run the Portfolio Necromancer API Server
"""

import argparse
from portfolio_necromancer.api.app import run_server


def main():
    parser = argparse.ArgumentParser(
        description='Portfolio Necromancer API Server'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    args = parser.parse_args()
    
    print(f"🧟 Portfolio Necromancer API Server")
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"Dashboard: http://localhost:{args.port}/")
    print(f"API Docs: http://localhost:{args.port}/api/health")
    print()
    
    run_server(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
