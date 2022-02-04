import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 6 Collection

# In[ ]:


scenario6_path = args[1]
s6 = pd.read_csv(scenario6_path)


# In[ ]:


# use malicious operating and reporting vehicles
useMalOpRep = s6[
    (s6['velocity'] == 0.1) & 
    (s6['byWitnessRep'] == False) & 
    (s6['byNumWitnesses'] == False) &
    (s6['kNumWitnesses'] == 2.0) &
    (s6['useQuartiles'] == False)
][['useMalOp', 'useMalRep', 'operatingError', 'reportingError']]
useMalOpRep.to_csv("9_useMalOpRep.csv")