verts = [PVector(901.12, 300),PVector(853.48, 279.76),PVector(768.04, 270.04),PVector(701.56, 261.04),
         PVector(684.4, 253.72),PVector(684.4, 250.48),PVector(701.32, 234.76),PVector(701.2, 231.28),
         PVector(685.84, 223.48),PVector(631.12, 220.6),PVector(570.52, 218.32),PVector(534.88, 200.68),
         PVector(434.2, 50.56),PVector(362.68, 50.56),PVector(320.32, 218.44),PVector(306.16, 213.52),
         PVector(258.28, 140.68),PVector(191.44, 140.68),PVector(164.8, 253.12),PVector(233.68, 262.96),
         PVector(245.92, 265.12),PVector(252.64, 268.72),PVector(278.2, 268.12),PVector(265.0, 276.04),
         PVector(244.24, 284.68), PVector(244.24, 315.32), PVector(265.0, 323.96),PVector(278.2, 331.88),
         PVector(252.64, 331.28),PVector(245.92, 334.88),PVector(233.68, 337.04),PVector(164.8, 346.88),
         PVector(191.44, 459.32),PVector(258.28, 459.32),PVector(306.16, 386.47998),PVector(320.32, 381.56),
         PVector(362.68, 549.44),PVector(434.2, 549.44),PVector(534.88, 399.32),PVector(570.52, 381.68),
         PVector(631.12, 379.4),PVector(685.84, 376.52002),PVector(701.2, 368.72),PVector(701.32, 365.24),
         PVector(684.4, 349.52002),PVector(684.4, 346.28),PVector(701.56, 338.96),PVector(768.04, 329.96),
         PVector(853.48, 320.24)]

             
                    

