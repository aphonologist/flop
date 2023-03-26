#import sys
from con import *
#from tablO import tablO
from fred import FRed

# command line parameter to control printing
#verbose = '-v' in sys.argv

# function to determine whether v1 <= v2 by checking first position where they differ
def leq(v1, v2):
	for i in range(len(v1)):
		if v1[i] < v2[i]:
			return True
		if v1[i] > v2[i]:
			return False
	return True

# underlying forms
urs = ['X' * i for i in range(1,6)]
for i in range(5):
	ur = urs[i]
	for j in range(len(ur)):
		ur2 = ur[:j] + 'H' + ur[j+1:]
		urs.append(ur2)

from gen import gen_autoseg_shift as gen

con = [AlignR(), NonFinality(), LinkH(), Float(), Maxlink(), Deplink(), Max()]

typology = []

# (SKB, derivation)
for ur in urs:
	derivations = []

	stack = []
	stack.append((set(), (ur,)))

	while stack:
		derivation = stack.pop()

		# check for convergence
		if len(derivation[1]) > 1 and derivation[1][-2] == derivation[1][-1]:
			derivations.append(derivation)
			continue

		# Generate candidate set
		input = derivation[1][-1]
		# bool controls whether flop is an operation
		candidates = sorted(list(gen(input, False)))

		# Assemble tableau
		tableau = []
		for constraint in con:
			tableau.append([constraint.vios(input,candidate) for candidate in candidates])

		# Find minimal violation for all constraints
		viominima = [tableau[c][0][:] for c in range(len(con))]

		for c in range(1, len(candidates)):
			for v in range(len(con)):
				if not leq(viominima[v], tableau[v][c]):
						viominima[v] = tableau[v][c][:]

		# Iterate through candidates
		for optimum in range(len(candidates)):

			# Generate comparative tableau
			unsat = False
			comptableau = []
			for c in range(len(candidates)):
				row = [''] * len(con)
				for v in range(len(con)):
					if leq(tableau[v][optimum], tableau[v][c]) and leq(tableau[v][c], tableau[v][optimum]):
						row[v] = 'e'
					elif leq(tableau[v][c], tableau[v][optimum]):
						row[v] = 'L'
					else:
						row[v] = 'W'
				comptableau.append(row)
				if 'W' not in row and 'L' in row:
					unsat = True
					break
			if unsat: continue

			#tablO(tableau, input, candidates, con, optimum, comptableau)

			# Run FRed on optimum
			SKB = FRed(comptableau[:optimum] + comptableau[optimum + 1:])

			if 'unsat' not in SKB:
				# combine ranking arguments
				combinedSKB = derivation[0].union(SKB)

				# check for inconsistency
				newSKB = FRed(combinedSKB)
				if 'unsat' not in newSKB:
					newderivation = (newSKB, derivation[1] + (candidates[optimum],))
					stack.append(newderivation)

	# combine derivations with previous derivations
	# (SKB, derivation, derivation, ...)
	if typology:
		new_languages = []
		while derivations:
			derivation = derivations.pop()
			for language in typology:
				combinedSKB = derivation[0].union(language[0])
				newSKB = FRed(combinedSKB)
				if 'unsat' not in newSKB:
					new_language = (newSKB,) + language[1:] + (derivation[1],)
					new_languages.append(new_language)
		typology = []
		while new_languages:
			typology.append(new_languages.pop())

	else:
		while derivations:
			typology.append(derivations.pop())

# represent by surface form
surface_gram = {}

for language in sorted(typology):
	# get surface forms
	sr_list = [x[-1] for x in language[1:]]
	sr_str = '_' + ' '.join(sr_list) + '\n'
	if sr_str not in surface_gram:
		surface_gram[sr_str] = []

	# get derivation string
	deriv_str = ''
	for derivation in language[1:]:
		deriv_str += '\t/' + derivation[0] + '/\t[' + derivation[-1] + ']\n'
		deriv_str += '\t' + ' -> '.join(derivation) + '\n'

	# get constraint string
	constraint_names = [c.name for c in con]
	con_str = '\t' + '\t'.join(constraint_names) + '\n'
	for erc in sorted(language[0]):
		con_str += '\t'
		i = 0
		while i < len(erc):
			con_str += erc[i] + '\t'
			i += 1
		con_str += '\n'

	# add to dictionary
	surface_gram[sr_str].append([sr_str, deriv_str, con_str])

for s in surface_gram:
	for g in sorted(surface_gram[s]):
		for x in g:
			print(x)
	print()
