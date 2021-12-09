import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 5 Collection

# In[ ]:


scenario5_path = args[1]
s5 = pd.read_csv(scenario5_path)


# In[ ]:


# dense population
densePopulation = s5[
    (s5['velocity'] == 0.1) & 
    (s5['byWitnessRep'] == False) & 
    (s5['byNumWitnesses'] == False) &
    (s5['kNumWitnesses'] == 2.0) &
    (s5['useQuartiles'] == False)
][['propWitnesses', 'percTransaction', 'operatingError', 'reportingError']]
densePopulation.to_csv("8_densePopulation.csv")