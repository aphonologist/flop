# GEN functions

# X = unlinked segment
# x = unlinked segment + floating H
# H = high tone with one link
# L = leftmost link
# R = rightmost link
# M = middle link

def gen_autoseg_shift(input, flop=False):
	candidates = set()

	# add fully faithful candidate
	candidates.add(input)

	# delete a high tone
	span = False
	a =  0
	for i in range(len(input)):
		if span == True:
			if input[i] == 'R':
				candidate = input[:a] + 'X' * (i-a+1) + input[i+1:]
				candidates.add(candidate)
				span = False
		else:
			if input[i] == 'L':
				a = i
				span = True

		if input[i] in {'H', 'x'}:
			candidate = input[:i] + 'X' + input[i+1:]
			candidates.add(candidate)

	for i in range(len(input)):
		# link a floating tone
		# x -> H ; x -> X and X -> H
		if input[i] == 'x':
			candidate = input[:i] + 'X' + input[i+1:]
			candidates.add(candidate)
			for j in range(len(candidate)):
				if candidate[j] == 'X':
					candidate2 = candidate[:j] + 'H' + candidate[j+1:]
					candidates.add(candidate2)
		# delink and float
		if input[i] == 'H':
			candidate = input[:i] + 'x' + input[i+1:]
			candidates.add(candidate)
		# relink
		if input[i] == 'x':
			candidate = input[:i] + 'H' + input[i+1:]
			candidates.add(candidate)

	for i in range(len(input) - 1):
		# spread to the left
		# XL -> LM ; XH -> LR
		if input[i:i+2] == 'XL':
			candidate = input[:i] + 'LM' + input[i+2:]
			candidates.add(candidate)
		if input[i:i+2] == 'XH':
			candidate = input[:i] + 'LR' + input[i+2:]
			candidates.add(candidate)
		# spread to the right
		# RX -> MR ; HX -> LR
		if input[i:i+2] == 'RX':
			candidate = input[:i] + 'MR' + input[i+2:]
			candidates.add(candidate)
		if input[i:i+2] == 'HX':
			candidate = input[:i] + 'LR' + input[i+2:]
			candidates.add(candidate)
		# delink from the left
		# LM -> XL ; LR -> XH
		# delink from the right
		# MR -> RX ; LR -> HX
		if input[i:i+2] == 'LM':
			candidate = input[:i] + 'XL' + input[i+2:]
			candidates.add(candidate)
		if input[i:i+2] == 'MR':
			candidate = input[:i] + 'RX' + input[i+2:]
			candidates.add(candidate)
		if input[i:i+2] == 'LR':
			candidate = input[:i] + 'XH' + input[i+2:]
			candidates.add(candidate)
			candidate = input[:i] + 'HX' + input[i+2:]
			candidates.add(candidate)

	if flop:
		for i in range(len(input) - 1):
			if input[i:i+2] == 'XH':
				candidate = input[:i] + 'HX' + input[i+2:]
				candidates.add(candidate)
			if input[i:i+2] == 'HX':
				candidate = input[:i] + 'XH' + input[i+2:]
				candidates.add(candidate)

	return sorted(list(candidates))
