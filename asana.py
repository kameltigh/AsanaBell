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
from urllib import quote
import json
# from asana_params import token
import asana_params




class asanaAPI():

	def __init__(self):
		self.asana_api_url = "https://app.asana.com/api/1.0"
		self.token = asana_params.token
		self.wrkspace_name = asana_params.workspace_name
		self.project_subname = asana_params.project_subname
		self.auth_key = base64.b64encode(self.token + ":")


	# @classmethod
	def asana(self):
		workspace_id = self.get_workspace_id()
		if(not workspace_id):
			return None
		# while True:

	def get_workspace_id(self):
		workspaces_target = 'workspaces'
		workspaces_req = requests.get("/".join([self.asana_api_url, quote(workspaces_target, safe="/&=?")]), auth=(self.token, ""))		
		found_ws = False
		for ws in json.loads(workspaces_req.text)['data']:
			if(ws['name'] == self.wrkspace_name):
				 workspace_id = ws['id']
				 found_ws = True
				 print 'Found workspace | id = ' + str(workspace_id)

		if(not found_ws):
			print 'workspace not found'
			return None

	def get_project_id(self):
		projects_target = 'projects'
		projects_req = requests.get("/".join([self.asana_api_url, quote(projects_target, safe="/&=?")]), auth=(self.token, ""))		
		found_project = False
		projects_ids = []
		for project in json.loads(projects_req.text)['data']:
			if self.project_subname in project['name']:
				print 'Found project | id = '+str(project['id'])
				projects_ids.append(project['id'])
				found_project = True
		if(not found_project):
			print 'No project contains the specified subname'
			return None


toto = asanaAPI()
toto.asana()
toto.get_project_id()