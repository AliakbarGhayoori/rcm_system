from surprise import prediction_algorithms
from surprise.model_selection.split import train_test_split
from surprise.model_selection import cross_validate


class PredictionModel:
    def __init__(self, collabDF, userDf= None, itemDf = None):
        self.collabDf = collabDF
        self.userDf = userDf
        self.itemDf = itemDf

        self.reader = Reader(rating_scale=(1,5))
        print(collabDF.head())
        self.dataTuning = Dataset.load_from_df(collabDF, self.reader)

    def randomNormalPred(self):
        pred = prediction_algorithms.random_pred.NormalPredictor()
        return pred

    def baseLinePred(self):
        pred = prediction_algorithms.baseline_only.BaselineOnly()
        return pred


    def isInt(self, str):
        return (str.startswith('-') and str[1:].isdigit()) or (str.isdigit())

    def knnGetInput(self):
        k = input("enter your ideal positive k, (leave blank : k=40): ")
        if self.isInt(k):
            k = int(k)
        elif k == '':
            k = 40
        else:
            while not self.isInt(k):
                k = input("please enter valid input, (leave blank : k=40): ")
                if k == '':
                    k=40
            k = int(k)

        min_k = input("enter your ideal positive min_k, min_k should be lower than k (leave blank : min_k=1): ")
        if self.isInt(min_k):
            min_k = int(min_k)
        elif min_k == '':
            min_k = 40
        else:
            while not self.isInt(min_k):
                min_k = input("please enter valid input, (leave blank : min_k=1): ")
                if min_k == '':
                    min_k=40
            min_k = int(min_k)

        sim = input("choose your ideal similarity option between cosine/msd/pearson/pearson_baseline (default similarity is msd): ")
        if not sim=='cosine' or sim=='msd' or sim=='pearson' or sim=='pearson_baseline':
            sim = 'msd'
        user_based= input("user_based or item_based? (u/i)")
        if user_based=='i':
            user_based=False
        else:
            user_based=True
        shrinkage = input("shrinkage(default:100): ")
        if self.isInt(shrinkage):
            shrinkage = int(shrinkage)
        else:
            shrinkage = 100

        return self.knnPred({'name':sim, 'user_based':user_based, 'shrinkage': shrinkage}, k, min_k)

    def slopeOne(self):
        pred = prediction_algorithms.slope_one.SlopeOne()
        return pred


    def coCluster(self):
        pred = prediction_algorithms.co_clustering.CoClustering(verbose= True)
        return pred

    def knnPred(self,sim_options, k = 40, min_k= 1):
        pred = prediction_algorithms.knns.KNNBasic(k=k, min_k=min_k, sim_options= sim_options)
        return pred

    def SVDMatrixFact(self, n_factors = 100, n_epochs = 20, biased = True, init_mean = 0, init_std = 0.1, lr = 0.05, reg = 0.02):
        pred = prediction_algorithms.matrix_factorization.SVD(n_factors=n_factors, n_epochs=n_epochs, biased=biased,
                                                              init_mean=init_mean, init_std_dev= init_std, lr_all = lr, reg_all = reg)
        return pred


    def SVDPPMatrixFact(self, n_factors = 100, n_epochs = 20, biased = True, init_mean = 0, init_std = 0.1, lr = 0.05, reg = 0.02):
        pred = prediction_algorithms.matrix_factorization.SVDpp(n_factors=n_factors, n_epochs=n_epochs, biased=biased,
                                                              init_mean=init_mean, init_std_dev= init_std, lr_all = lr, reg_all = reg)
        return pred


    def primaryTest(self, predictor):

        trainSet, testset = train_test_split(self.dataTuning, test_size=0.2)
        prediction = predictor.fit(trainSet).test(testset)
        result = pd.DataFrame(prediction, columns=['user_id', 'item_id', 'base_event', 'predict_event', 'details'])
        result.drop(columns={'details'}, inplace=True)
        result['error'] = abs(result['base_event'] - result['predict_event'])
        cross_validate(predictor, self.dataTuning, measures=['RMSE', 'MAE'], cv=5, verbose=True)
        print(result.head())
