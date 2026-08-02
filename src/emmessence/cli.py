from .utils_logging import setup_logging


def main() -> None:
    logger = setup_logging()
    try:
        from emmessence.energy_market_model import run
    except ImportError:
        logger.exception("Import Error.")
        raise SystemExit(1)
    run()
