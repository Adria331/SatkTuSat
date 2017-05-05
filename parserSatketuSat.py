#!/usr/bin/env python

import sys 
import re

class ParserFile():

	def __init__(self):
		self.clauses = set()
		self.clauses_by_literal = {}
		self.numVars = None
		self.numClauses = None

	def read_file(self, file_path, data_sep = "\t| "):
		with open(str(file_path), "r") as f:
			return self.read_stream(f,data_sep)

	def read_stream(self, stream, data_sep = "\t| "):
		reader = (l for l in (ll.strip  for ll in stream) if l)	
		self.clauses = set()
		for line in stream:
			temp_list = []
			if "p" in line:
				l = line.split()
				self.numVars = int(l[2])
				self.numClauses = int(l[3])
			elif "%" not in line and "c" not in line:
				for val in re.split(data_sep, line):
					if val != "\n" and "#" not in val and val != "" \
						and "0\n" != val:
						temp_list.append(self.filter_token(val.strip()))
						
			if temp_list:
				self.clauses.add(tuple(temp_list))

		for clause in self.clauses:
			for literal in clause:
				if literal not in self.clauses_by_literal and -literal not in self.clauses_by_literal:
					self.clauses_by_literal[literal] = set()
				if literal in self.clauses_by_literal:
					self.clauses_by_literal[literal].add(tuple(clause))
				if -literal in self.clauses_by_literal:
					self.clauses_by_literal[-literal].add(tuple(clause))

		return self.clauses, self.clauses_by_literal


	def filter_token(self, token):
		try:
			return int(token)
		except ValueError:
			try:
				return float(token)
			except ValueError:
				pass
		return token
		
if __name__ == "__main__":
        
	if len(sys.argv) != 2:
		sys.exit("Use: %s <cnf-formula>" % sys.argv[0])

	parser = ParserFile();
	print "\n" + str(parser.read_file(sys.argv[1])) + "\n"
