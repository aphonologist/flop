# GEN functions

# _ = unlinked segment

# input alphabet
# F = floating feature
# L*MR* = linked segment

# output alphabet
# l = new link left
# r = new link right
# U = removed link left
# D = removed link right

# X = deleted linked
# x = deleted floating

# f = new float from linked
# m = new linked from floating

# u = flopped from
# d = flopped to

### returns a list of (cand, clean cand) tuples, where cand records the changes and clean cand is just the output form

import re

def clean(candidate):
	for i,j in [('l', 'L'), ('r', 'R'), ('U', '_'), ('D', '_'), ('X', '_'), ('x', '_'), ('f', 'F'), ('m', 'M'), ('u', '_'), ('d', 'M')]:
		candidate = candidate.replace(i,j)
	return candidate

def gen_autoseg_shift(input, flop=False):
	candidates = set()

	# add fully faithful candidate
	candidates.add(input)

	# floating feature
	for i in range(len(input)):
		if input[i] == 'F':
			# delete it
			candidate = input[:i] + 'x' + input[i+1:]
			candidates.add(candidate)

			# link it
			temp = input[:i] + '_' + input[i+1:]
			for j in range(len(temp)):
				if temp[j] == '_':
					candidate = temp[:j] + 'm' + temp[j+1:]
					candidates.add(candidate)

	# linked feature
	for i in range(len(input)):
		# link left
		if input[i:i+2] in {'_L', '_M'}:
			candidate = input[:i] + 'l' + input[i+1:]
			candidates.add(candidate)

		# link right
		if input[i:i+2] in {'R_', 'M_'}:
			candidate = input[:i+1] + 'r' + input[i+2:]
			candidates.add(candidate)

		# unlink left
		if input[i:i+2] == '_L':
			candidate = input[:i+1] + 'U' + input[i+2:]
			candidates.add(candidate)

		if input[i:i+2] == 'MR':
			candidate = input[:i] + 'UM' + input[i+2:]
			candidates.add(candidate)

		# unlink right
		if input[i:i+2] == 'R_':
			candidate = input[:i] + 'D' + input[i+1:]
			candidates.add(candidate)

		if input[i:i+2] == 'LM':
			candidate = input[:i] + 'MD' + input[i+2:]
			candidates.add(candidate)

		# unlink head
		if input[i:i+3] == '_M_':
			candidate = input[:i] + '_f_' + input[i+3:]
			candidates.add(candidate)

	if input[:2] == 'M_':
		candidate = 'f_' + input[2:]
		candidates.add(candidate)
	if input[-2:] == '_M':
		candidate = input[:-2] + '_f'
		candidates.add(candidate)

	# delete a linked feature : as a simplification, assuming maximally one span
	span = re.search('([LMR]+)', input)
	if span:
		candidate = input[:span.span()[0]] + span.group(0).replace('L', 'U').replace('M', 'X').replace('R', 'D') + input[span.span()[1]:]
		candidates.add(candidate)

	# single-step shift operation : as a simplification, only flopping singly-linked features
	if flop:
		for i in range(len(input) - 1):
			if input[i:i+2] in {'_M', 'M_'}:
				candidate = input[:i] + input[i:i+2].replace('M', 'u').replace('_', 'd') + input[i+2:]
				candidates.add(candidate)

	return sorted([(candidate, clean(candidate)) for candidate in candidates])
