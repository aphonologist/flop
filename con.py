## Constraints

# Align-R
# penalizes syllables that intervene between high tone and right edge of word
class AlignR:
	def __init__(self):
		self.name = 'Align-R'

	def vios(self, input, candidate):
		loci = [0]
		for i in range(len(candidate) - 1):
			if candidate[i] in {'H', 'R'}:
				loci[0] += len(candidate) - i - 1
		return loci

# NonFinality
# penalizes high tones associated to the final syllable
class NonFinality:
	def __init__(self):
		self.name = 'NonFinality'

	def vios(self, input, candidate):
		if candidate[-1] in {'H', 'R'}:
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
			if candidate[i] in {'H', 'L', 'R', 'M'}:
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
		total = 0
		for i in range(len(candidate)):
			if (input[i], candidate[i]) in {('L', 'X'), ('R', 'X'), ('M', 'X'), ('H', 'X'), ('H', 'x')}:
				total += 1
		return [total]

# Dep(link)
# penalizes creation of a high tone link
class Deplink:
	def __init__(self):
		self.name = 'Dep(link)'

	def vios(self, input, candidate):
		total = 0
		for i in range(len(candidate)):
			if (input[i], candidate[i]) in {('X', 'L'), ('X', 'R'), ('X', 'M'), ('X', 'H'), ('x', 'H')}:
				total += 1
		return [total]

# Max
# penalizes deletion of a floating high tone
class Max:
	def __init__(self):
		self.name = 'Max'

	def vios(self, input, candidate):
		input_tones = 0
		cand_tones = 0
		for i in range(len(candidate)):
			if input[i] in {'L', 'H', 'x'}:
				input_tones += 1
			if candidate[i] in {'L', 'H', 'x'}:
				cand_tones += 1
		if input_tones > cand_tones:
			return [1]
		return [0]
