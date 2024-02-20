import glob
import numpy as np
import pandas as pd
import statistics
from collections import defaultdict

if __name__ == "__main__":
    data = glob.glob("data/*.csv")
    data_map = defaultdict(list)

    for subject in data:
        with open(subject, 'r') as infile:
            # skip the header on each file
            _ = infile.readline()

            for i, line in enumerate(infile.readlines()):
                # destructure the data
                dist, size, direction, time, traveled, errors = line.split(",")
                data_map[f"{dist}_{size}"].append(float(time))

    for key, value in data_map.items():
        avg = statistics.mean(value)
        std = statistics.stdev(value)
        print(f"{key = }, {avg = }, {std = }")
