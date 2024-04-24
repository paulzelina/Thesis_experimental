import nibabel as nib
import numpy as np
import scilpy as sc
from dipy.io.image import load_nifti
from dipy.io.streamline import load_tractogram
from dipy.tracking.streamlinespeed import set_number_of_points
from scilpy.tracking.tools import resample_streamlines_num_points
from scilpy.tractanalysis.features import get_streamlines_centroid
from core1 import generate_core_streamline
from core2 import generate_core_streamline_new1
from fa_profiling import fa_profiling
from plot_fa import plot_fa_profiles
from robustReebConstruction import constructRobustReeb

fa_map, affine = load_nifti("/home/paulzelina/PycharmProjects/Thesis_experimental/100206__fa.nii.gz")
fa = nib.load("/home/paulzelina/PycharmProjects/Thesis_experimental/100206__fa.nii.gz")
#fa_data = fa_map.get_fdata()

# Load the tractography data
bundles_filename = "/home/paulzelina/PycharmProjects/Thesis_experimental/AF_left.tck"
streams = load_tractogram(bundles_filename, fa).streamlines

# Number of points to resample each streamline
num_points = 40

eps = 3
alpha = 4
delta = 0.1
def resample_streamlines_num_points(sft, num_points):
    """
    Resample streamlines using number of points per streamline

    Parameters
    ----------
    sft: StatefulTractogram
        SFT containing the streamlines to subsample.
    num_points: int
        Number of points per streamline in the output.

    Return
    ------
    resampled_sft: StatefulTractogram
        The resampled streamlines as a sft.
    """

    # Checks
    if num_points <= 1:
        raise ValueError("The value of num_points should be greater than 1!")

    # Resampling
    lines = set_number_of_points(sft, num_points)

    # Creating sft
    # CAREFUL. Data_per_point will be lost.
    #resampled_sft = _warn_and_save(lines, sft)

    return lines

streams = resample_streamlines_num_points(streams, num_points)
# Compute centroids using the first method
centroid_method = np.array(get_streamlines_centroid(streams, num_points))
centroid_method1 = np.array(generate_core_streamline(streams, percentage=5, nb_points=num_points))
centroid_method2 = np.array(generate_core_streamline_new1(streams, percentage=5, distance_threshold=25, nb_points=num_points))
result = fa_profiling(centroid_method, streams, fa_map, affine, num_points)
result1 = fa_profiling(centroid_method1, streams, fa_map, affine, num_points)
result2 = fa_profiling(centroid_method2, streams, fa_map, affine, num_points)

graph = constructRobustReeb(streams, eps, alpha, delta, 15)

print("Reeb graph generated: ", graph)

#plot_fa_profiles([result, result1, result2])
#print(np.mean(result2-result1), np.mean(result2-result), np.mean(result1-result))
