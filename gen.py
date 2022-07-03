# GEN functions

# X = unlinked segment
# x = unlinked segment + floating H
# H = high tone with one link
# L = leftmost link
# R = rightmost link
# M = middle link
# S = shifted high tone

def gen_autoseg_shift(input, shift=False):
	candidates = set()

	# add fully faithful candidate
	candidates.add(input)

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
		# delink and float
		# XH -> Xx ; HX -> xX
		if input[i:i+2] == 'XH':
			candidate = input[:i] + 'Xx' + input[i+2:]
			candidates.add(candidate)
		if input[i:i+2] == 'HX':
			candidate = input[:i] + 'xX' + input[i+2:]
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

	for i in range(len(input)):
		# delete a floating tone
		# x -> X
		# link a floating tone
		# x -> H ; x -> X and X -> H
		if input[i] == 'x':
			candidate = input[:i] + 'X' + input[i+1:]
			candidates.add(candidate)
			for j in range(len(input)):
				if input[j] == 'X':
					candidate2 = candidate[:j] + 'X' + candidate[j+1:]
					candidates.add(candidate2)
		# delink
		if input[i] == 'H':
			candidate = input[:i] + 'x' + input[i+1:]
			candidates.add(candidate)
		# relink
		if input[i] == 'x':
			candidate = input[:i] + 'H' + input[i+1:]
			candidates.add(candidate)

	if shift:
		for i in range(len(input) - 1):
			# local shift
			# XH -> SX ; HX -> XS
			if input[i:i+2] == 'XH':
				candidate = input[:i] + 'SX' + input[i+2:]
				candidates.add(candidate)
			if input[i:i+2] == 'HX':
				candidate = input[:i] + 'XS' + input[i+2:]
				candidates.add(candidate)

	return sorted(list(candidates))
