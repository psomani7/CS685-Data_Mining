import numpy as np
import pandas as pd
import json

f = open('./neighbor-districts-modified.json')
data = json.load(f)

district_list = []
edge_list = []
for dist in data:
    district_list.append(dist)
    for neighbour in data[dist]:
        if(neighbour not in district_list):
            edge_list.append([dist, neighbour])

write_data = pd.DataFrame(edge_list)
write_data.to_csv('./output/edge-graph.csv', index=False, header=False)