import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 2 Collection

# In[ ]:


scenario2_path = args[1]
s2 = pd.read_csv(scenario2_path)


# In[ ]:


# high concentration of malicious vehicles
malEnv = s2[
    (s2['velocity'] == 0.1) & 
    (s2['byWitnessRep'] == False) & 
    (s2['byNumWitnesses'] == False) &
    (s2['kNumWitnesses'] == 2.0) &
    (s2['useQuartiles'] == False)
][['propNormal', 'operatingError', 'reportingError']]
malEnv.to_csv("5_malEnv.csv")