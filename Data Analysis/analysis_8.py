import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 8 Collection

# In[ ]:


scenario8_path = args[1]
s8 = pd.read_csv(scenario8_path)


# In[ ]:


# sparse population
sparsePop = s8[
    (s8['velocity'] == 0.1) & 
    (s8['byWitnessRep'] == False) & 
    (s8['byNumWitnesses'] == False) &
    (s8['kNumWitnesses'] == 2.0) &
    (s8['useQuartiles'] == False)
][['numVehicles', 'minRecipients', 'maxRecipients', 'operatingError', 'reportingError']]
sparsePop.to_csv("11_sparsePop.csv")