import pandas as pd
import matplotlib
import re
import sys
args = sys.argv[1:]

filename = args[0]
df = pd.read_csv(filename)

print(df)
op_errs = []
rep_errs = []
for index, row in df.iterrows():
    i = row['operatingScores']
    diffs = []
    avs = i.split(",")
    for a_str in avs:
        status = re.search(r"\((\w+)\)", a_str)
        score = re.search(r"\d\.\d+", a_str)
        if status is None or score is None:
            continue
        else:
            status = status.group(1)
            score = float(score.group())
            expected = 1 if status == "NORM" or status == "MAL_REP" else 0
            diffs.append(abs(expected-score))
    if len(diffs) != 0:
        op_errs.append(sum(diffs)/len(diffs))
    else:
        op_errs.append("NA")

    i = row['reportingScores']
    diffs = []
    avs = i.split(",")
    for a_str in avs:
        status = re.search(r"\((\w+)\)", a_str)
        score = re.search(r"\d\.\d+", a_str)
        if status is None or score is None:
            continue
        else:
            status = status.group(1)
            score = float(score.group())
            expected = 1 if status == "NORM" or status == "MAL_OP" else 0
            diffs.append(abs(expected-score))
    if len(diffs) != 0:
        rep_errs.append(sum(diffs)/len(diffs))
    else:
        rep_errs.append("NA")
df['operatingError'] = op_errs
df['reportingError'] = rep_errs
print(df)
df.to_csv("errors_"+filename)
