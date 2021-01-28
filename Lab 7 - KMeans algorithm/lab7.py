# import necessary libraries.
import random
import argparse
import numpy as np
import pandas as pd
from scipy import spatial
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import glob
from PyPDF2 import PdfFileMerger


# function0: read data from the input file
def function0(file, features):
    data = pd.read_csv(file)
    features = features.split(",")
    features = [int(features[i]) for i in range(len(features))]
    category = data.iloc[:, -1]
    category = LabelEncoder().fit_transform(category)
    return data.iloc[:, features].values, category, data.columns[features]

# function1: randomly select K centers from data points
def function1(data1, k, seed):
    random.seed(seed)
    return random.sample(list(data1), k)

# function2: compute distance between data points and cluster centers
def function2(data2, centers, metric):
    k = len(centers)
    n = data2.shape[0]
    distance = np.zeros((n, k))
    if metric == '0':
        for i in range(n):
            for j in range(k):
                distance[i, j] = spatial.distance.cosine(data2[i, :], centers[j])
                m = "Cosine"
    elif metric == '1':
        for i in range(n):
            for j in range(k):
                distance[i, j] = spatial.distance.cityblock(data2[i, :], centers[j])
                m = "Manhattan"
    elif metric == '2':
        for i in range(n):
            for j in range(k):
                distance[i, j] = spatial.distance.euclidean(data2[i, :], centers[j])
                m = "Euclidean"
    elif metric == '3':
        for i in range(n):
            for j in range(k):
                distance[i, j] = spatial.distance.minkowski(data2[i, :], centers[j], p = 3)
                m = "Minkowski"
    return distance, m

# function3: assign data points to clusters
def function3(distance_matrix):
    return np.argmin(distance_matrix, axis=1)

# function4: compute new cluster centers
def function4(cluster, data3):
    new_cluster = []
    for i in np.unique(cluster):
        samples = data3[cluster == i]
        new_cluster.append(sum(samples) / samples.shape[0])
    return new_cluster

# function5: save results into the output file
def function5(data4, names, cluster, centroid, num, p, metr_name):
    plt.scatter(data4[:, 0], data4[:, 1], c=cluster)
    x_cent = [x[0] for x in centroid]
    y_cent = [x[1] for x in centroid]
    plt.scatter(x_cent, y_cent, s=60, marker="X", c='red')
    plt.xlabel(names[0])
    plt.ylabel(names[1])
    plt.title("Iteration #{iteration}, Purity score - {purity}, Metric - {metr_name}".format(iteration=num, purity=p, metr_name=metr_name))
    plt.savefig("./output/" + str(num) + ".pdf")
    plt.close()

# function6: compute purity
def function6(y_true, y_pred):
    contingency_matrix = metrics.cluster.contingency_matrix(y_true, y_pred)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)

def kmalgorithm(input_file, features, number_of_clusters, distance_metric, random_seed, number_of_iterations, output_file):
    iris_features, categories, feature_names = function0(input_file, features)
    centroids = function1(iris_features, number_of_clusters, random_seed)
    for i in range(number_of_iterations):
        dist_mat, used_metric = function2(iris_features, centroids, distance_metric)
        clusters = function3(dist_mat)
        purity = function6(categories, clusters)
        function5(iris_features, feature_names, clusters, centroids, i, purity, used_metric)
        centroids = function4(clusters, iris_features)
    dist_mat, used_metric = function2(iris_features, centroids, distance_metric)
    clusters = function3(dist_mat)
    np.savetxt(output_file, clusters, fmt="%d")

    merger = PdfFileMerger()
    files = [f for f in glob.glob("./output/*.pdf", recursive=False)]
    for png in files:
        merger.append(png)
    merger.write("output.pdf")
    merger.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_file", required=True, help="Name of input file")
    ap.add_argument("-f", "--features", default='all', help="Features to cluster")
    ap.add_argument("-k", "--number_of_clusters", default="3", help="Number of clusters")
    ap.add_argument("-d", "--distance_metric", default="2", help="Distance metric to cluster by")
    ap.add_argument("-s", "--random_seed", default="777", help="Random seed to use")
    ap.add_argument("-n", "--number_of_iterations", default="10", help="Number of iterations")
    ap.add_argument("-o", "--output_file", required=True, help="Name of output file")
    args = vars(ap.parse_args())

    kmalgorithm(args["input_file"], args["features"], int(args["number_of_clusters"]), args["distance_metric"], int(args["random_seed"]), int(args["number_of_iterations"]), args["output_file"])
