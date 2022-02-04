import pandas as pd
import sys

args = sys.argv
assert(len(args[1:]) == 1), "Must include data file name"


# ## Scenario 1 Collection

# In[ ]:


scenario1_path = args[1]
s1 = pd.read_csv(scenario1_path)


# In[ ]:


# effect from velocity
vel = s1[
    (s1['byWitnessRep'] == False) & 
    (s1['byNumWitnesses'] == False) & 
    (s1['kNumWitnesses'] == 2.0) &
    (s1['useQuartiles'] == False)
]
vel[['velocity', 'operatingError', 'reportingError']].to_csv("0_velocity.csv")


# In[ ]:


# effect from byWitnessRep
bWR = s1[
    (s1['velocity'] == 0.1) & 
    (s1['byNumWitnesses'] == False) & 
    (s1['kNumWitnesses'] == 2.0) &
    (s1['useQuartiles'] == False)
]
bWR[['byWitnessRep', 'operatingError', 'reportingError']].to_csv("1_byWitnessRep.csv")


# In[ ]:


# effect from byNumWitnesses
bNW = s1[
    (s1['velocity'] == 0.1) & 
    (s1['byWitnessRep'] == False) & 
    (s1['kNumWitnesses'] == 2.0) &
    (s1['useQuartiles'] == False)
]
bNW[['byNumWitnesses', 'operatingError', 'reportingError']].to_csv("2_byNumWitnesses.csv")


# In[ ]:


# effect from kNumWitnesses
kNW = s1[
    (s1['velocity'] == 0.1) & 
    (s1['byWitnessRep'] == False) & 
    (s1['byNumWitnesses'] == False) &
    (s1['useQuartiles'] == False)
][['kNumWitnesses', 'operatingError', 'reportingError']]
kNW.to_csv("3_kNumWitnesses.csv")


# In[ ]:


# effect from useQuartiles
useQuartiles = s1[
    (s1['velocity'] == 0.1) & 
    (s1['byWitnessRep'] == False) & 
    (s1['byNumWitnesses'] == False) &
    (s1['kNumWitnesses'] == 2.0) 
][['useQuartiles', 'operatingError', 'reportingError']]
useQuartiles.to_csv("4_useQuartiles.csv")