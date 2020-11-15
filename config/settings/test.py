# -*- coding: utf-8 -*-
import iptools

from .base import *  # noqa: F401

DEBUG = False
INTERNAL_IPS = iptools.IpRangeList(
    '10/8',
    '127/8',
    '172.16/12',
    '192.168/16'
)
