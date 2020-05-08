import os
import pandas as pd
import numpy as np

class data_preprocessing():
    
    def __init__(self, filename):
        self.filename = filename
        self.datasetf = './dataset'
        self.outputf = './outputs'
        self.path = os.path.join(self.datasetf,filename)
        self.dataset = pd.read_csv(self.path)

    def merge_states(self):
        datafr = self.dataset
        new_dict = []
        for country in self.unique:
            c_data = datafr[datafr['Country/Region'] == country].sum(axis=0)
            new_dict.append(c_data)
        d = pd.DataFrame(new_dict)
        d = d.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis = 1)
        unique = pd.DataFrame(self.unique, columns = ['Country'])
        dataset = pd.concat([unique, d], axis = 1)
        self.dataset = dataset

    def re_dimension_testing(self):
        filepath = './dataset/testing.csv'
        d = pd.read_csv(filepath)
        unique = d['location'].unique()
        dicts = []
        for country in unique:
            count = d[d['location'] == country].count()[2]
            new_dict = { 'Country' : country, 'Counts' : count}
            dicts.append(new_dict)
        data = pd.DataFrame(dicts)
        slicer = data[data['Counts'] == data['Counts'].max()]
        cols = d[d['location'] == slicer.iloc[0][0]]['date'].to_list()
        reframe = pd.DataFrame(columns = [cols])
        n=0
        for country in unique:
            zeros = len(cols) - d[d['location'] == country]['date'].count()
            testing = d[d['location'] == country]['new_tests']
            row = []
            for x in range(0,zeros):
                row.append(0)
            row.extend(testing)
            reframe.loc[n] = row
            n = n + 1
        unique = pd.DataFrame(unique, columns = ['Country'])
        reframe = pd.concat([unique,reframe], axis = 1)
        cols.insert(0, "Country")
        reframe.columns = [cols]
        reframe.fillna(0, inplace=True)
        self.dataset = reframe
        
    def consistent_countries_t(self):
        dataset = pd.read_csv('./outputs/testing.csv')
        unique = pd.DataFrame(self.unique)
        unique.columns = ['Country']
        df3 = pd.merge(unique, dataset, on='Country', how = 'left')
        df3.fillna(0, inplace=True)
        self.dataset = df3
        
    def consistent_countries(self):
        dataFr = self.dataset
        unique = pd.DataFrame(self.unique)
        unique.columns = ['Country']
        df3 = pd.merge(unique, dataFr, on='Country', how = 'left')
        self.dataset = df3 
        
    def consistent_dates(self):
        data = self.dataset
        data.iloc[:,((self.row-1)*-1):-1]
        data.iloc[:,0]
        tes = pd.concat([data.iloc[:,0], data.iloc[:,((self.row-1)*-1):-1]], axis=1)
        self.dataset = tes

    def save_file(self):
        save_path = os.path.join(self.outputf,self.filename)
        dataset = pd.DataFrame(self.dataset)
        dataset.to_csv(save_path, index=False)
        
    @classmethod
    def time_rows(cls, datasetf):
        files = os.listdir(datasetf)
        row = []
        for file in files:
            dat = pd.read_csv(os.path.join(datasetf, file))
            row.append(dat.shape[1])
        data_preprocessing.row = np.array(row)[0] - 3
        
    @classmethod
    def unique_countries(cls, datasetf):
        lst = os.listdir(datasetf)
        arr = []
        for file in lst:
            arr.append(pd.read_csv(os.path.join(datasetf,file)).shape[0])
        result = {'File' : lst , 'Counts': arr}
        result = pd.DataFrame(result)
        file = result[result['Counts'] == result['Counts'].min()].iloc[0][0]
        unique = pd.read_csv(os.path.join(datasetf,file))['Country/Region'].unique()
        data_preprocessing.unique = unique

const2 = data_preprocessing('testing.csv')
const2.time_rows(const2.datasetf)
const2.unique_countries(const2.datasetf)
const2.re_dimension_testing()
const2.save_file()
const2.consistent_countries_t()
const2.consistent_dates()
const2.save_file()

files = ['confirmed.csv' , 'death.csv', 'recovery.csv']

for file in files:
    const = data_preprocessing(file)
    const.time_rows(const.datasetf)
    const.unique_countries(const.datasetf)
    const.merge_states()
    const.consistent_countries()
    const.consistent_dates()
    const.save_file()