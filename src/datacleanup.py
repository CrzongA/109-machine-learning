from numpy import NaN
import pandas as pd
import csv

dataPath = "../data/"
outputPath = "out/"
trainPath = dataPath + "train.csv"
sortedPath = dataPath + outputPath + "newtrain.csv"
remainPath = dataPath + outputPath + "remainEmployees.csv"
leftPath = dataPath + outputPath + "leftEmployees.csv"
year_2014_2016_path = dataPath + outputPath + "data_2014-2016.csv"
year_2015_2017_path = dataPath + outputPath + "data_2015-2017.csv"

print("Running...")

# testdata = pd.read_csv(testpath)
traindata = pd.read_csv(trainPath)
data = traindata.sort_values(by=["PerStatus"])

# 去掉最高學歷, 畢業學校類別, 畢業科系類別
data = data.drop(columns=['最高學歷', '畢業學校類別', '畢業科系類別'])
headers = ["PerNo","yyyy","PerStatus","sex","工作分類","職等","廠區代碼","管理層級","工作資歷1","工作資歷2","工作資歷3","工作資歷4","工作資歷5","專案時數","專案總數","當前專案角色","特殊專案佔比","工作地點","訓練時數A","訓練時數B","訓練時數C","生產總額","榮譽數","是否升遷","升遷速度","近三月請假數A","近一年請假數A","近三月請假數B","近一年請假數B","出差數A","出差數B","出差集中度","年度績效等級A","年度績效等級B","年度績效等級C","年齡層級","婚姻狀況","年資層級A","年資層級B","年資層級C","任職前工作平均年數","眷屬量","通勤成本","歸屬部門"]
data = data[headers]

# 清除缺失員工資料
row_drop_idx = []
for i in range(0,data.shape[0]):
    empty_col_count = [data.isnull().loc[i]][0].value_counts()
    if (empty_col_count.loc[False]<44):
        row_drop_idx.append(i)
data.drop(axis=0, index=row_drop_idx, inplace=True)


byPerNoData = data.copy(deep=True).sort_values(by=["PerNo"], ascending=True)
remainData = data.copy(deep=False)[data["PerStatus"]==1].sort_values(by=["yyyy","PerNo"], ascending=True)
leftData = data.copy(deep=False)[data["PerStatus"]==0].sort_values(by=["yyyy","PerNo"], ascending=True)

# 合併三年資料
data_2014 = byPerNoData[byPerNoData["yyyy"]==2014.0]
data_2015 = byPerNoData[byPerNoData["yyyy"]==2015.0]
data_2016 = byPerNoData[byPerNoData["yyyy"]==2016.0]
data_2017 = byPerNoData[byPerNoData["yyyy"]==2017.0]
data_2014_2016 = data_2014.copy(deep=True).merge(data_2015, how='inner', on='PerNo', suffixes=["_1", "_2"]).merge(data_2016, how='inner', on='PerNo', suffixes=["", "_3"])
data_2015_2017 = data_2015.copy(deep=True).merge(data_2016, how='inner', on='PerNo', suffixes=["_1", "_2"]).merge(data_2017, how='inner', on='PerNo', suffixes=["", "_3"])
# for i in range (0, data.shape[0]):
#     if 
# byPerNoHeaders = 

# in_ = input("1:1 重組 離職員工 與 留職員工? Y/n")
# if(in_.lower() == "y" or in_.lower() == ""):
#     randomize()

data_2014_2016.to_csv(year_2014_2016_path, index=False, header=data_2014_2016.columns)
data_2015_2017.to_csv(year_2015_2017_path, index=False, header=data_2015_2017.columns)
remainData.to_csv(remainPath, index=False, header=remainData.columns)
leftData.to_csv(leftPath, index=False, header=leftData.columns)

print("Data cleanup done!\n" +  "Output files: "
 + remainPath + ", " 
 + leftPath + ", " 
 + year_2014_2016_path + ", " 
 + year_2015_2017_path)