#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

class Walker:
	def __init__(self, location):
		self.location     	= location
		self.AppInventory 	= {}
		self.ParsedResults	= None
		self.Finder         = None
		self.do_walk()

	def get_classes(self):
		k = self.AppInventory.keys()
		print("{}".format(k))

	def assign_finder(self, finder):
		self.Finder = finder

	def do_find(self):
		return self.Finder.do_find(self.AppInventory)

	def do_walk(self):
		self.AppInventory = {}
		self.AppInventory['packages'] = set()
		for root, subFolders, files in os.walk(self.location):
			for file in files:
				if file.endswith(".smali"):
					self.AppInventory['packages'].add(root.replace(self.location+"\\", '').replace('/', '.'))
					with open(root+"/"+file, "r") as file_handle:
						content = file_handle.read()
						class_name = re.search('^\\.class\\s+(.*?)' + "\n" +'\\.super\\s+(.*?)' + "\n" + '\\.source\\s+(.*?)' + "\n", content).groups()[0].split(' ')[-1]
						self.AppInventory[class_name] = {}
						self.AppInventory[class_name]['Properties'] = re.findall('[.]field\\s+(.*?)' + "\n", content, re.DOTALL)
						self.AppInventory[class_name]['Methods'] = []
						for m in re.findall('[.]method\\s(.*?)' + "\n" +'(.*?)[.]end\\s+method', content, re.DOTALL):
							ind_meth = {}
							ind_meth['Name'] = m[0].split(' ')[-1]
							ind_meth['Instructions'] = []
							for i in m[1].split("\n"):
								if len(i)>0:
									ind_meth['Instructions'].append(i.lstrip().rstrip())
							self.AppInventory[class_name]['Methods'].append(ind_meth)
