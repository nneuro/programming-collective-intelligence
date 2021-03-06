def read_file(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    col_names = lines[0].strip().split('\t')[1:]
    row_names = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')

        # First column in each row is the row name
        row_names.append(p[0])

        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return row_names, col_names, data


from math import sqrt


def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(rows, distance=pearson):
    distances = {}
    current_clust_id = -1

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowest_pair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # Loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # Distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = \
                        distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowest_pair = (i, j)

        # Calculate the average of the two clusters
        merge_vec = [(clust[lowest_pair[0]].vec[i] + clust[lowest_pair[1]].vec[i])
                    / 2.0 for i in range(len(clust[0].vec))]

        # Create the new cluster
        new_cluster = bicluster(merge_vec, left=clust[lowest_pair[0]],
                               right=clust[lowest_pair[1]], distance=closest,
                               id=current_clust_id)

        # Cluster ids that weren't in the original set are negative
        current_clust_id -= 1
        del clust[lowest_pair[1]]
        del clust[lowest_pair[0]]
        clust.append(new_cluster)

    return clust[0]


def print_clust(clust, labels=None, n=0):
    # Indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id < 0:
        # Negative id means that this is branch
        print '-'
    else:
        # Positive id means that this is an endpoint
        if labels is None: print clust.id
        else: print labels[clust.id]

    # Now print the right and left branches
    if clust.left is not None: print_clust(clust.left, labels=labels, n=n + 1)
    if clust.right is not None: print_clust(clust.right, labels=labels, n=n + 1)
