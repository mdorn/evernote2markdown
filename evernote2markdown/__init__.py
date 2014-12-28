# -*- coding: utf-8 -*-

__author__ = 'Matt Dorn'
__email__ = 'matt.dorn@gmail.com'
__version__ = '0.1.0'

# Set default logging handler to avoid "No handler found" warnings.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
