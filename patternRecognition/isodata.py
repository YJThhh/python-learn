
from math import sqrt
import numpy as np
# cluster points
SampleNum=8  # 样本数
PointData=np.array([([SampleNum, 1]),([0, 0]),([1, 1]),([2, 2]),
                                     ([3, 4]),([3, 5]),([4, 4]),
                                     ([4, 5]),([5, 6])])
points = PointData.tolist()[1:-1]

# measure distance between two points
def distance_2point(x1, y1, x2, y2):
	return sqrt((x2-x1)**2 + (y2-y1)**2)


# estimate volume of the cluster
def volume_estimation(cluster, center):
	num_of_points = len(cluster)
	distance = []
	for i in range(num_of_points):
		distance.append(distance_2point(center[0], center[1], cluster[i][0], cluster[i][1]))

	return sum(distance)/num_of_points


# defining of new cluster center
def new_cluster_centers(cluster):
	s = list(map(sum, zip(*cluster)))
	length = len(cluster)
	return (s[0]/length, s[1]/length)


# measure distances between each two pairs of cluster centers
def center_distance(centers):
	D_ij = {}
	# offset coeficient
	k = 0
	for i in range(len(centers)):
		for j in range(k, len(centers)):
			if i == j:
				pass
			else:
				D_ij[(i,j)] = distance_2point(centers[i][0], centers[i][1], centers[j][0], centers[j][1])
		k +=1
	return D_ij


# standart deviation vector for cluster
def standart_deviation(values, center):
	n = len(values) 
	x_coord = []
	y_coord = []
	for i in range(n):
		x_coord.append((values[i][0]-center[0])**2)
		y_coord.append((values[i][1]-center[1])**2)

	x = sqrt(sum(x_coord)/n)
	y = sqrt(sum(y_coord)/n)

	return (x,y)


def cluster_points_distribution(centers, points):
	centers_len = len(centers)
	points_len = len(points)
	distances = []
	distance = []

	# define array for clusters
	clusters = [[] for i in range(centers_len)]

	# iteration throught all points
	for i in range(points_len):
		# iteration throught all centers
		for j in range(centers_len):
			distance.append(distance_2point(centers[j][0], centers[j][1], points[i][0], points[i][1]))
		distances.append(distance)
		distance = []

	# distribution
	for i in range(points_len):
		ind = distances[i].index(min(distances[i]))
		clusters[ind].append(points[i])

	return clusters


def cluster_division(cluster, center, dev_vector):
	#divide only center of clusters

	# coeficient
	k = 0.5

	max_deviation = max(dev_vector)
	index = dev_vector.index(max(dev_vector))
	g = k*max_deviation

	# defining new centers
	center1 = list(center)
	center2 = list(center)
	center1[index] += g
	center2[index] -= g

	cluster1 = []
	cluster2 = []

	return tuple(center1), tuple(center2)
import matplotlib.pyplot as plt
def outputPlot(W):

            plt.figure(figsize=(8, 8))
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            color=[
                'red',
                'black',
                'blue',
                'pink',
                'green',
                'purple',
                'magenta'
            ]

            for idx,item_class in enumerate(W):
                X, Y = [], []
                for item_data in item_class:
                    X.append(item_data[0])
                    Y.append(item_data[1])
                plt.scatter(X, Y, color=color[idx])
            plt.show()

def cluster_union(cluster1, cluster2, center1, center2):
	x1 = center1[0]
	x2 = center2[0]
	y1 = center1[1]
	y2 = center2[1]
	n1 = len(cluster1)
	n2 = len(cluster2)

	x = (n1*x1 + n2*x2)/(n1+n2)
	y = (n1*y1 + n2*y2)/(n1+n2)
	center = (x,y)
	cluster = cluster1 + cluster2

	return center, cluster


def clusterize():

	# initial values
	K = 3 # max cluster number
	THETA_N = 1 # for cluster elimination
	THETA_S = 1 # for cluster division
	THETA_C = 3 # for cluster union
	L = 3 # 
	I = 4 # max number of iterations
	N_c = 1 # number of primary cluster centers

	distance = [] # distances array
	centers = [] # clusters centers
	clusters = [] # array for clusters points
	iteration = 1 # number of current iteration
	
	centers.append(points[0]) # first cluster center


	while iteration <= I:
		#print ("Iteration ", iteration)
		# step 2

		"""
		if there are one cluster center - all points goes to first cluster
		otherwise we distribute points between clusters
		"""
		if len(centers) <= 1:
			clusters.append(points)
		else:
			clusters = cluster_points_distribution(centers, points)
		
		# step 3
		# eliminating small clusters (unfinished!!!!!!)
		"""
		for i in range(len(clusters)):

			if len(clusters[i]) <= THETA_N:
				print(clusters[i][i])
				item = clusters[i][i]
				points.remove(item)
				#del clusters[i]
				break
			else:
				print("else")
			break	
			"""
			
		
		# step 4
		# erasing existing centers and defining a new ones
		centers = []
		for i in range(len(clusters)):
			centers.append(new_cluster_centers(clusters[i]))

		# step 5 - estimating volumes of all clusters
		# array for clusters volume
		D_vol = []
		for i in range(len(centers)):
			D_vol.append(volume_estimation(clusters[i], centers[i]))

		# step 6
		if len(clusters) <= 1:
			D = 0
		else:		
			cluster_length = []
			vol_sum = []
			for i in range(len(centers)):
				cluster_length.append(len(clusters[i]))
				vol_sum.append(cluster_length[i]*D_vol[i])

			D = sum(vol_sum)/len(points)


		# step 7
		if iteration >= I:
			THETA_C = 0

		elif (N_c >= 2*K) or (iteration % 2 == 0):
			pass

		else:
			# step 8
			# vectors of all clusters standart deviation 
			vectors = []
			for i in range(len(centers)):
				vectors.append(standart_deviation(clusters[i], centers[i]))

			# step 9
			max_s = []
			for v in vectors:
				max_s.append(max(v[0], v[1]))

			#step 10 (cluster division)
			for i in range(len(max_s)):
				length = len(clusters[i])
				coef = 2*(THETA_N+1)

				if (max_s[i] > THETA_S) and ((D_vol[i]>D and length>coef) or N_c<float(K)/2):
					center1, center2 = cluster_division(clusters[i], centers[i], vectors[i])
					del centers[i]
					centers.append(center1)
					centers.append(center2)
					N_c += 1

				else:
					pass
		

		#for i in clusters:
		#	print(i)

		# step 11
		D_ij = center_distance(centers)
		rang = {}
		for coord in D_ij:
			if D_ij[coord] < THETA_C:
				rang[coord] = (D_ij[coord])
			else:
				pass

		"""
		# step 13 (cluster union)
		for key in rang.keys():
			cluster_union(clusters[key], clusters[key.next()], centers[key], centers[key.next()])
			N_c -= 1

			"""

		iteration += 1


	return clusters

if __name__ == '__main__':
	# if file called as a script
	cl = clusterize()
	for i in cl:
		print("Cl", i)
	outputPlot(cl)