class Skeleton(object):
    def __init__(self, verts, tol = 0):
        self.vertices = verts
        self.branches = []
        self.bones = []
        self.rays = []
        self.tol = tol
        self.run()
        
        
    def run(self):
        
        '''Runs the algorithm.'''
        
        self.initialize
        self.reduce
                
        
    @property
    def initialize(self):
        
        '''Starts by computing the rays originating from the corners of the polygon. 
           Each ray object also stores the coordinates of its neighboring polygon edges (previous and next).'''
        
        lv = len(self.vertices)
        
        for i in range(lv):
            pv = self.vertices[(i-1)%lv]  #previous vertex
            cv = self.vertices[i] #current vertex
            nv = self.vertices[(i+1)%lv] #next vertex
                    
            b = self.bisector(pv, cv, cv, nv)
            ept = b.setMag(100000).add(cv) #end-point of the ray (far from start-point)
            self.rays.append((cv, ept, (pv, cv), (cv, nv))) #start-point, end-point, previous edge, next edge 
            
       
       
    @property            
    def reduce(self):
        
        '''Finds consecutive rays intersecting each other before either intersects its other neighbor. 
           Replaces these pairs of rays by a single one originating from their intersection point and 
           aiming towards the average direction of its neighboring polygon edges.'''
        
        while len(self.rays) > 2:
        
            intersections = [] # Nearest intersection points from parent
            lr = len(self.rays)
        
            for i in xrange(lr):
                pr = self.rays[(i-1)%lr] #previous ray 
                cr = self.rays[i] #current ray
                nr = self.rays[(i+1)%lr] #next ray
                
                mind, X = 100000, None #min-distance, intersection point
                
                for r in (pr, nr):
                    x = self.intersect(cr[0], cr[1], r[0], r[1])
                    if x:
                        d = x.dist(cr[0])
                        if d < mind:
                            mind = d
                            X = x

                intersections.append((X, mind))
            
            candidates = []
            for id, ((X1, d1), (X2, d2)) in enumerate(zip(intersections, intersections[1:]+intersections[:1])): 
                if (X1 and X2) != None and X1 == X2:
                    dsum = d1 + d2 #sum of distances from selected rays (s-pt) to their intersection point
                    candidates.append((id, X1, dsum))
                    
            if not candidates:
                
                #making sure that NO consecutive rays intersect each other before either intersects its other neighbor
                if len(set(intersections)) == len(intersections):
                    for id, ((X1, d1), (X2, d2)) in enumerate(zip(intersections, intersections[1:]+intersections[:1])):
                        if (X1 and X2) != None:
                            
                            #sending to candidates anyway
                            dsum = d1 + d2 #sum of distances from selected rays (s-pt) to their intersection point
                            candidates.append((id, X1, dsum))
        
            srays = sorted(candidates, key=lambda t: t[2]) #rays sorted by distance from their s-pt to their intersection pt
            selectedrays =  [r for r in srays if r[2] == srays[0][2]] #in cases when several rays are equally distant from their intersection pt
            
            if selectedrays:
                offset = 0
                
                for ray in selectedrays:
                    id, X, _ = ray
                    r1 = self.rays[id-offset]
                    r2 = self.rays[(id+1-offset)%lr]
                    
                    #stores bones (segments from parent rays to intersection point 'X')
                    for r in (r1[0], r2[0]):
                        if r not in self.vertices:
                            d1 = X.dist(r1[2][1])
                            d2 = X.dist(r2[3][0])
                            if (d1 + d2) / 2 > self.tol:
                                self.bones.append((r, X))
                            else:
                                self.branches.append((r, X))
                        else:
                            self.branches.append((r, X))
                        

                    #compute direction of the new ray
                    b = self.bisector(r1[2][0], r1[2][1], r2[3][0], r2[3][1]) #s-pt & e-pt of 1st edge, s-pt & e-pt of 2nd edge
                    ept = X.copy().add(b.setMag(100000))
                    
                    #check if ray points in the right direction
                    si = self.vertices.index(r2[3][0]) #s-pt index
                    ei = self.vertices.index(r1[2][1]) #e-pt index
                    slice = self.vertices[si:ei] if ei > si else self.vertices[si:] + self.vertices[:ei]
                    
                    if not self.contain([X] + slice, X.copy().add(b.setMag(1))): 
                        ept.mult(-1)
    
                    #delete parents rays from array list and insert their 'child' instead  
                    self.rays[id-offset] = (X, ept, r1[2], r2[3])
                    del self.rays[(id+1-offset)%lr]
                    offset += 1
                    lr = len(self.rays)
                
            else: 
                print("Error: no rays have been found for reduction. A shared intersection point is probably missing.")
                break
                   
                                
        #connect start-points of the last 2 rays    
        self.bones.append((self.rays[0][0], self.rays[1][0]))
                        
         
         
    def bisector(self, p1, p2, p3, p4):
        
        '''Returns a PVector.
           Computes the bisector of a corner between edge p1-p2 and edge p3-p4.'''
        
        dir1 = (p2 - p1).normalize() #direction between 1st point and 2nd point of edge 1
        dir2 = (p4 - p3).normalize() #direction between 1st point and 2nd point of edge 2

        dsum = dir1 + dir2

        return PVector(dsum.y, -dsum.x).normalize() 
        
        
        
    def intersect(self, p1, p2, p3, p4):
        
        '''Returns a Boolean.
           Checks if 2 lines are intersecting. Option: returns location of intersection point'''
        
        uA = ((p4.x-p3.x)*(p1.y-p3.y) - (p4.y-p3.y)*(p1.x-p3.x)) / ((p4.y-p3.y)*(p2.x-p1.x) - (p4.x-p3.x)*(p2.y-p1.y)) 
        uB = ((p2.x-p1.x)*(p1.y-p3.y) - (p2.y-p1.y)*(p1.x-p3.x)) / ((p4.y-p3.y)*(p2.x-p1.x) - (p4.x-p3.x)*(p2.y-p1.y))
        
        if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
                                            
            secX = p1.x + (uA * (p2.x-p1.x))
            secY = p1.y + (uA * (p2.y-p1.y))
            
            return PVector(round(secX), round(secY))
        
        
        
    def contain(self, verts, pt):
    
        '''Returns a boolean.
           Determine whether a point lies inside a shape/polygon or not.'''
        
        N = len(verts)
        isInside = 0
        
        for i in xrange(N):
            v1 = verts[(i+1)%N]
            v2 = verts[i]
            
            if (v2.y > pt.y) != (v1.y > pt.y):
                if pt.x < (v1.x - v2.x) * (pt.y - v2.y) / (v1.y - v2.y) + v2.x:
                    isInside = not isInside
                    
        return isInside
