from numpy import NaN
import pandas as pd
import csv

dataPath = "../data"
trainPath = dataPath+"train.csv"
sortedPath = dataPath+"newtrain.csv"
remainPath = dataPath+"remainEmployees.csv"
leftPath = dataPath+"leftEmployees.csv"

# testdata = pd.read_csv(testpath)
traindata = pd.read_csv(trainPath)
data = traindata.sort_values(by=["PerStatus"])

# 去掉最高學歷, 畢業學校類別, 畢業科系類別
data = data.drop(columns=['最高學歷', '畢業學校類別', '畢業科系類別'])

# 清除缺失員工資料
row_drop_idx = []
for i in range(0,data.shape[0]):
    empty_col_count = [data.isnull().loc[i]][0].value_counts()
    if (empty_col_count.loc[False]<44):
        row_drop_idx.append(i)
data.drop(axis=0, index=row_drop_idx, inplace=True)

remainData = data[data["PerStatus"]==1].sort_values(by=["yyyy","PerNo"], ascending=True)
leftData = data[data["PerStatus"]==0].sort_values(by=["yyyy","PerNo"], ascending=True)



# in_ = input("1:1 重組 離職員工 與 留職員工? Y/n")
# if(in_.lower() == "y" or in_.lower() == ""):
#     randomize()

remainData.to_csv(remainPath, index=False, header=remainData.columns)
leftData.to_csv(leftPath, index=False, header=leftData.columns)

print("Data cleanup done! Output files in " + remainPath + " and " + leftPath)