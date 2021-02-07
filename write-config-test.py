
data = [(39,40), (39,41), (40,39), (40,40), (41,40)]

f = open("config.dat", "w")
data_str = ""
separator = ","
for d in data:
    point = str(d[0]) + separator + str(d[1]) + "\n"
    data_str += point
f.write(data_str)
f.close()