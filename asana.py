#!/usr/bin/env python
# coding: utf-8

"""
Released under MIT License. See LICENSE file.

Asana API gets tasks completion from Asana to action a bell.

By Kamel TIGHIDET <tighidet.kamel@gmail.com>

"""

import base64
import requests
import time
from urllib.parse import quote
import simplejson as json
from asana_token import token



class asanaAPI():

	def __init__(self, token):

