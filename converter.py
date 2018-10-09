import shapefile

sf = shapefile.Reader('shape_files/Apkaimes')

fields = sf.fields

print(fields)

# todo: implement
