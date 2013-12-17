import numpy as np
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier,GradientBoostingClassifier,RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


class Trainer:

    def __init__(self, n=32):
        self.n = n
        self.trainer = AdaBoostClassifier(
            n_estimators=self.n)        
        #self.trainer = AdaBoostClassifier(
        #    n_estimators=self.n)
        # self.trainer = ExtraTreesClassifier(
        #     max_features=self.n, n_estimators=self.n)
        #self.trainer = RandomForestClassifier(
        #    max_features=self.n, n_estimators=10, max_depth=3)
        
    def features(self):
        ### Take self.n best features, or less
        positive = (self.trainer.feature_importances_ > 0).sum()
        if positive > self.n:
            print "Error, to many features contribute to classification", positive

        #print positive

        f = np.array(self.trainer.feature_importances_.argsort()[-positive:][::-1])
        return f 

    def train(self, train, test, weights):
        self.trainer.fit(train, test, sample_weight=weights)
        #self.trainer.fit(train, test)

    def predict(self, data):
        scores = self.trainer.predict_proba(data)[:, 1]
        return scores
