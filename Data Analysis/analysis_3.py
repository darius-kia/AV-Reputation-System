import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 3 Collection

# In[ ]:


scenario3_path = args[1]
s3 = pd.read_csv(scenario3_path)


# In[ ]:


# high noise environment
highNoise = s3[
    (s3['velocity'] == 0.1) & 
    (s3['byWitnessRep'] == False) & 
    (s3['byNumWitnesses'] == False) &
    (s3['kNumWitnesses'] == 2.0) &
    (s3['useQuartiles'] == False)
][['broadcastNoise', 'witnessNoise', 'operatingError', 'reportingError']]
highNoise.to_csv("6_highNoise.csv")