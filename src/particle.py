import numpy as np
from numpy import random



# State is represented as a numpy array
### [x, y, w, h, vx, vy, weight]
MAX_velocity = 25




class ParticleFilter():

    def __init__(self, target, count, bounds, SIGMA_size=0.64, SIGMA_velocity=6.4):
        self.count = count
        self.target = np.array(target)
        self.particles = createInitialParticles(self.target, count)
        self.iterations = 0
        self.bounds = bounds
        self.deg = 0
        self.SIGMA_size = SIGMA_size
        self.SIGMA_velocity = SIGMA_velocity
        self.probLambda = 12

    def updateParticles(self):
        # Update positions with velocity
        self.particles[:, 0:2] += self.particles[:, 4:6]
        #np.clip(self.particles[:,0], 0, self.bounds[0], self.particles[:,0])
        #np.clip(self.particles[:,1], 0, self.bounds[1], self.particles[:,1])

        # Add noise to w,h
        if self.SIGMA_size > 0.0001:
            self.particles[:, 2:4] += random.normal(0, self.SIGMA_size, (self.particles.shape[0], 2))
        #np.clip(self.particles[:,2], 1, self.bounds[0], self.particles[:,2])
        #np.clip(self.particles[:,3], 1, self.bounds[1], self.particles[:,3])
        # Add noise to velocities and clip
        self.particles[:, 4:6] += random.normal(
            0, self.SIGMA_velocity, (self.particles.shape[0], 2))
        #np.clip(self.particles[:,4:6], -MAX_velocity,MAX_velocity, self.particles[:,4:6])

        lb = [0, 0, 1, 1, -MAX_velocity, -MAX_velocity, 0]
        ub = [self.bounds[1],
              self.bounds[0],
              self.bounds[1],
              self.bounds[0],
              MAX_velocity,
              MAX_velocity,
              1]
        np.clip(self.particles, lb, ub, self.particles)
        if np.max(self.particles[:, 0]) > self.bounds[1]:
            print "Not clipped"
        self.iterations += 1
        # TODO update weight

    def updateWeights(self, scores):
        # We have to clip the scores so they dont get to big after exponiating.
        # They should be between 0 and 1 regardles...
        np.clip(scores, 0, 1., scores)
        scores = np.exp(self.probLambda * scores)
        total = np.sum(scores)
        self.particles[:, 6] = scores / total
        assert np.abs(np.sum(self.particles[:, 6]) - 1) < 0.1

        N_eff = 1 / np.sum(self.particles[:,6]**2)
        if N_eff < self.count / 10.0:
            self.resample()
            self.particles[:,6] = 1 / float(self.count)
            self.deg += 1
            #print self.deg
            #print "Degenerate, resampling"


        self.target = self.getTrackedObject()

        self.resample()

    def resample(self):
        # Sample acording to weights
        indices = random.choice(
            range(0, self.particles.shape[0]), self.count, p=self.particles[:, 6])
        # Update particles with new samples
        self.particles = self.particles[indices]

    def getTrackedObject(self):
        rect = self.particles[:, 0:4]
        weights = self.particles[:, 6]
        weights = weights[None, :]
        # Calculates weight[i]*(x,y,w,h)[i] and sums it

        # return self.particles[self.particles[:,6].argmax(),:4]
        return np.sum(rect * weights.T, axis=0)



def particleToString(particle):
    return "Weight: {6}, (x:{0}, y:{1}), (w:{2},h:{3}), (vx:{4},vy:{5})".format(*particle)


def createInitialParticles(target, count):
    '''Returns a matrix where each row represents the state of a particle'''
    velocities = random.normal(0, 6.4, (count, 2))

    # Repeat target count times
    targets = np.tile(target, (count, 1))
    # Stack the rectangle, velocities and particle weight
    targets = np.hstack((targets, velocities, np.ones((count, 1)) / count))
    return targets


if __name__ == "__main__":
    pf = ParticleFilter(np.array([10, 10, 5, 5]), 10, (100, 100))
    initial = pf.particles
    print particleToString(initial[0, :])
    print pf.getTrackedObject()
