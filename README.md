# Kaggle "Santa's Stolen Sleighs" Challenge

Simple recursive clustering attempt at solving "Santa's Stolen Sleighs" challenge.

The basic idea is to do an initial clustering, check for each cluster if the total weight exceeds the limit and if it does, do clustering on that cluster, and repeat for all new clusters.

For each final cluster, I sorted by weights.

I then tried a merging function where it would iterate over eligible pairs of clusters and merge them if it reduced the total cost.

# Quick Start
Download all files and run "python main.py"
