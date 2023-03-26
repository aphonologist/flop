## Constraints

# Align-R
# penalizes syllables that intervene between high tone and right edge of word
class AlignR:
	def __init__(self):
		self.name = 'Align-R'

	def vios(self, input, candidate):
		loci = [0]
		for i in range(len(candidate) - 1):
			if candidate[i] in ['H', 'R']:
				loci[0] += len(candidate) - i - 1
		return loci

# NonFinality
# penalizes high tones associated to the final syllable
class NonFinality:
	def __init__(self):
		self.name = 'NonFinality'

	def vios(self, input, candidate):
		if candidate[-1] in ['H', 'R']:
			return [1]
		return [0]

# *Link(H)
# penalizes TBUs associated to a high tone
class LinkH:
	def __init__(self):
		self.name = '*Link(H)'

	def vios(self, input, candidate):
		loci = [0]
		for i in range(len(candidate)):
			if candidate[i] in ['H', 'L', 'R', 'M']:
				loci[0] += 1
		return loci

# *Float
# penalizes high tone not associated to any segment
class Float:
	def __init__(self):
		self.name = '*Float'

	def vios(self, input, candidate):
		loci = [0]
		for i in range(len(candidate)):
			if candidate[i] == 'x':
				loci[0] += 1
		return loci

# Max(link)
# penalizes removal of a high tone link
class Maxlink:
	def __init__(self):
		self.name = 'Max(link)'

	def vios(self, input, candidate):
		for i in range(len(candidate) - 1):
			if (input[i:i+2], candidate[i:i+2]) in [('LM', 'XL'), ('LR', 'XH'), ('MR', 'RX'), ('LR', 'HX'), ('XH', 'HX'), ('HX', 'XH')]:
				return [1]
			if (input[i], candidate[i]) in [('H', 'x'), ('H', 'X')]:
				return [1]
		if (input[-1], candidate[-1]) in [('H', 'x'), ('H', 'X')]:
			return [1]
		return [0]

# Dep(link)
# penalizes creation of a high tone link
class Deplink:
	def __init__(self):
		self.name = 'Dep(link)'

	def vios(self, input, candidate):
		for i in range(len(candidate) - 1):
			if (input[i:i+2], candidate[i:i+2]) in [('XL', 'LM'), ('XH', 'LR'), ('RX', 'MR'), ('HX', 'LR'), ('XH', 'HX'), ('HX', 'XH')]:
				return [1]
			if (input[i], candidate[i]) == ('x','H'):
				return [1]
		if (input[-1], candidate[-1]) == ('x','H'):
			return [1]
		return [0]

# Max
# penalizes deletion of a floating high tone
class Max:
	def __init__(self):
		self.name = 'Max'

	def vios(self, input, candidate):
		delink = False
		relink = False
		for i in range(len(candidate)):
			if (input[i], candidate[i]) == ('x', 'X'):
				delink = True
			if (input[i], candidate[i]) == ('X', 'H'):
				relink = True
			if input[i] in {'L', 'M', 'R', 'H'} and candidate[i] == 'X':
				return [1]
		if delink and not relink:
			return [1]
		return [0]
