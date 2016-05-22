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
# import eqsbell as bell

# TODO init workspaces befor starting


class asanaAPI():

	def __init__(self):
		self.asana_api_url = "https://app.asana.com/api/1.0"
		self.token = asana_params.token
		self.wrkspace_name = asana_params.workspace_name
		self.project_subname = asana_params.project_subname
		self.auth_key = base64.b64encode(self.token + ":")
		self.nb_init_projects = 0
		self.nb_projects = 0
		self.uncompleted_tasks = {}
		self.completed_eventually = {}



	# @classmethod
	def asana(self):
		workspace_id = self.get_workspace_id()
		projects_ids = self.get_projects_id()
		self.nb_init_projects = len(projects_ids)
		self.nb_projects = len(projects_ids)
		while True:
			if((not workspace_id) or (not projects_ids)):
				# return None
				print 'Error | '+str(workspace_id)+" | "+str(projects_ids)
			else:
				for project_id in projects_ids:
					self.run(workspace_id, project_id)

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

	def run(self, workspace_id, project_id):
		validation_time = datetime.datetime.now().isoformat()[:-3]+'Z'
		tasks_target = 'tasks?opt_fields=completed,name&opt_pretty&limit=100&workspace=%d&project=%d&completed_since=%s&include_archived=%s' % (workspace_id, project_id, validation_time, 'true')
		tasks_req = requests.get("/".join([self.asana_api_url, quote(tasks_target, safe="/&=?")]), auth=(self.token, ""))		
		found_tasks = False
		tasks_ids = []
		# We init the tasks dict
		if self.nb_init_projects > 0:
			self.nb_init_projects -= 1
			for task in json.loads(tasks_req.text)['data']:
				self.uncompleted_tasks[task['id']] = task['completed']
			return
		# Check for completed tasks
		print json.loads(tasks_req.text)['data']
		for task_id, m_task_completed in self.uncompleted_tasks.iteritems():
			print self.completed_eventually
			if m_task_completed:
				continue
			is_newly_completed = True
			found_task = False
			for snap_task in json.loads(tasks_req.text)['data']:
				if snap_task['id'] == task_id:
					found_task = True
					if snap_task['completed'] == False:
						is_newly_completed = False			
			# if not found_task:
			# 	print "found_task = "+str(found_task)+" is_newly_completed = "+str(is_newly_completed)
			if not found_task and is_newly_completed:
				if task_id in self.completed_eventually:
					if self.completed_eventually[task_id] == 0:
						print "Validated task : "+str(task_id)
						del self.completed_eventually[task_id]
						self.uncompleted_tasks[task_id] = True
						# bell.jingle_bell()
						time.sleep(3)
					elif self.completed_eventually[task_id] > 0:
						self.completed_eventually[task_id] -= 1
						# print "Not found in a project"
				else:
					self.completed_eventually[task_id] = self.nb_projects
			else:
				if task_id in self.completed_eventually:
					del self.completed_eventually[task_id]
		# We add new tasks to the dict
		for task in json.loads(tasks_req.text)['data']:
			if not task['id'] in self.uncompleted_tasks.keys():
				self.uncompleted_tasks[task['id']] = task['completed']
				print "Added task: "+str(task['id'])
		print 'still have %u uncompleted tasks' % len(self.uncompleted_tasks)
		print self.uncompleted_tasks


test_instance = asanaAPI()
test_instance.asana()