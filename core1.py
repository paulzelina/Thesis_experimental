import numpy as np
from dipy.tracking.utils import length
from dipy.tracking.streamline import Streamlines
from scilpy.tractanalysis.features import get_streamlines_centroid


def generate_core_streamline(streamlines, percentage, nb_points):
    # Step 1: Averaging the top percentage longest streamlines
    num_streamlines = len(streamlines)

    num_longest = int(percentage / 100 * num_streamlines)

    #return top_5_percent_streamlines
    lengths = list(length(streamlines))
    lengths_pts = [length(streamline) for streamline in streamlines]
    threshold = (np.percentile(lengths, 100-percentage))
    long_streamlines = Streamlines()
    for i, sl in enumerate(streamlines):
        if lengths[i] > threshold:
            long_streamlines.append(sl)

    core_streamline = get_streamlines_centroid(long_streamlines, nb_points)
    return core_streamline