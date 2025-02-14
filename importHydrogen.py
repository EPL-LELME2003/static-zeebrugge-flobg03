# Florian Peeters
"""
import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()

# Define model parameters
LHV_NH3 = 18.5 # MJ/kg
LHV_CH4 = 50 # MJ/kg
Volume = 200000 # m3
Density_NH3 = 600 # kg/m3
Density_CH4 = 500 # kg/m3
Losses_NH3 = 0.4 # 40%
Losses_CH4 = 0.35 # 35%
H2_t = 0.25 # pour CH4
CO2_t = 2.75 # pour CH4
maxboats = 100

# Define model variables
model.boatNH3 = pyo.Var(domain=pyo.NonNegativeReals)
model.boatCH4 = pyo.Var(domain=pyo.NonNegativeReals)

# Define the objective functions
model.obj = pyo.Objective(expr = Volume*Density_CH4*model.boatCH4 + Volume*Density_NH3*model.boatNH3, sense=pyo.maximize)

# Define the constraints
model.constraint1 = pyo.Constraint(expr = model.boatNH3 + model.boatCH4<=100)
model.constraint2 = pyo.Constraint(expr = Volume*Density_CH4*model.boatCH4/(1-Losses_CH4) + Volume*Density_NH3*model.boatNH3/(1-Losses_NH3) <= 140*10**3)
model.constraint3 = pyo.Constraint(expr = model.boatCH4*Volume*Density_CH4*CO2_t <= 14*10**6)
# Specify the path towards your solver (gurobi) file
solver = pyo.SolverFactory("gurobi")
sol = solver.solve(model)

# Print here the number of CH4 boats and NH3 boats
print("Number of CH4 boats: ", model.boatCH4())
print("Number of NH3 boats: ", model.boatNH3())
##########################################
############ CODE TO ADD HERE ############
##########################################
"""
import pyomo.environ as pyo

# Create a Pyomo model
model = pyo.ConcreteModel()



# Define model parameters
model.H2inNH3 = pyo.Param(initialize=0.18)
model.H2inCH4 = pyo.Param(initialize=0.25)
model.CO2inCH4 = pyo.Param(initialize=2.75)
model.volumeBoat = pyo.Param(initialize=200000.)
model.densityNH3 = pyo.Param(initialize=0.6)
model.densityCH4 = pyo.Param(initialize=0.5)
model.LHV_NH3 = pyo.Param(initialize=18.5) #GJ/t
model.LHV_CH4 = pyo.Param(initialize=50.) #GJ/t
model.losses_NH3 = pyo.Param(initialize=0.4)
model.losses_CH4 = pyo.Param(initialize=0.35) 
model.maxBoats = pyo.Param(initialize=100.)
model.maxEnergy = pyo.Param(initialize=140*1E6*3.6) #MJ
model.maxCO2 = pyo.Param(initialize=14E6)


# Define model variables
model.boatsNH3 = pyo.Var(domain=pyo.NonNegativeReals)
model.boatsCH4 = pyo.Var(domain=pyo.NonNegativeReals)

# Define objective function
model.objective = pyo.Objective(expr=model.boatsCH4*model.volumeBoat*model.densityCH4*model.H2inCH4+model.boatsNH3*model.volumeBoat*model.densityNH3*model.H2inNH3, sense=pyo.maximize)

# Define constraints
def maxBoats(model):
    return model.boatsNH3+model.boatsCH4 <= model.maxBoats

model.maxBoatsConstr = pyo.Constraint(rule=maxBoats)

def maxEnergy(model):
    return model.boatsNH3*model.volumeBoat*model.densityNH3*model.LHV_NH3/(1.-model.losses_NH3) + model.boatsCH4*model.volumeBoat*model.densityCH4*model.LHV_CH4/(1-model.losses_CH4) <= model.maxEnergy

model.maxEnergyConstr = pyo.Constraint(rule=maxEnergy)

def maxCO2(model):
    return model.boatsCH4*model.volumeBoat*model.densityCH4*model.CO2inCH4 <= model.maxCO2

model.maxCO2Constr = pyo.Constraint(rule=maxCO2)

model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)

solver = pyo.SolverFactory('gurobi')
sol = solver.solve(model)


print(model.boatsCH4.value)
print(model.boatsNH3.value)
model.display()
model.dual.display()
model.rc.display()