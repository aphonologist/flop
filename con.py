## Constraints

# Align-R
# penalizes segmentes that intervene between linked feature and right edge of word
class AlignR:
	def __init__(self):
		self.name = 'Align-R'

	def vios(self, input, candidate):
		candidate = candidate[1][::-1]
		for i in range(len(candidate)):
			if candidate[i] in {'M', 'R'}:
				return [i]	# for simplicity, assuming only one span
		return [0]

# NonFinality
# penalizes features associated to the final syllable
class NonFinality:
	def __init__(self):
		self.name = 'NonFinality'

	def vios(self, input, candidate):
		candidate = candidate[1]
		if candidate[-1] in {'M', 'R'}:
			return [1]
		return [0]

# *Link
# penalizes linked segments
class Link:
	def __init__(self):
		self.name = '*Link'

	def vios(self, input, candidate):
		candidate = candidate[1]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] in {'L', 'R', 'M'}:
				loci += 1
		return [loci]

# *Float
# penalizes feature not associated to any segment
class Float:
	def __init__(self):
		self.name = '*Float'

	def vios(self, input, candidate):
		candidate = candidate[1]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] == 'F':
				loci += 1
		return [loci]

# Max(link)
# penalizes removal of an autosegmental link
class Maxlink:
	def __init__(self):
		self.name = 'Max(link)'

	def vios(self, input, candidate):
		candidate = candidate[0]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] in {'U', 'D', 'X', 'f', 'u'}:
				loci += 1
		return [loci]

# Dep(link)
# penalizes creation of an autosegmental link
class Deplink:
	def __init__(self):
		self.name = 'Dep(link)'

	def vios(self, input, candidate):
		candidate = candidate[0]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] in {'l', 'r', 'm', 'd'}:
				loci += 1
		return [loci]

# Max
# penalizes deletion of a feature
class Max:
	def __init__(self):
		self.name = 'Max'

	def vios(self, input, candidate):
		candidate = candidate[0]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] in {'X', 'x'}:
				loci += 1
		return [loci]

# MaxLinked
# penalizes deletion of a linked feature
class MaxLinked:
	def __init__(self):
		self.name = 'MaxLinked'

	def vios(self, input, candidate):
		candidate = candidate[0]
		loci = 0
		for i in range(len(candidate)):
			if candidate[i] == 'X':
				loci += 1
		return [loci]
