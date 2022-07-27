import csv
import numpy
import scipy.stats as stats
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from math import *

FILENAME = 'crime_boston.csv'
DELIMITER = ';'
ENCODING = 'utf-8'
FILTERED_HEADERS = ['col', 'atm']
FILTERED_VALUES = ['-1']
MAX_PIE_CHART_VALUES = 4
MAX_HISTOGRAM_VALUES = 10
COLOR_MAP = ["#377eb8", '#00ff44',
             "#ff7f00","#4daf4a",
             "#f781bf", "#a65628",
             "#984ea3", '#e41a1c',  "#dede00"]

def dataToColumn(data, index):
    res = []
    for line in data:
        res.append(line[index])
    return res

def convertToNumeric(data):
    errors = 0
    res = []
    for d in data:
        try:
            res.append(int(d)) #quali discret
        except:
            try:
                res.append(float(d.replace(',', '.'))) #quali continu
            except:
                errors += 1

    if errors == 0:
        for i in range(len(data)):
            data[i] = res[i]
        return True
    else:
        return False

def convertToHistogram(data):
    histo = {}
    for d in data:
        if d in histo:
            histo[d] += 1
        else:
            histo[d] = 1
    return histo

class UnivariateStats:
    def __init__(self, header, data):
        self.header = header

        if self.header in FILTERED_HEADERS:
            data = list(filter(lambda x: x not in FILTERED_VALUES, data))
        
        self.isNumeric = convertToNumeric(data)
        self.raw = data
        self.histo = convertToHistogram(data)

        if self.isNumeric:
            self.skew = stats.skew(self.raw)
            self.kurtosis = stats.kurtosis(self.raw)

    def __repr__(self):
        res = self.header
        
        nbValues = len(self.histo)
        res += f'\n\t{nbValues} values'
        if nbValues == len(self.raw):
            res += f'\n\tINDEX'
        elif nbValues > 1:
            res += f'\n\t{min(self.raw)} ... {max(self.raw)}'
        else:
            res += f'\n\t{self.raw[0]}'

        if self.isNumeric:
            res += f'\n\t[S:{self.skew:.1f} K:{self.kurtosis:.1f}]'
        return res

    def showHistogram(self):
        plt.hist(self.raw, density=True, bins=len(self.histo))
        plt.title(self.header)
        plt.show()

    def showPieChart(self):
        values = self.histo.values()
        labels = list(self.histo.keys())
        plt.pie(values, labels=labels, autopct='%4.2f%%', shadow=True)
        plt.show()        

if __name__ == '__main__':
    data = []
    with open(FILENAME, encoding=ENCODING) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=DELIMITER)
        headers = reader.fieldnames

        for row in reader:
            data.append([])
            for header in row:
                data[-1].append(row[header].strip())

    print(headers)
    #data = data[:100]    
    #print(data)

    #Display data shape
    print(f'{len(data)} lines x {len(headers)} variables')

    columns = {}
    for i in range(len(headers)):
        column = UnivariateStats(headers[i], dataToColumn(data, i))
        columns[headers[i]] = column
        print(f'{i+1} - {column}')

    #columns['lum'].showPieChart()
    axSize = ceil(sqrt(len(headers)))
    fig, axes = plt.subplots(axSize, axSize)

    #Draw all histograms
    i, j = 0, 0
    for header in columns:
        if len(columns[header].histo) <= MAX_HISTOGRAM_VALUES:
            axes[i, j].set_title(header)

            if len(columns[header].histo) <= MAX_PIE_CHART_VALUES:
                values = columns[header].histo.values()
                labels = columns[header].histo.keys()
                axes[i, j].pie(values, labels=labels, autopct='%4.2f%%')
            else:
                axes[i, j].hist(columns[header].raw, density=True, bins=range(len(columns[header].histo) + 1),
                                rwidth=0.8)
                
            i += 1
            if i >= axSize:
                i = 0
                j += 1

    plt.show()

    def maping():
        #Clustering demo
        long = columns['Long'].raw
        lat = columns['Lat'].raw
        long = list(filter(lambda x : x != 0, long))
        lat = list(filter(lambda x : x != 0, lat))
        
        data = numpy.array(list(map(lambda i: [long[i], lat[i]], range(len(long)))))

        data = data[:20000]

        #clustering = DBSCAN().fit(data)
        #print(clustering.labels_)
        #print(clustering.n_features_in_)

        #colors = list(map(lambda x : COLOR_MAP[x % len(COLOR_MAP)], clustering.labels_))   

        colors = list(map(lambda x : COLOR_MAP[x % len(COLOR_MAP)], columns['OFFENSE_DESCRIPTION']))

        fig, ax = plt.subplots()
        ax.scatter(data[:,0], data[:,-1], color=colors,s=0.2)
        plt.show()
            
    maping()
