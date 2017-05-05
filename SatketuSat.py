#!/usr/bin/env python

import random
from parserSatketuSat import ParserFile
import sys

class Solver(object):

    def __init__(self, clauses, clauses_by_literal, num_vars):
        self.clauses = clauses
        self.clauses_by_literal = clauses_by_literal
        self.num_vars = num_vars

        self.unsat_clauses = set()
        self.maxflips = num_vars
        self.sol = []

    def solve(self):

        while(1):
            self.sol = self.random_solution() # Random solution like [True,False,True,True]
            for flip in xrange(self.maxflips):
	            self.is_sat()
	            if len(self.unsat_clauses) == 0:	# If all the clauses are satisfied
	            	sol = []
	                lit = 1
	                print "s SATISFIABLE"
	                print "v ",
	                for inter in self.sol:
	                    if inter == True:
	                        sol.append(lit)
	                    else:
	                        sol.append(-lit)
	                    lit = lit +1
                    
                        for lit in sol:
                                print str(lit),
                        print "0",
	                return sol

	            else:
	                self.flip_lit()

    def get_random_clause(self):
    	return random.sample(self.unsat_clauses, 1)[0]

    def is_sat_lit(self, lit):

    	if lit > 0 and self.sol[abs(lit)-1] == True or lit < 0 and self.sol[abs(lit)-1] == False:
            return True
        return False

    def get_broken_clause(self,clause):
    	for lit in clause:
    		if self.is_sat_lit(lit):
    			return True
    	return False

    def get_broken(self, clauses):
    	count = 0
    	for clause in clauses:
    		if not self.get_broken_clause(clause):
    			count += 1 
    	return count

    def best_variable_change(self):
    	best_lit = None
    	b = len(self.clauses) + 1
    	for literal in self.get_random_clause():
    		if literal in self.clauses_by_literal:
    			lit_clauses = self.clauses_by_literal[literal]
    		elif -literal in self.clauses_by_literal:
    			lit_clauses = self.clauses_by_literal[-literal]
    		broken_clauses = self.get_broken(lit_clauses)
    		self.sol[abs(literal) -1] = not self.sol[abs(literal) -1]
    		broken_clauses_changed = self.get_broken(lit_clauses)
    		self.sol[abs(literal) -1] = not self.sol[abs(literal) -1]
    		broke = broken_clauses_changed - broken_clauses
    		if b > broke:
    			b = broke
    			best_lit = literal
    	return b, best_lit

    def flip_lit(self):
    	b, best_lit =self.best_variable_change()
    	if b <= 0 and random.random() < 0.8	:
    		self.sol[abs(best_lit) -1] = not self.sol[abs(best_lit) -1]
    	else:
    		rnd = random.randint(1, self.num_vars)
    		self.sol[rnd-1] = not self.sol[rnd-1]

    def is_sat(self):  # Look if the interpretation is valid
        self.unsat_clauses = set()
        for clause in self.clauses:
            for lit in clause:
                sat = self.is_sat_lit(lit)
                if sat:
                	break
            if not sat:
            	self.unsat_clauses.add(tuple(clause)) # Unsat clauses
    
    
    def random_solution(self): # Creates a random interpretation 				
        return [random.random() >= 0.5 for i in xrange(self.num_vars)] # [true,false,true]

if __name__ == "__main__":
    parser = ParserFile()
    c, cByL = parser.read_file(sys.argv[1])
    solution = Solver(c, cByL, parser.numVars).solve()
