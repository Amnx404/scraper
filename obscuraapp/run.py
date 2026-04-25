"""Start the Obscura scraping API server.

    python -m obscuraapp            # default: host=0.0.0.0 port=8000
    python -m obscuraapp --port 8080
    OBSCURA_ENDPOINT=http://my-host:9222 python -m obscuraapp
"""

from __future__ import annotations

import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Obscura scraping API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="Hot-reload (dev mode)")
    args = parser.parse_args()

    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Run: pip install uvicorn")
        sys.exit(1)

    uvicorn.run(
        "obscuraapp.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
