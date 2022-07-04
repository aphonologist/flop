## Constraints

# Align-R
# penalizes syllables that intervene between high tone and right edge of word
class AlignR:
	def __init__(self):
		self.name = 'Align-R'

	def vios(self, input, candidate):
		loci = [0]
		for i in range(len(candidate)):
			if candidate[i] in ['H', 'R', 'S']:
				loci[0] += len(candidate) - i - 1
		return loci

# NonFinality
# penalizes high tones associated to the final syllable
class NonFinality:
	def __init__(self):
		self.name = 'NonFinality'

	def vios(self, input, candidate):
		if candidate[-1] in ['H', 'R', 'S']:
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
			if candidate[i] in ['H', 'L', 'R', 'M', 'S']:
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
			if candidate[i] in ['x']:
				loci[0] += 1
		return loci

# Max(link)
# penalizes removal of a high tone link
class Maxlink:
	def __init__(self):
		self.name = 'Max(link)'

	def vios(self, input, candidate):
		for i in range(len(candidate) - 1):
			if (input[i:i+2], candidate[i:i+2]) in [('XH', 'Xx'), ('HX', 'xX'), ('LM', 'XL'), ('LR', 'XH'), ('MR', 'RX'), ('LR', 'HX')]:
				return [1]
		return [0]

# Dep(link)
# penalizes creation of a high tone link
class Deplink:
	def __init__(self):
		self.name = 'Dep(link)'

	def vios(self, input, candidate):
		for i in range(len(candidate) - 1):
			if (input[i:i+2], candidate[i:i+2]) in [('XL', 'LM'), ('XH', 'LR'), ('RX', 'MR'), ('HX', 'LR')]:
				return [1]
		for i in range(len(candidate)):
			if (input[i], candidate[i]) == ('x','H'):
				return [1]
		xX = False
		XH = False
		for i in range(len(candidate)):
			if (input[i], candidate[i]) == ('x', 'X'):
				xX = True
			if (input[i], candidate[i]) == ('X', 'H'):
				XH = True
			if xX and XH:
				return [1]
		return [0]

# Max
# penalizes deletion of a floating high tone
class Max:
	def __init__(self):
		self.name = 'Max'

	def vios(self, input, candidate):
		for i in range(len(candidate)):
			if (input[i], candidate[i]) == ('x', 'X'):
				return [1]
		return [0]

# NoFlop
# penalizes shifting a high tone
class NoFlop:
	def __init__(self):
		self.name = 'NoFlop'

	def vios(self, input, candidate):
		for i in range(len(candidate)):
			if candidate[i] == 'S':
				return [1]
		return [0]
