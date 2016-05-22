#!/usr/bin/env python
# coding: utf-8

"""
Released under MIT License. See LICENSE file.

Asana API gets tasks completion from Asana to action a bell.

By Kamel TIGHIDET <tighidet.kamel@gmail.com>

TODO : Factoring GET requests

"""

import base64
import requests
import time
from urllib import quote
import json
import asana_params
import datetime
import eqsbell as bell




class asanaAPI():

	def __init__(self):
		self.asana_api_url = "https://app.asana.com/api/1.0"
		self.token = asana_params.token
		self.wrkspace_name = asana_params.workspace_name
		self.project_subname = asana_params.project_subname
		self.auth_key = base64.b64encode(self.token + ":")
		self.nb_uncompleted_tasks = -1
		self.uncompleted_tasks = {}



	# @classmethod
	def asana(self):
		workspace_id = self.get_workspace_id()
		projects_ids = self.get_projects_id()
		while True:
			if((not workspace_id) or (not projects_ids)):
				# return None
				print 'Error | '+str(workspace_id)+" | "+str(projects_ids)
			else:
				for project_id in projects_ids:
					self.get_validated_tasks(workspace_id, project_id)

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
		return workspace_id

	def get_projects_id(self):
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
		return projects_ids

	def get_validated_tasks(self, workspace_id, project_id):
		validation_time = datetime.datetime.now().isoformat()[:-3]+'Z'
		tasks_target = 'tasks?opt_fields=completed&workspace=%d&project=%d&completed_since=%s&include_archived=%s' % (workspace_id, project_id, validation_time, 'true')
		tasks_req = requests.get("/".join([self.asana_api_url, quote(tasks_target, safe="/&=?")]), auth=(self.token, ""))		
		found_tasks = False
		tasks_ids = []
		# We init the tasks dict
		if len(self.uncompleted_tasks) == 0:
			for task in json.loads(tasks_req.text)['data']:
				self.uncompleted_tasks[task['id']] = task['completed']
			return
		# Check for completed tasks
		for task_id, m_task_completed in self.uncompleted_tasks.iteritems():
			if m_task_completed:
				continue
			is_completed = not m_task_completed
			for snap_task in json.loads(tasks_req.text)['data']:
				if snap_task['id'] == task_id:
					if snap_task['completed'] == False:
						is_completed = False
			if is_completed:
				print "jingle_bell!!!"
				bell.jingle_bell()
				self.uncompleted_tasks[task_id] = True
				time.sleep(3)
		# We add new tasks to the dict
		for task in json.loads(tasks_req.text)['data']:
			if not task['id'] in self.uncompleted_tasks.keys():
				self.uncompleted_tasks[task['id']] = task['completed']


test_instance = asanaAPI()
test_instance.asana()