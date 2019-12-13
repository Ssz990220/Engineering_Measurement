def extract_corner(points, threshold):
    corner_bin = []
    for point in points:
        if not corner_bin:
            corner_bin.append(point)
        else:
            for corner in corner_bin:
                if abs(corner[0] - point[0]) < threshold & abs(corner[1] - point[1] < threshold):
                    corner_update = ((corner[0] + point[0]) / 2, (corner[1] + point[1]) / 2)
                    corner_bin.remove(corner)
                    corner_bin.append(corner_update)
                else:
                    corner_bin.append(point)
    return corner_bin
