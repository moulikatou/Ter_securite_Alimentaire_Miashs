import os
import pandas as pd
import numpy as np
import pyreadstat as pt
from simpledbf import Dbf5 

# import matplotlib.pyplot as plt
# import seaborn as sns

DATA_PATH = "TER_M1_MIASHS/donnees/"
ADM_PATH = "TER_M1_MIASHS/limites_adm/"

'''
desc : from a filename 'fichier' (with an ".sav" extension) returns a DataFrame
return : DataFrame
'''
def lire(fichier):
    return pd.read_sas(fichier)

'''
desc : save a dataframe as a CSV file
df : a dataframe to be saved
filename : a string, the path where the file should be saved
'''
def sauver(df, filename):
    return df.to_csv(filename)

'''
desc : concat multiple dataframe, joining the same columns and adding the ones that are different
dfs : a list of DataFrame
return : the concatenation of dfs
'''
def concat(dfs):
    res = dfs[0]
    for i in range(1, len(dfs)):
        res = res.merge(dfs[i], how="outer")
    return res

'''
desc : from a string answer to a question converts it to an int
s : the string represeting the value of the answer
'''
def answer_string2int(s):
    res = np.nan
    if (s == "Jamais"):
        return 0
    
    try:
        value = int(s[:1])
        return value
    except Exception as e:
        return np.nan

'''
desc : compute a csi score
X : a dataframe, answers to all five questions {"a":[0-7], "b":[0-7], "c":[0-7], "d":[0-7], "e":[0-7]}
    to compute the CSI score
return : a float, the computed CSI score
'''
def reduced_csi_score(X):
    csi = pd.DataFrame(columns=["answers", "weight", "weighted_score"])
    csi.answers = X
    csi.weight = [1,2,1,3,1] # les poids de chaque questions

    csi.weighted_score = csi.answers * csi.weight # le score pondere pour chaque question
    # csi.score = csi.weighted_score.sum() # la somme des scores ponderes est le reduced CSI (cf. d-CSI dans la biblio)
    return csi.weighted_score.sum()

'''
desc : from an orginal df (loaded from a .sav file), compute the reduced CSI
       then return the dataframe without useless columns,
       the columns to keep are defined by the parameter cols
df : the original dataframe
og_cols : a dictionnary containing 3 fields : metadata, data and target;
          in each field are mentionned every original columns name
cols : cols should be a dictionnary containing 3 fields : metadata, data and target;
       in each field are mentionned every columns to be renamed,
       those are also the columns that will be kept
return : the reduced dataframe
'''
def compute_dataframe(df):
    # a dictionnary containing 3 fields : metadata, data and target;
    # in each field are mentionned every column name
    metadata_cols = ["REG", "PROV", "COM", "VIL", "MEN", "YEAR"]
    og_cols = ["S62Q1_1", "S62Q1_2", "S62Q1_3", "S62Q1_4", "S62Q1_5"]
    cols = ["Q1","Q2","Q3","Q4","Q5"]

    try:
        df = df.rename(columns={"CODMEN" : "MEN"})
    except Exception as e:
        pass

    print(metadata_cols)
    df[metadata_cols] = df[metadata_cols].astype(int) # convert all columns about location as int

    columns = { og_cols[i] : cols[i] for i in range(len(og_cols)) }
    df = df.rename(columns=columns)
    
    try: # try to reformat string answers to int/float
        for col in cols:
            df[col] = df[col].apply(lambda x : answer_string2int(x))
    except Exception as e:
        pass

    print(df[metadata_cols + cols].head())
    df.CSI = np.nan # initialize target(CSI) column
    # pour chaque MEN (donc chaque ligne) du dataframe on calcule le CSI reduit
    # (cf. la fonction "reduced_csi_score(X)")
    for i in range(df.shape[0]):
        d = df.iloc[i]
        d.CSI = reduced_csi_score(d[cols])
        df.iloc[i] = d

    columns = metadata_cols + cols + ["CSI"]
    print(columns)
    return df.loc[:, columns] # on reduit le dataframe au colonnes voulus

'''
desc : 
'''
def associate_geo_name(df, geo):
    res = pd.DataFrame(columns=df.columns)

    cols_to_keep = ["REG", "PROV", "COM", "VIL", "MEN", "YEAR", "Q1", "Q2", "Q3", "Q4", "Q5", "CSI"]
    og_cols = ["ID_1", "ID_2", "ID_3"]
    cols = ["REG", "PROV", "COM"]

    geo = geo.rename(columns={og_cols[i] : cols[i] for i in range(len(og_cols))})

    for i in range(df.shape[0]):
        d = df.iloc[i]

        old_value, new_value = d.REG, geo[geo.REG == int(d.REG)].iloc[0].REGION
        # print(d, d.iloc[1])
        d.iloc[1] = new_value
        # d.loc[0] = new_value

        res = res.append(d, ignore_index=True)
        print(res.shape)
    print(res.head())

    return res

if __name__ == "__main__":

    new_filename = "reduced_data.csv"
    new_path = DATA_PATH + "formated/"

    raw_data = None
    if (len(os.listdir(new_path)) == 0) :
        for _,_,files in os.walk(DATA_PATH):

            for f in files:
                df = pd.read_spss(DATA_PATH + f)

                annee = f.split('.')[0].split('_')
                annee = int(annee[len(annee)-1][:4])
                df["YEAR"] = annee

                df = compute_dataframe(df)
                filename = "donnees_" + str(annee) + ".csv" # nouveau nom de fichier
                sauver(df, new_path + filename) # on sauvegarde le nouveau dataframe (dans le dossier "formated")

                if raw_data is not None:
                    raw_data = concat([df, raw_data])
                else:
                    raw_data = df

        DATA_PATH = new_path
        sauver(raw_data, DATA_PATH + new_filename)

    elif os.path.isfile(DATA_PATH + new_filename):
        raw_data = pd.read_csv(DATA_PATH + new_filename)

        metadata_cols = ["REG", "PROV", "COM", "VIL", "MEN", "YEAR"]
        raw_data[metadata_cols] = raw_data[metadata_cols].astype(int)

    else :
        for _,_,files in os.walk(new_path):

            for f in files:
                if raw_data is not None:
                    df = pd.read_csv(new_path + f)
                    raw_data = concat([df, raw_data])
                else:
                    raw_data = pd.read_csv(new_path + f)

            raw_data = raw_data.rename(columns={raw_data.columns[0] : "Index"})
            raw_data = raw_data.set_index(raw_data.columns[0])
        sauver(raw_data, DATA_PATH + new_filename)

        metadata_cols = ["REG", "PROV", "COM", "VIL", "MEN", "YEAR"]
        raw_data[metadata_cols] = raw_data[metadata_cols].astype(int)
        sauver(raw_data, DATA_PATH + "reduced_data.csv")

    geo = Dbf5(ADM_PATH + "BFA_adm3.dbf").to_dataframe()
    df = associate_geo_name(raw_data, geo)
    sauver(df, DATA_PATH + "reduced_named_data.csv")
