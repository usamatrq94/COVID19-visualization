import os
import pandas as pd
import numpy as np
import country_converter as coco

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


files = ['confirmed.csv' , 'death.csv', 'recovery.csv']
for file in files:
    const = data_preprocessing(file)
    const.time_rows(const.datasetf)
    const.unique_countries(const.datasetf)
    const.merge_states()
    const.consistent_countries()
    const.consistent_dates()
    const.save_file()

const2 = data_preprocessing('testing.csv')
const2.time_rows(const2.datasetf)
const2.unique_countries(const2.datasetf)
const2.re_dimension_testing()
const2.save_file()
const2.consistent_countries_t()
const2.consistent_dates()
const2.save_file()

class restructuring():
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def Plotly_style(self):
        # Fetching list of all files in output folder
        lst = os.listdir(self.output_folder)
        # Creating a dataframe for confirmed cases
        dfc_path = os.path.join(self.output_folder,lst[0])
        dfc = pd.read_csv(dfc_path)
        # Creating a dataframe for deaths
        dfd_path = os.path.join(self.output_folder,lst[1])
        dfd = pd.read_csv(dfd_path)
        # Creating a dataframe for recovery
        dfr_path = os.path.join(self.output_folder, lst[2])
        dfr = pd.read_csv(dfr_path)
        # Creating a dataframe for testing
        dft_path = os.path.join(self.output_folder, lst[3])
        dft = pd.read_csv(dft_path)
        # Creating an empty dataframe
        restruct = pd.DataFrame()
        # Declaring country
        unique = dfc['Country'].unique()
        for country in unique:
            # Generating slicers
            rowC = dfc[dfc['Country'] == country].drop(columns = 'Country')
            rowD = dfd[dfd['Country'] == country].drop(columns = 'Country')
            rowR = dfr[dfr['Country'] == country].drop(columns = 'Country')
            rowT = dft[dft['Country'] == country].drop(columns = 'Country')
            count = rowT.shape[1]
            rowN = [country for i in range(count)] 
            Con = coco.convert(names=country, to='continent')
            rowCon = [Con for i in range(count)]
            rowTS = []
            ls = rowT.T
            ls.columns = ['Confirmed']
            ls = ls['Confirmed'].tolist()
            rowTS.insert(0, ls[0])
            for x in range(1,len(ls)):
                ans = rowTS[x-1] + ls[x]
                rowTS.append(ans)    
            # Creating a new dataframe
            c = pd.DataFrame(rowC.T)
            d = pd.DataFrame(rowD.T)
            r = pd.DataFrame(rowR.T)
            ts = pd.DataFrame(rowTS)
            ts.set_index(rowC.columns, inplace=True)
            if ts.sum()[0] == 0:
                ts = c
            else:
                ts = ts
            t = pd.DataFrame(rowT.T)
            t.set_index(rowC.columns, inplace=True)
            cons = pd.DataFrame(rowCon)
            cons.set_index(rowC.columns, inplace=True)
            date = pd.DataFrame(rowC.columns)
            date.set_index(rowC.columns, inplace=True)
            n = pd.DataFrame(rowN)
            n = n.set_index(rowC.columns)
            data = pd.concat([n, cons, date, c, d, r, t, ts], axis=1)
            data.columns = ['Country', 'Continent', 'Date', 'Confirmed', 'Deaths', 'Recovery', 'dTesting', 'Testing']
            restruct = pd.concat([restruct, data], axis=0)
        restruct.to_csv(os.path.join(self.output_folder, 'unified.csv'), index=False)

unified = restructuring('./outputs')
unified.Plotly_style()

uni = pd.read_csv('./outputs/unified.csv')
uni['Continent'] = uni['Continent'].replace('not found', 'Cruise Ship')
uni.to_csv('./outputs/unified.csv')