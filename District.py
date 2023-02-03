class District:
    def __init__(self):
        District.index += 1
        self.index = District.index
        self.number_edges = 0
        self.number_edges_odd = 0
        self.max_distance = 0
        self.edges = list()
        
    def update_max_distance(self):
        #do a bfs to update the max distance
        self.max_distance = 0
    
    def get_odd_rate(self):
        return self.number_edges_odd/self.number_edges
    
    def update_odd(self):
        #search for how many nodes contribute with odd number of edges to this district
        self.number_edges_odd = 0
            
    
    def add_edge(self, edge):
        self.number_edges+=1
        self.edges.append(edge)
        self.update_odd(self)
    
    