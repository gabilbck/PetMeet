"""Configuracao de logging da aplicacao (RNF15 - observabilidade)."""

import logging
import sys


def configurar_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

    logger_raiz = logging.getLogger("petmeet")
    logger_raiz.setLevel(logging.INFO)
    logger_raiz.addHandler(handler)
    logger_raiz.propagate = False
