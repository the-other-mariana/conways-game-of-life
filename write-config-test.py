
"""Script that helps to write a config.dat file quickly. Remember is defined by (x,y), not by (i,j)"""

# Example 1
data = [(39,40), (39,41), (40,39), (40,40), (41,40)]

# Example 2
data2 = [(40, 20), (40, 21), (41, 20), (41, 21), (40, 30), (39, 30), (41, 30), (38, 31), (37, 32), (37, 33), (42, 31), (43, 32), (43, 33), (42, 35), (41, 36), (40, 36), (39, 36), (38, 35), (40, 34), (40, 37), (41, 40), (42, 40), (43, 40), (41,41), (42, 41), (43, 41), (40, 42), (44, 42), (40, 44), (39, 44), (44, 44), (45, 44), (42, 54), (43, 54), (42, 55), (43, 55)]


# choose
choice = data

f = open("config.dat", "w")
data_str = ""
separator = " "
for d in choice:
    point = str(d[0]) + separator + str(d[1]) + "\n"
    data_str += point
f.write(data_str)
f.close()
