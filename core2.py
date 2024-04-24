import numpy as np
import numpy as np
from scipy.spatial import ConvexHull
from core1 import generate_core_streamline


def generate_core_streamline_new1(streamlines, percentage = 5, distance_threshold = 20, nb_points = 40):
    # Step 1: Averaging the top percentage longest streamlines
    core_streamline = generate_core_streamline(streamlines, percentage, nb_points)

    # Step 2: Generating orthogonal planes and finding intersecting points
    core_streamline_array = core_streamline[0]  # Extract the NumPy array from the list
    all_centers_of_mass = []
    all_points_initial_core = []
    all_normals = []
    all_points = []
    all_areas = []
    #print(len(core_streamline_array))
    for i in range(len(core_streamline_array) - 1):
        segment = core_streamline_array[i:i+2]

        if len(segment) != 2:
            continue

        direction_vector = segment[1] - segment[0]
        tangent_vector = direction_vector / np.linalg.norm(direction_vector)

        # Compute a normal vector
        normal_vector = tangent_vector
        # Define the plane through the point segment[0] and normal to normal_vector
        plane_point = segment[0]  # Any point on the plane
        plane_normal = normal_vector  # The normal vector to the plane

        # Find intersection points of the plane with the rest of the streamlines
        intersection_points = []
        for streamline in streamlines:
            for j in range(len(streamline) - 1):
                line_point = streamline[j]  # Any point on the line
                line_vector = streamline[j+1] - streamline[j]  # The direction vector of the line

                # Solve for the intersection point
                t = np.dot(plane_normal, plane_point - line_point) / np.dot(plane_normal, line_vector)
                intersection_point = line_point + t * line_vector

                # Check if the intersection point lies within the line segment
                if 0 <= t <= 1:
                    distance = np.linalg.norm(intersection_point - segment[0])
                # Check if the distance is less than the threshold
                    if distance < distance_threshold:
                        intersection_points.append(intersection_point)

        if intersection_points:
            hull = ConvexHull(intersection_points)
            area = hull.area
            #print("Area is: ", area)
            all_areas.append(area)

            center_of_mass = np.mean(intersection_points, axis=0)
            all_centers_of_mass.append(center_of_mass)

    segment = core_streamline_array[nb_points-2:nb_points]

    direction_vector = segment[1] - segment[0]
    tangent_vector = direction_vector / np.linalg.norm(direction_vector)

    # Compute a normal vector
    normal_vector = tangent_vector
    # Define the plane through the point segment[0] and normal to normal_vector
    plane_point = segment[1]  # Any point on the plane
    plane_normal = normal_vector  # The normal vector to the plane

    # Find intersection points of the plane with the rest of the streamlines
    intersection_points = []
    for streamline in streamlines:
        for j in range(len(streamline) - 1):
             line_point = streamline[j]  # Any point on the line
             line_vector = streamline[j+1] - streamline[j]  # The direction vector of the line

             # Solve for the intersection point
             t = np.dot(plane_normal, plane_point - line_point) / np.dot(plane_normal, line_vector)
             intersection_point = line_point + t * line_vector
             # Check if the intersection point lies within the line segment
             if 0 <= t <= 1:
                distance = np.linalg.norm(intersection_point - segment[1])
             # Check if the distance is less than the threshold
                if distance < distance_threshold:
                    intersection_points.append(intersection_point)

    #print(len(intersection_points))
    if intersection_points:
        hull = ConvexHull(intersection_points)
        area = hull.area

        # Check if the current hull area is more than 2 times the min_area
        center_of_mass = np.mean(intersection_points, axis=0)
        all_centers_of_mass.append(center_of_mass)


    #print((all_centers_of_mass))
    #all_centers_of_mass = np.array(all_centers_of_mass).reshape(nb_points, 3)
    all_centers_of_mass = [np.array(all_centers_of_mass).reshape(-1, 3)]
    return (all_centers_of_mass)