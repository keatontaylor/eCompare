### Power cost comparison python code 


### TODO: data structure for past data.


### TODO: Logic for calculating new rate based on new parameters
### Cost per kWh in range, might be a static value or per kWh
### might include incentives if certain critera are met
### might have base charge additons

### Rules can be written as class isntance that define the behavior 
### for a range or per kWh this will allow the creation of rules
### that can then be piped into the core logic to produce results

class EnergyCompare(list):
	def __init__(self, oldCosts, baseCharge=None, tax=None):
		self.baseCharge = None
		self.tax = None
		self.oldCosts = oldCosts
		self.newCosts = []

	def getRange(self, kWhRange, value):
		nums = list(range(value+1))
		i = 0
		for x in nums:
			if x >= kWhRange[0] and x <= kWhRange[-1] and x != 0:
				i = i + 1
		return i

	def addRule(self, kWhRange=None, costPerkWh=None, constantCharge=None, override=False):
		class rangeRule(EnergyCompare):
			def __init__(self, kWhRange, cost, override):
				self.kWhRange = kWhRange
				self.cost = cost
				self.override = override
				self.rules = 'rangeRule(costPerkWh={}, override={})'.format(costPerkWh, override)
			def apply(self, value):
				kWh = self.getRange(self.kWhRange, value)
				if kWh > 0:
					return (kWh * self.cost)
				else: 
					return 0

		class constantRule(EnergyCompare):
			def __init__(self, kWhRange, constantCharge, override):
				self.kWhRange = kWhRange
				self.constantCharge = constantCharge
				self.override = override
				self.rules = 'constantRule(constantCharge={}, override={})'.format(costPerkWh, override)
			def apply(self, value):
				kWh = self.getRange(self.kWhRange, value)
				if kWh > 0: return constantCharge
				else: 
					return 0
		
		if costPerkWh is not None:
			self.append(rangeRule(kWhRange=kWhRange, cost=costPerkWh, override=override))
		if constantCharge is not None:
			self.append(constantRule(kWhRange=kWhRange, constantCharge=constantCharge, override=override))

	def calculateCost(self):
		newCosts = []
		for key, value in self.oldCosts.items():
			ruleCost = 0
			for rule in self:
				if rule.override:
					ruleCost = rule.apply(value)
				elif rule.apply(value) !=0:
					ruleCost += rule.apply(value)
			newCosts.append(round(ruleCost, 2))
		self.newCosts = newCosts
		return newCosts

	def prettyPrint(self):
		print(list(self.oldCosts.keys()))
		print(self.newCosts)


oldCost = {37.97:551, 32.06:432, 30.82:444, 34.81:532, 32.27:476, 44.41:743, 86.01:1344, 85.73:1341, 77.57:1195, 54.29:887, 31.17: 417}
energy = EnergyCompare(oldCost)
energy.addRule(kWhRange=range(0, 1000), costPerkWh=0.089)
energy.addRule(kWhRange=range(1001,1499), constantCharge=0.119)
energy.calculateCost()
energy.prettyPrint()


