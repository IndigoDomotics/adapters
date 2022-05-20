#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Docstring placeholder
"""
import indigo  # noqa
import logging


class IndigoLoggingHandler(logging.Handler):
    """
    Docstring placeholder
    """

    def __init__(self, p):
        """
        Docstring placeholder
        """
        logging.Handler.__init__(self)
        self.plugin = p

    def emit(self, record):
        """
        Docstring placeholder
        """
        if record.levelno < 20:
            self.plugin.debugLog(record.getMessage())
        elif record.levelno < 40:
            indigo.server.log(record.getMessage())
        else:
            self.plugin.errorLog(record.getMessage())
