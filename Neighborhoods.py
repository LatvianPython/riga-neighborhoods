import shapefile
from shapely.geometry import Point
from shapely.geometry import shape
from lks92_converter import to_lks92


class Neighborhoods:
    def __init__(self):
        sf = shapefile.Reader("shape_files/Apkaimes")
        # points in file are [easting, northing]

        self._all_shapes = sf.shapes()
        self._all_records = sf.records()

    def get_neighborhood(self, lat, lng):
        name = None
        point = to_lks92(lat, lng)
        for i in range(0, len(self._all_shapes)):
            boundary = self._all_shapes[i]
            if Point(point).within(shape(boundary)):
                name = self._all_records[i][1]

        return name


if __name__ == "__main__":
    converter = Neighborhoods()

    result = converter.get_neighborhood(57.035006, 24.1310555)

    print(result)
