import pandas as pd
import numpy as np
import imp
import mycluster
import compute

hyperopt = imp.load_source('hyperopt','/usr/local/pkgs/hyperopt/')

gifts = pd.read_csv('gifts.csv')

print('Read gifts.csv')

X = gifts[['Latitude','Longitude']]
X = np.asarray(X)
y = gifts['Weight']

best_score = 100000000000000000
best_e=100
e=[]
best_d=0
d=[]
scores=[]

for e_iter in [15,7,1]:
	for d_iter in [1,0.8,0.5]:
		e.append(e_iter)
		d.append(d_iter)
		Z = mycluster.hcluster(X,y,e_iter,d_iter)
		s = compute.weighted_reindeer_weariness(Z)
		scores.append(s)
		if(s<best_score):
			best_e = e_iter
			best_d = d_iter
			best_score=s

for i in range(len(e)):
	print e[i],d[i],scores[i]

print "BEST SCORE : ",best_score, " for e : ",best_e, " and d : ", best_d

print "Redo best score clustering"
Z=mycluster.hcluster(X,y,best_e,best_d)

print "Preparing and writing csv"
Z = Z[Z['TripId']>=0]
Z = Z.drop('Longitude',1)
Z = Z.drop('Latitude',1)
Z = Z.drop('Weight',1)
Z = Z.astype(int)
Z.to_csv('trips.csv',header=False)
