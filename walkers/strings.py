#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

class StringsFinder(object):

	def __init__(self, what, return_strings=False):
		self.limitations = ['.field', '.local', '.param', 'const-string', 'sput', 'sget']
		self.patterns = what
		self.ret_strings = return_strings

	def do_find(self, where):
		co = {}
		for class_name in where:
			for mth_dict in where[class_name]['Methods']:
				for inst in mth_dict['Instructions']:
					inst = inst.lower()
					for pattern in self.patterns:
						if re.search(pattern, inst) is not None:
							for lim in self.limitations:
								if lim in inst:
									if self.ret_strings:
										if 'const-string' in inst:
											inst = inst.split(', ')[1]
										else:
											continue
										try:
											lstr = co[class_name]
											lstr.add(inst)
											co[class_name] = lstr
										except KeyError:
											lstr = set()
											lstr.add(inst)
											co[class_name] = lstr
									else:
										method_definition = "%s->%s" % (class_name, mth_dict['Name'])
										if method_definition in co:
											if inst not in co[method_definition]:
												co[method_definition].append( inst )
										else:
											co[method_definition] = [inst]
		return co
