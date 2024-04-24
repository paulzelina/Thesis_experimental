import numpy as np
from dipy.tracking.streamline import values_from_volume
from nibabel.streamlines import ArraySequence
from scilpy.tracking.tools import resample_streamlines_num_points
from scilpy.tractanalysis.distance_to_centroid import min_dist_to_centroid

def fa_profiling(centroid, streams, fa_map, affine, num_points):
    centroid = ArraySequence(centroid)
    dists, labels = min_dist_to_centroid(streams._data, centroid._data)
    fa_values = values_from_volume(fa_map, streams, affine)

    # Initialize an empty list to hold the FA values for each centroid point
    fa_values_centroid = [[] for _ in range(num_points)]

    # Assign the FA values to the corresponding centroid point
    for fa_value, dist in zip(fa_values, dists):
        fa_values_centroid[dist].append(fa_value)

    # Calculate the average FA value for each centroid point
    fa_values_avg = [np.mean(values) for values in fa_values_centroid]

    return np.array(fa_values_avg, dtype=object)
