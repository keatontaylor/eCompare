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
				if rule.override and rule.apply(value) != 0:
					ruleCost = rule.apply(value)
				elif rule.apply(value) != 0:
					ruleCost += rule.apply(value)
			newCosts.append(round(ruleCost, 2))
		self.newCosts = newCosts
		return newCosts

	def prettyPrint(self):
		print("{0:<16} {1:<16} {2:<16} {3:<16}".format("Old Yearly Cost", "New Yearly Cost", "Difference ($)", "Difference (%)"))
		oldYearlyCost = sum(list(self.oldCosts.keys()))
		newYearlyCost = sum(self.newCosts)
		print(list(self.oldCosts.keys()))
		print(self.newCosts)
		differenceDollars = sum(self.newCosts) - sum(list(self.oldCosts.keys()))
		differencePercent = ((newYearlyCost-oldYearlyCost)/((newYearlyCost+oldYearlyCost)/2))*100
		print("${0:<15.2f} ${1:<15.2f} ${2:<15.2f} {3:<1.2f}%".format(round(oldYearlyCost, 2), round(newYearlyCost,2), differenceDollars, differencePercent))



oldCost = {32.27:476, 44.41:743, 86.01:1344, 85.73:1341, 77.57:1195, 54.29:887, 31.17:417, 32.15:402, 32.16:363, 32.17:349, 32.18:349, 32.19:406}

## Pollution FreeTM Conserve 12 Choice
energy = EnergyCompare(oldCost)
energy.addRule(kWhRange=range(0,1000), costPerkWh=0.051453)
energy.addRule(kWhRange=range(1001,5000), costPerkWh=0.094943)
energy.addRule(kWhRange=range(0,5000), constantCharge=3.49)
energy.addRule(kWhRange=range(0,5000), costPerkWh=0.034556)
energy.calculateCost()
energy.prettyPrint()

energy1 = EnergyCompare(oldCost)
energy1.addRule(kWhRange=range(0,5000), costPerkWh=0.057198)
energy1.addRule(kWhRange=range(0,5000), constantCharge=3.49)
energy1.addRule(kWhRange=range(0,5000), costPerkWh=0.034556)
energy1.calculateCost()
energy1.prettyPrint()


