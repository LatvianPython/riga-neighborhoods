import math


def meridional_arc(phi):
    # approximation based on pre-calculated values
    return (111132.95255 * math.degrees(1 * phi) -
            16038.509 * math.sin(2 * phi) +
            16.833 * math.sin(4 * phi) -
            0.022 * math.sin(6 * phi) +
            0.00003 * math.sin(8 * phi))


def to_lks92(lat, lng):
    # assume lat/lng were passed as degrees, thus we convert to radians as calculations are to be done with radians
    lat = math.radians(lat)
    lng = math.radians(lng)

    semi_major_axis = 6378137.0
    semi_minor_axis = 6356752.314140

    flattening = (semi_major_axis - semi_minor_axis) / semi_major_axis

    first_eccentricity = flattening * (2.0 - flattening)

    second_eccentricity = first_eccentricity / math.pow(1.0 - flattening, 2.0)

    radius_of_curvature_meridian = ((semi_major_axis * (1.0 - first_eccentricity)) /
                                    math.pow((1.0 - first_eccentricity * math.pow(math.sin(lat), 2.0)), 3.0 / 2.0)
                                    )

    radius_of_curvature_prime = radius_of_curvature_meridian * (1 + second_eccentricity * math.pow(math.cos(lat), 2))

    meridional_distance = meridional_arc(lat)

    scale = 0.9996

    # specific for LKS92
    delta_lng = lng - math.radians(24.0)
    false_easting = 500000.0
    false_northing = -6000000.0

    tan = math.tan(lat)
    tan_sqr = math.pow(tan, 2.0)

    # todo: a lot of potential for simplification
    terms = {'1': (meridional_distance * scale),
             '2': (radius_of_curvature_prime * math.sin(lat) * math.cos(lat) * scale) / 2.0,
             '3': (((radius_of_curvature_prime * math.sin(lat) * math.pow(math.cos(lat), 3.0) * scale) / 24.0) *
                   (5.0 -
                    tan_sqr +
                    9.0 * second_eccentricity * math.pow(math.cos(lat), 2.0) +
                    4.0 * second_eccentricity * second_eccentricity * math.pow(math.cos(lat), 4.0)
                    )
                   ),
             '4': (((radius_of_curvature_prime * math.sin(lat) * math.pow(math.cos(lat), 5.0) * scale) / 720.0) *
                   (61.0 -
                    58.0 * tan_sqr +
                    tan_sqr * tan_sqr +
                    270.0 * second_eccentricity * math.pow(math.cos(lat), 2.0) -
                    330.0 * tan_sqr * lat * second_eccentricity * math.pow(math.cos(lat), 2.0)
                    )
                   ),
             '5': (((radius_of_curvature_prime * math.sin(lat) * math.pow(math.cos(lat), 7.0) * scale) / 40320.0) *
                   (1385.0 -
                    3111.0 * tan_sqr +
                    543.0 * tan_sqr * tan_sqr -
                    tan_sqr * tan_sqr * tan_sqr
                    )
                   ),
             '6': radius_of_curvature_prime * math.cos(lat) * scale,
             '7': (((radius_of_curvature_prime * math.pow(math.cos(lat), 3.0) * scale) / 6.0) *
                   (1.0 -
                    tan_sqr +
                    second_eccentricity * math.pow(math.cos(lat), 2.0)
                    )
                   ),
             '8': (((radius_of_curvature_prime * math.pow(math.cos(lat), 5.0) * scale) / 120.0) *
                   (5.0 -
                    18.0 * tan_sqr +
                    tan_sqr * tan_sqr +
                    14.0 * second_eccentricity * math.pow(math.cos(lat), 2.0) -
                    58.0 * tan_sqr * second_eccentricity * math.pow(math.cos(lat), 2.0)
                    )
                   ),
             '9': (((radius_of_curvature_prime * pow(math.cos(lat), 7.0) * scale) / 5040.0) *
                   (61.0 -
                    479.0 * tan_sqr +
                    179.0 * tan_sqr * tan_sqr -
                    tan_sqr * tan_sqr * tan_sqr
                    )
                   )}

    northing = (false_northing +
                terms['1'] +
                terms['2'] * math.pow(delta_lng, 2.0) +
                terms['3'] * math.pow(delta_lng, 4.0) +
                terms['4'] * math.pow(delta_lng, 6.0) +
                terms['5'] * math.pow(delta_lng, 8.0))

    easting = (false_easting +
               terms['6'] * delta_lng +
               terms['7'] * math.pow(delta_lng, 3.0) +
               terms['8'] * math.pow(delta_lng, 5.0) +
               terms['9'] * math.pow(delta_lng, 7.0))

    return [round(northing, 3), round(easting, 3)]


# Skujas 57 15 15.45640 25 25 53.92363
# ->
# Skujas	   346600.927 586371.641

# 57°15'15.5"N 25°25'53.9"E
# ->
# 57.254293, 25.431646

latitude, longitude = 57.254293, 25.431646

result = to_lks92(latitude, longitude)

official = [346600.927, 586371.641]

print('lat: {}\nlng: {}'.format(latitude, longitude))
print('conversion to LKS92 values in [m]\n{}'.format('-' * 60))
print('                 [Northing  , Easting   ]')
print('my_conversion:   {}'.format(result))
print('official gov.lv: {}'.format(official))
print('error: {}, {}'.format(round(result[0] - official[0], 3), round(result[1] - official[1], 3)))
