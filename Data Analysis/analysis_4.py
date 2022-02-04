import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 4 Collection

# In[ ]:


scenario4_path = args[1]
s4 = pd.read_csv(scenario4_path)


# In[ ]:


# large population
largePopulation = s4[
    (s4['velocity'] == 0.1) & 
    (s4['byWitnessRep'] == False) & 
    (s4['byNumWitnesses'] == False) &
    (s4['kNumWitnesses'] == 2.0) &
    (s4['useQuartiles'] == False)
][['numVehicles', 'operatingError', 'reportingError']]
largePopulation.to_csv("7_largePopulation.csv")