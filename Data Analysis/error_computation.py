import pandas as pd
import matplotlib
import re
import sys
args = sys.argv[1:]

filename = args[0]
df = pd.read_csv(filename)

op_errs = []
rep_errs = []
for index, row in df.iterrows():
    i = row['operatingScores']
    diffs = []
    avs = i.split(",")
    for a_str in avs:
        status = re.search(r"\((\w+)\)", a_str).group(1)
        score = float(re.search(r"\d\.\d+", a_str).group())
        expected = 1 if status == "NORM" or status == "MAL_REP" else 0
        diffs.append(abs(expected-score))
    op_errs.append(sum(diffs)/len(diffs))

    i = row['reportingScores']
    diffs = []
    avs = i.split(",")
    for a_str in avs:
        status = re.search(r"\((\w+)\)", a_str).group(1)
        score = float(re.search(r"\d\.\d+", a_str).group())
        expected = 1 if status == "NORM" or status == "MAL_OP" else 0
        diffs.append(abs(expected-score))
    rep_errs.append(sum(diffs)/len(diffs))
df['operatingError'] = op_errs
df['reportingError'] = rep_errs
df.to_csv("errors_"+filename)
