import logging
import re
import warnings

import pandas as pd
import pyomo.environ as pyo




class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[90m",     # grey
        logging.INFO: "\033[94m",      # blue
        logging.WARNING: "\033[93m",   # yellow
        logging.ERROR: "\033[91m",     # red
        logging.CRITICAL: "\033[95m",  # magenta
    }
    RESET = "\033[0m"
    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

def setup_logging():
    warnings.formatwarning = colored_warning
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter("%(levelname)s: %(message)s"))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    return logger

def colored_warning(message, category, filename, lineno, file=None, line=None):
    return f"\033[93m{category.__name__}: {message}\033[0m\n"

def shorten_path(path):
    parts = re.sub(r'/+', '/', path.replace('\\', '/')).split('/')
    if len(parts) >= 2:
        return f".../{parts[-2]}/{parts[-1]}"
    return path

def pyo_var_to_csv(var, path, value_col="value"):
    cols = [s.name for s in var.index_set().subsets()]
    rows = [
        [*(idx if isinstance(idx, tuple) else (idx,)),
         pyo.value(var[idx])]
        for idx in var
    ]
    df = pd.DataFrame(rows, columns=[*cols, value_col])
    df.to_csv(f"{path}/{var.name}.csv", index=False)
