#!/usr/bin/env python
# coding: utf-8

# # Import Packages

# In[ ]:

import sys
import pandas as pd

args = sys.argv
assert(len(args[1:]) == 8), "Must include all 8 scenario files"

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


# ## Scenario 2 Collection

# In[ ]:


scenario2_path = args[2]
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


# ## Scenario 3 Collection

# In[ ]:


scenario3_path = args[3]
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


# ## Scenario 4 Collection

# In[ ]:


scenario4_path = args[4]
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


# ## Scenario 5 Collection

# In[ ]:


scenario5_path = args[5]
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


# ## Scenario 6 Collection

# In[ ]:


scenario6_path = args[6]
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


# ## Scenario 7 Collection

# In[ ]:


scenario7_path = args[7]
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


# ## Scenario 8 Collection

# In[ ]:


scenario8_path = args[8]
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
sparsePop.to_csv("10_malFreq.csv")

