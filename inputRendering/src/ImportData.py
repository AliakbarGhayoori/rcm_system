import pandas as pd

class ImportData():
    def __init__(self, path):
        self.path = path

    def createDF(self):
        strInputs = ['{0:04}'.format(num) for num in range(1, 100)] #because huge computational cost of working with all of data
        # for working with it easier give first 100 of them.
        items = []
        users = []
        ratings = []
        for strInput in strInputs:
            loc = self.path + '/mv_000' + strInput + '.txt'
            with open(loc, 'r') as f:
                doc = f.read().split("\n")
                itemId = int(strInput)
                for i in range(1, len(doc)):
                    rateInfo = doc[i].split(',')
                    if len(rateInfo) < 3:
                        continue
                    userId = int(rateInfo[0])
                    rating = int(rateInfo[1])
                    items += [itemId]
                    users += [userId]
                    ratings += [rating]
        rating_dict = {'itemID': items, 'userID': users, 'rating': ratings}
        df = pd.DataFrame(rating_dict)
        print(df.head())
        return df