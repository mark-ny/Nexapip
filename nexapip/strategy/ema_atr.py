"""EMA Crossover with ATR stop strategy."""

from typing import List, Optional
import logging
import numpy as np

from ..indicators import Indicators
from .base import BaseStrategy, Signal
from datetime import datetime

logger =
