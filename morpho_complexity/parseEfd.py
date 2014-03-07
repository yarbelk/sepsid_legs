#!/usr/bin/env python2
import re
import sys
from pprint import pprint

_coef_re = re.compile(r"\s*(?P<A>-?\d+\.\d+(e-?\d+)?)"
                      r"\s*(?P<B>-?\d+\.\d+(e-?\d+)?)"
                      r"\s*(?P<C>-?\d+\.\d+(e-?\d+)?)"
                      r"\s*(?P<D>-?\d+\.\d+(e-?\d+)?)")

def split_on_names(filename):
    species = {}
    with open(filename, "r") as fd:
        lastName = ""
        for line in fd:
            line = line.strip()
            if line[0] == "#":
                continue
            data = re.split(r"\s+", line)
            if len(data) == 4:
                nOrder = [float(d) for d in data]
                species[lastName].append(nOrder)

            else:
                lastName = line
                if lastName in species:
                    raise RuntimeError("Duplicate species", lastName, species[lastName])
                species[lastName] = []

    return species


if __name__ == "__main__":
    pprint(split_on_names(sys.argv[1]))
