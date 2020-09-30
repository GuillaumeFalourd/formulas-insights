#!/usr/bin/python3
import os

from formula import formula

insightType = os.environ.get("INSIGHT_TYPE")
contribution = os.environ.get("CONTRIBUTION")
formula.Run(insightType, contribution)
