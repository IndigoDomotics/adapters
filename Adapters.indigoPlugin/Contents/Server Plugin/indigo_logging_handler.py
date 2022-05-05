# noqa pylint: disable=too-many-lines, line-too-long, invalid-name, unused-argument, redefined-builtin, broad-except, fixme
"""
Docstring Placeholder
"""

import logging
import indigo  # noqa


class IndigoLoggingHandler(logging.Handler):
    """
    Docstring Placeholder
    """

    def __init__(self, p):
        logging.Handler.__init__(self)
        self.plugin = p

    def emit(self, record):
        if record.levelno < 20:
            self.plugin.debugLog(record.getMessage())
        elif record.levelno < 40:
            indigo.server.log(record.getMessage())
        else:
            self.plugin.errorLog(record.getMessage())
