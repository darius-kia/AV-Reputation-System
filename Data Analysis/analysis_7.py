import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 7 Collection

# In[ ]:


scenario7_path = args[1]
s7 = pd.read_csv(scenario7_path)


# In[ ]:


# different frequency of malicious vehicle transactions
malFreq = s7[
    (s7['velocity'] == 0.1) & 
    (s7['byWitnessRep'] == False) & 
    (s7['byNumWitnesses'] == False) &
    (s7['kNumWitnesses'] == 2.0) &
    (s7['useQuartiles'] == False)
][['percMalicious', 'operatingError', 'reportingError']]
malFreq.to_csv("10_malFreq.csv")