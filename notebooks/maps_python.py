import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd

path = "../TER_M1_MIASHS/"

# import polygones des régions
gpd_Map_reg = gpd.read_file(path + 'limites_adm/BFA_adm2.shp')
# on retire les métadonnées inutiles
gpd_Map_reg = gpd_Map_reg[['REGION', 'PROVINCE', 'geometry']]

# import données CSI
data_epa_csi = pd.read_csv(path + "donnees/reduced_data.csv")
# on retire les variables inutiles pour la carte
data_epa_csi = data_epa_csi[['REGION', 'PROVINCE', 'CSI']]

# import fichier noms
data_com = pd.read_excel(path + "donnees/village_rural.xlsx", engine="openpyxl")

### ajout des noms des zones
#regroupement liste adm par communes
data_com=data_com.groupby(['REGION','PROVINCE']).agg({'region1':"first", 'province1':"first"}).reset_index()
#regroupement zones de ouaga -> ouaga
data_com=data_com.apply(pd.Series.replace, to_replace="OUAGADOUGOU-BOGODOGO", value="OUAGADOUGOU")
data_com=data_com.apply(pd.Series.replace, to_replace="OUAGADOUGOU-BOULMIOU", value="OUAGADOUGOU")
data_com=data_com.apply(pd.Series.replace, to_replace="OUAGADOUGOU-NONGREMA", value="OUAGADOUGOU")
data_com=data_com.apply(pd.Series.replace, to_replace="OUAGADOUGOU- SIG-NON", value="OUAGADOUGOU")

# on merge les données csi sans noms avec le fichier des noms
data_epa_csi = pd.merge(data_epa_csi, data_com, how='left', on=['REGION', 'PROVINCE'])

# on retire les codes des zones dont on n'a plus besoin
data_epa_csi = data_epa_csi[['region1', 'province1', 'CSI']]
data_epa_csi = data_epa_csi.rename(columns={'region1':'REGION','province1':'PROVINCE'})

# variables nécessaires pour la spatialisation du CSI
crs = {'init':'epsg:6326'}
geometry = 'geometry'

# on regroupe le CSI par régions
epa_csi_group = data_epa_csi.groupby(['REGION', 'PROVINCE']).agg({'CSI': "mean"}).reset_index()

# on merge ("recole") les données CSI avec les polygones
epa_csi_merge = pd.merge(epa_csi_group, gpd_Map_reg, how='left', on=['REGION', 'PROVINCE'])

# on spatialise en transformant en objet geopandas
geo_epa_csi_merge = gpd.GeoDataFrame(epa_csi_merge, crs=crs, geometry=geometry)

### on créé la carte
data = geo_epa_csi_merge
var = 'CSI'
# nécessaire pour la légende
v = mpatches.Patch(color='#ff8b73', label='3ème tercile (rCSI critique)')
j = mpatches.Patch(color='#fcdf79', label='2ème tercile (rCSI limite)')
r = mpatches.Patch(color='#b4f05d', label='1er tercile (rCSI acceptable)')

fig, ax = plt.subplots(figsize=(15,15)) # taille de la carte
data.plot(ax=ax, linewidth=1, edgecolor='black')
# on discrétise le CSI (ici en 3 classes de même fréquence = terctiles)
data[data[var] <= data[var].quantile(0.33)].plot(ax=ax, color='#b4f05d')
data[(data[var] > data[var].quantile(0.33)) & (data[var] <= data[var].quantile(0.66))].plot(ax=ax, color='#fcdf79')
data[data[var] > data[var].quantile(0.66)].plot(ax=ax, color='#ff8b73')
# on ajoute les étiquettes
data.apply(lambda x: ax.annotate(s=x.PROVINCE+" ("+str(round(x.CSI, 2))+")", xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
# on ajoute la légende
plt.legend(loc="best", prop={'size': 12}, handles=[r, j, v])
ax.axis('off')
plt.savefig('./pictures/map_csi_province.png') # on exporte
