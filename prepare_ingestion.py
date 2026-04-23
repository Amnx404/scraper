"""CLI shim — implementation lives in ``live.engines.prepare_ingestion``."""

from live.engines.prepare_ingestion import main

if __name__ == "__main__":
    raise SystemExit(main())
