class Edge:
    def __init__(self):
        self.district = None
        self.distance = 1
        self.vertices = list()
        self.distance_to_deposit = list()
        Edge.universe.append(self)
    
    def update_district(self, district):
        self.district = district