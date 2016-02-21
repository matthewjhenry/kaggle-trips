import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from math import radians, cos, sin, asin, sqrt
import compute

"""
Code for hierarchical clustering, modified from 
Programming Collective Intelligence by Toby Segaran 
(O'Reilly Media 2007, page 33). 
"""

class mycluster:
    def __init__(self,id,eps,locvec=[],indvec=[],count=0,totweight=0):
        self.locvec=locvec
	self.indvec=indvec
        self.id=id
        self.count=count
	self.totweight=totweight
	self.eps=eps

def merge_(mycluster1,mycluster2,X):
	indvec3= mycluster1.indvec + mycluster2.indvec
	locvec3 = X[indvec3,:]
	id3=min(mycluster1.id, mycluster2.id)
	mycluster1.id=-15
	mycluster2.id=-15
	count3 = mycluster1.count+mycluster2.count
	totweight3 = mycluster1.totweight + mycluster2.totweight
	eps3 = min(mycluster1.eps, mycluster2.eps)
	mycluster3=mycluster(id3,eps3,locvec3,indvec3,count3,totweight3)
	return mycluster3

def hcluster(X,y,init_eps=20,d_eps=0.8):
	# X feats, y weights

	# return clusters
	myclusters_=[]

	model=DBSCAN(eps=20,min_samples=1).fit(X)
	print "First clustering done."

	#index=np.asarray(range(y.shape[0]))
	final_label=len(set(model.labels_))+1
	
	# first clustering
	for lab in set(model.labels_):
		clu = mycluster(lab,init_eps,[],[],0,0)
		for w in range(len(y)):
			if model.labels_[w]==lab:
				clu.indvec.append(w)
				clu.count = clu.count+1
				clu.totweight = clu.totweight+y[w]
		clu.locvec=X[clu.indvec,:]
		myclusters_.append(clu)
	print "Number of clusters : ", len(myclusters_)

	# while there are some clusters with totweight>1000, continue clustering
	while(np.sum([((clu.totweight>1000) and (clu.id>=0)) for clu in myclusters_])>0):
		print "# of totweights over 1000 : ", np.sum([((clu.totweight>1000) and (clu.id>=0)) for clu in myclusters_])
		for clu in myclusters_:
			if (clu.totweight>1000) and (clu.id>=0) :
				clu.id=-5 # invalidate cluster
				clu.eps=clu.eps*d_eps
				# cluster elements
				model = DBSCAN(eps=clu.eps,min_samples=1).fit(np.array(clu.locvec))
				for lab in set(model.labels_):
					nclu=mycluster(final_label,clu.eps,[],[],0,0)
					final_label=final_label+1
					for w in range(clu.count):
						if model.labels_[w]==lab:
							nclu.indvec.append(clu.indvec[w])
							nclu.count=nclu.count+1
							nclu.totweight=nclu.totweight+y[clu.indvec[w]]
					nclu.locvec=X[nclu.indvec,:]
					myclusters_.append(nclu)
					if len(myclusters_) % 1000 ==0:
						print "Size of myclusters_ : ", len(myclusters_)
	# checkup
        print "Last check"
        we = 0
        c = 0
        for clu in myclusters_:
                if clu.id >=0:
                        we = we + clu.totweight
                        c = c + clu.count
                        if clu.totweight>1000:
                                print "ERROR OVERWEIGHT"
	print "Total Weight : ",we," and total count : ", c
	print "Real total weight : ", np.sum(y), " and total count : ", y.shape[0]

	Z = np.ones(y.shape)*(-10)
	
	Z_ind=1
	for clu in myclusters_:
                if clu.id >=0:
			for index in clu.indvec:
				if Z[index] != (-10):
					print "Z error"
				Z[index]=Z_ind
	'''			Z_ind=Z_ind+1
	# Final checkup
	print "Final checkup"
	for h in np.unique(Z):
		tot=0
		for i in range(len(Z)):
			if Z[i]==h:
				tot=tot+y[i]
		if tot>1000:
			print "Error : total = ", tot, " for ", i
	'''
	d = np.column_stack((Z,X[:,0],X[:,1],y))
	print d.shape
	myclusters_pd = pd.DataFrame(d,columns=["TripId","Latitude", "Longitude", "Weight"])
	
	# sort by weights for each trip
	print "Sorting by weights for each trip"
	myclusters_pd = myclusters_pd.sort_values(by=['TripId','Weight'],ascending=False)

	print(myclusters_pd.head())
        return myclusters_pd
