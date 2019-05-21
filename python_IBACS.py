#cd '/Users/luishenryquiroganunez/Documents/Familia/Katherin/tesis'
##########################################################################################
#Libraries
##########################################################################################
import numpy as np
from math import *
import sys
import re
import csv
from collections import OrderedDict
import pandas as pd
import folium
from geopy.geocoders import Nominatim
import collections
##########################################################################################
#Functions
##########################################################################################
def read_txt(filename):
    data=[]
    f = open(filename, "r")
    for x in f:
        data.append(x)
    return data    

def no_t(line):
    element=line.find('\t')
    return element    
  
def pos_n(line):
    element=line.find('\n')
    return element 
    
def is_spe_col(col,special_col):     
    if col in special_col:
        a=True
    else:
        a=False
    return a    
def extract_ref(dd):
    pp=dd.find('.')
    return(Ipsg[i][0:pp])    
##########################################################################################
#Reading columns
##########################################################################################    
filename='/Users/luishenryquiroganunez/Documents/Familia/Katherin/tesis/data/ArtistasMasivos.txt'    
data=read_txt(filename)
columns=[]
for i in range(45):
    line=data[i]
    t=no_t(line)
    if (t!=-1):
        #n=pos_n(line)
        columns.append(line[0:t])
#Special comulns with data in the next line
special_col=['Medium/Technique','Description','* Material','* Color','Artist']
#Posible second line after special_col
special_col2=['Description','* Material','* Color','Author']
##########################################################################################
#Reading data and clasifiyng 
##########################################################################################              
data_out=OrderedDict()                
for i in range(len(columns)):
    data_out[columns[i]]=[]

for i in range(len(data)):
    line=data[i]
    t=no_t(line)
    n=pos_n(line)                            
    if (t!=-1):
        col=line[0:t]        
        spec=is_spe_col(col,special_col)
        if (spec==True ):
            dummy_line=data[i+1]
            #dummy_t=no_t(dummy_line)
            dummy_n=pos_n(dummy_line)
            datos=dummy_line[0:dummy_n]
            nodat=is_spe_col(datos,special_col2)
            if nodat==True:
                datos=''
            data_out[col].append(datos)
        else:
            dato=line[t+1:n]
            data_out[col].append(dato)

#Erasing incomplete and unuseful columns
#aa=data_out.keys()
#for i in range(len(data_out)):
#    print (len(data_out[aa[i]]))   
inc_col=[ 'State of Signature', 'Position Signature', 'Marking Text', 'Marking Location']
for i in inc_col:
    data_out.pop(i, None)  
#Test for doube check
#refs=data_out['Ipsg Reference']
#print [item for item, count in collections.Counter(refs).items() if count > 1]
##########################################################################################
#Expoting to csv/SPSS
##########################################################################################                  
#df = pd.DataFrame.from_dict(data_out, orient='index').T.to_csv('interpol_art4.csv', index=False)          
##########################################################################################
########################################################################################## 
#Organizing data by art robbery
########################################################################################## 
keyys=data_out.keys()
Ipsg = data_out['Ipsg Reference']
cas=[]
for i in range(len(Ipsg)):
    dd=Ipsg[i]
    pp=dd.find('.')
    cas.append(Ipsg[i][0:pp])

cases=list(dict.fromkeys(cas)) 
counter=collections.Counter(cas)
cases=counter.keys()

robberies=[]

cases_bis=[]              
for i in range(len(Ipsg)):
    aa=extract_ref(data_out['Ipsg Reference'][i])
    bbb=2#condition for 3 (insert 2) or 2(insert 1) stolen objects of more
    if counter[aa] >bbb:
        kk= aa in cases_bis
        if kk is False:
            cases_bis.append(aa)    
            point = {keyys[0]:data_out[keyys[0]][i],keyys[1]:data_out[keyys[1]][i],keyys[2]:data_out[keyys[2]][i],\
                    keyys[3]:data_out[keyys[3]][i],keyys[4]:data_out[keyys[4]][i],keyys[5]:data_out[keyys[5]][i],\
                    keyys[6]:data_out[keyys[6]][i],keyys[7]:data_out[keyys[7]][i],keyys[8]:data_out[keyys[8]][i],\
                    keyys[9]:data_out[keyys[9]][i],keyys[10]:data_out[keyys[10]][i],keyys[11]:data_out[keyys[11]][i],\
                    keyys[12]:data_out[keyys[12]][i],keyys[13]:data_out[keyys[13]][i],keyys[14]:data_out[keyys[14]][i],\
                    keyys[15]:data_out[keyys[15]][i],keyys[16]:data_out[keyys[16]][i],keyys[17]:data_out[keyys[17]][i],\
                    keyys[18]:data_out[keyys[18]][i],keyys[19]:data_out[keyys[19]][i],keyys[20]:data_out[keyys[20]][i],\
                    keyys[21]:data_out[keyys[21]][i],keyys[22]:data_out[keyys[22]][i],keyys[23]:data_out[keyys[23]][i],\
                    keyys[24]:data_out[keyys[24]][i],keyys[25]:data_out[keyys[25]][i],'Number of Objects':counter[aa]}
            robberies.append(point)  
#Saving csv files        
keyys.append('Number of Objects')

dic = OrderedDict() 
for i in range(len(keyys)):
    dic[keyys[i]]=[]

for i in range(len(robberies)):
    for j in range(len(robberies[i])):
        aa=str(robberies[i][keyys[j]])
        bb=aa.find("/")
        if bb==-1:
            dic[keyys[j]].append(robberies[i][keyys[j]])
        else:
            cc=aa.replace(',', '--')
            dic[keyys[j]].append(cc)            
        
num_objects=dic['Number of Objects']
print('Number of large-scale thefts: %s robberies' %(len(robberies)))
print('Number of objects stolen in robberies with more than %s objects: %s objects' %(bbb+1,sum(num_objects)))
#df = pd.DataFrame.from_dict(dic, orient='index').T.to_csv('large_scale_art_thefts_3objs.csv', index=False)          
##########################################################################################  
#                                   STARTING PLOTS!                                      #
##########################################################################################  
#Plot evolution in time
########################################################################################## 
Ipsg =[ robberies[i]['Ipsg Reference'] for i in range(len(robberies))]
#Ipsg = data_out['Ipsg Reference']
cas=[]
for i in range(len(Ipsg)):
    dd=Ipsg[i]
    pp=dd.find('.')
    cas.append(Ipsg[i][0:pp])

cases=list(dict.fromkeys(cas))    
c_2009=[]
c_2010=[]
c_2011=[]
c_2012=[]
c_2013=[]
c_2014=[]
c_2015=[]
c_2016=[]
c_2017=[]
c_2018=[]
c_2019=[]

for i in range(len(cases)):    
    yr=int(cases[i][0:4])
    if yr == 2009 or yr==1993:
        c_2009.append(cases[i])
    elif yr == 2010:
        c_2010.append(cases[i])
    elif yr == 2011:
        c_2011.append(cases[i])        
    elif yr == 2012:
        c_2012.append(cases[i])
    elif yr == 2013:
        c_2013.append(cases[i])
    elif yr == 2014:
        c_2014.append(cases[i])
    elif yr == 2015:
        c_2015.append(cases[i])        
    elif yr == 2016:
        c_2016.append(cases[i])        
    elif yr == 2017:
        c_2017.append(cases[i])                
    elif yr == 2018:
        c_2018.append(cases[i])                
    elif yr == 2019:
        c_2019.append(cases[i])                
    else:
        print(i)
        print('Algo anda mal...')

#len(c_2014)+len(c_2015)+len(c_2016)+len(c_2017)+len(c_2018)+len(c_2019)                
cases_yrs=[2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
cases_value=[len(c_2009),len(c_2010),len(c_2011),len(c_2012),len(c_2013),len(c_2014),len(c_2015),len(c_2016),len(c_2017),len(c_2018)]

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(cases_value)):
    ax2.text(cases_yrs[i], cases_value[i]+1, str(cases_value[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')    
#title("Radial density distribution of masers")
ax2.bar(cases_yrs,cases_value,align='center', alpha=1.0)
ax2.set_xticks([2009,2010,2011,2012,2013,2014,2015,2016,2017,2018])
ax2.set_xlabel('Year')
ax2.set_ylabel('Large-Scale Art Thefts') 
#ax2.set_ylim([0,70])
name_plot_2="plots/histogram_art_thefts_2009-2018_2.pdf"
#plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Worldmap by cities
##########################################################################################                  
cities =[ robberies[i]['City'] for i in range(len(robberies))]
new_cities=[]
for i in range(len(cities)):
    aa=cities[i]
    aa=aa.upper()
    pp=aa.find('/')    
    if pp >0:
        new_cities.append(aa[0:pp])
    else:
        new_cities.append(aa)
        
#Remove cities that were bad-spelling or non-understandable and add them back manually    
#Remove
zz=new_cities.count('')
for i in range(zz):      
    new_cities.remove('')    
new_cities.remove('BIVERS')
#new_cities.remove('ILLEGIO - TOLMEZZO (UD)') #For 2 objects only (i.e., 435 robberies)
#new_cities.remove('WARSAW - CRACOW') #For 2 objects only (i.e., 435 robberies)
new_cities.remove('CRACOW')
new_cities.remove('PONTASSIEVE - DOCCIA (FI)')
new_cities.remove('LONS LE SAULNIER')
#new_cities.remove('ORRFORS')#For 2 objects only (i.e., 435 robberies)
new_cities.remove('ZELESNICE')
#new_cities.remove('LESNIOWO')#For 2 objects only (i.e., 435 robberies)
new_cities.remove('BRE\xc5\xbdICE')
new_cities.remove('LA D\xc3\x89FENSE')
#Append
#new_cities.append('TOLMEZZO')
#new_cities.append('WARSAW')
new_cities.append('KRAKOW')
new_cities.append('PONTASSIEVE')
new_cities.append('LONS-LE-SAUNIER')
#new_cities.append('ORREFORS')
new_cities.append('ZELEZNICE')
#new_cities.append('LESNIEWO')
new_cities.append('BREZICE')
new_cities.append('LA DEFENSE')

counter=collections.Counter(new_cities)
citi=counter.keys()

geolocator = Nominatim(user_agent="Netscape",timeout=300)

info=['lat','lon','name']
map_out=OrderedDict()                
for i in range(len(info)):
    map_out[info[i]]=[]    

for i in range(len(citi)):
    location = geolocator.geocode(citi[i])#,timeout=None)    
    map_out['lat'].append(location.longitude)    
    map_out['lon'].append(location.latitude)
    names=citi[i]+':'+str(counter[citi[i]])
    map_out['name'].append(names)
                
datan = pd.DataFrame(data=map_out)
m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)
for i in range(0,len(datan)):
    folium.Marker([datan.iloc[i]['lon'], datan.iloc[i]['lat']], popup=datan.iloc[i]['name']).add_to(m)
    #folium.Marker([datan.iloc[i]['lon'], datan.iloc[i]['lat']]).add_to(m)
m.save('plots/art_map_cities_final2_2.html')   

##########################################################################################
#Histograms by cities
##########################################################################################     
top_citi=[]
for i in citi:
    aa=counter[i]
    if aa>2:
        top_citi.append([i,aa])

top_cities=sorted(top_citi,key=lambda l:l[1], reverse=True)        
tpcity=np.array([ top_cities[i][0] for i in range(len(top_cities))])
tprob=[ top_cities[i][1] for i in range(len(top_cities))]
x=np.arange(len(tpcity))

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    #if i<4:
    ax2.text(x[i], tprob[i]+1, tpcity[i], color='k',
            rotation=90,
            horizontalalignment='center',
            verticalalignment='bottom',
            multialignment='center')
#title("Radial density distribution of masers")
ax2.bar(x,tprob,color='b',align='center', alpha=1.0)
ax2.set_xlabel('City')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,30])
name_plot_2="histogram_art_thefts_cities.pdf"
#plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Worldmap countries
##########################################################################################  
countries =[ robberies[i]['Country'] for i in range(len(robberies))]
zz=countries.count('Former Yugoslav Republic of Macedonia')
kk=countries.count('United States')
for i in range(zz):
    countries.remove('Former Yugoslav Republic of Macedonia')    
    countries.append('Macedonia') 
for i in range(kk):      
    countries.remove('United States')    
    countries.append('United States of America') 

counter=collections.Counter(countries)

#somedict = dict(raymond='red', rachel='blue', matthew='green')
with open('mycsvfile2.csv','wb') as f:
    w = csv.writer(f)
    w.writerows(counter.items())
    
#Go to datawrapper
'''
map_data = pd.DataFrame({
    'A3':counter.keys(),
    'value':counter.values()})
m = folium.Map(location=[100, 0], zoom_start=1.5)

country_geo = 'countries-land-10km.geo'

m.choropleth(
    #geo_data = 'https://github.com/simonepri/geo-maps/releases/download/v0.6.0/countries-land-10km.geo.json',
    geo_data = country_geo,
    data = map_data,
    columns = ['A3', 'value'],
    key_on = 'feature.properties.A3',
    fill_color = 'YlOrRd'
) 
m.save('art_map_countries2.html')   
'''

##########################################################################################
#Histograms by countries
##########################################################################################     
new_countries =[ robberies[i]['Country'] for i in range(len(robberies))]        
zz=new_countries.count('Former Yugoslav Republic of Macedonia')
for i in range(zz):
    new_countries.remove('Former Yugoslav Republic of Macedonia')    
    new_countries.append('Macedonia') 
counter=collections.Counter(new_countries)
countres=counter.keys()

top_countries=[]
for i in countres:
    aa=counter[i]
    if aa>2:
        top_countries.append([i,aa])


top_countes=sorted(top_countries,key=lambda l:l[1], reverse=True)        
tpcountes=np.array([ top_countes[i][0] for i in range(len(top_countries))])
tprob_countes=[ top_countes[i][1] for i in range(len(top_countries))]
x=np.arange(len(tpcountes))

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    ax2.text(x[i], tprob_countes[i]+1, str(tprob_countes[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')
ax2.bar(x,tprob_countes,color='b',align='center', alpha=1.0)
ax2.set_xlabel('Country')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,60])
plt.xticks(x, tpcountes)
plt.xticks(rotation=90)

'''
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
'''

name_plot_2="plots/histogram_art_thefts_countries3.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Histogram places
########################################################################################## 
places =[ robberies[i]['Place'] for i in range(len(robberies))]        
zz=places.count('NOT DEFINED DURING BRC')
kk=places.count('CHURCH/PLACE OF WORSHIP')
ll=places.count('CASTLE / PALACE')
for i in range(zz):
    places.remove('NOT DEFINED DURING BRC')    
for i in range(kk):
    places.remove('CHURCH/PLACE OF WORSHIP')    
    places.append('CHURCH')       
for i in range(ll):
    places.remove('CASTLE / PALACE')   
    places.append('CASTLE')          
counter=collections.Counter(places)
place=counter.keys()

top_places=[]
non_top_places=[]
for i in place:
    aa=counter[i]
    if aa>2:
        top_places.append([i,aa])
    else:
        non_top_places.append([i,aa])        

kk=[]
for i in range(len(non_top_places)):
    kk.append(non_top_places[i][1])

top_places.append(['Others',sum(kk)])
top_placess=sorted(top_places,key=lambda l:l[1], reverse=True)        
tpplacess=np.array([ top_placess[i][0] for i in range(len(top_placess))])
tprob_cplacess=[ top_placess[i][1] for i in range(len(top_placess))]
x=np.arange(len(tpplacess))

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    ax2.text(x[i], tprob_cplacess[i]+1, str(tprob_cplacess[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')
ax2.bar(x,tprob_cplacess,color='m',align='center', alpha=1.0)
ax2.set_xlabel('Places')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,159])
plt.xticks(x, tpplacess)
plt.xticks(rotation=90)

'''
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
'''

name_plot_2="plots/histogram_art_thefts_places3.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Histogram objects
########################################################################################## 
objects =[ robberies[i]['* Object'] for i in range(len(robberies))]        
new_objects=[]
for i in range(len(objects)):
    aa=objects[i]
    pp=aa.find('>')    
    new_objects.append(aa[0:pp])
        
zz=new_objects.count('SCULPTURE / STATUE ')
kk=new_objects.count('GOLD & SILVERWARE / JEWELLERY ')
ll=new_objects.count('RELIGIOUS OR LITURGICAL ITEM ')
mm=new_objects.count('DOCUMENT / BOOK ')
nn=new_objects.count('WATCH / CLOCK ')

for i in range(zz):
    new_objects.remove('SCULPTURE / STATUE ')    
    new_objects.append('SCULPTURE')   
for i in range(kk):
    new_objects.remove('GOLD & SILVERWARE / JEWELLERY ')    
    new_objects.append('JEWELLERY')       
for i in range(ll):
    new_objects.remove('RELIGIOUS OR LITURGICAL ITEM ')   
    new_objects.append('RELIGIOUS ITEM')
for i in range(mm):
    new_objects.remove('DOCUMENT / BOOK ')    
    new_objects.append('BOOK')       
for i in range(nn):
    new_objects.remove('WATCH / CLOCK ')   
    new_objects.append('CLOCK') 

new_objects.remove('COIN / MEDAL')            
new_objects.append('COIN / MEDAL ')            
new_objects.remove('DRAWING')            
new_objects.append('DRAWING ') 
                          
counter=collections.Counter(new_objects)
objec=counter.keys()

top_obj=[]
non_top_obj=[]
for i in objec:
    aa=counter[i]
    if aa>2:
        top_obj.append([i,aa])
    else:
        non_top_obj.append([i,aa])

kk=[]
for i in range(len(non_top_obj)):
    kk.append(non_top_obj[i][1])

top_obj.append(['Others',sum(kk)])
top_objs=sorted(top_obj,key=lambda l:l[1], reverse=True)        
tpobjs=np.array([ top_objs[i][0] for i in range(len(top_objs))])
tprob_objs=[ top_objs[i][1] for i in range(len(top_objs))]
x=np.arange(len(tpobjs))

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    ax2.text(x[i], tprob_objs[i]+1, str(tprob_objs[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')
ax2.bar(x,tprob_objs,color='g',align='center', alpha=1.0)
ax2.set_xlabel('Objects')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,270])
plt.xticks(x, tpobjs)
plt.xticks(rotation=90)
name_plot_2="plots/histogram_art_thefts_objects3.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################  
#Plot pie objects
##########################################################################################  
#recipe = ["Painting","Sculture","Print","Drawing","Book","Religius Item",
#          "Jewellery","Ceramics","Icon","Firearm","Tapestry","Musical Instrument","Clock","Furniture","Others"]
ff=[]
for i in range(len(top_objs)):
    ff.append(top_objs[i][1])

recipe=[]
dara=[]
perce=[]
for i in range(len(top_objs)):
    perce.append(':'+str(round(top_objs[i][1]*100./sum(ff),1))+'%')
    
for i in range(len(top_objs)):
    recipe.append(top_objs[i][0]+perce[i])
    dara.append(top_objs[i][1])
    
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

#ax.set_title("Preferred Stolen Artworks between 2008-2019")
name_plot_2="plots/pie_art_thefts_objects3.pdf"
#plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Pie objects per country
########################################################################################## 
eu=['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic',
'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania',
'Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom']
USA=[]
Europe=[]
for i in range(len(robberies)):
    #aa=robberies[i]['Place']    
    aa=robberies[i]['Country']    
    if aa=='United States':
    #if aa=='RESIDENCE' or aa=='ART GALLERY':
        USA.append(robberies[i]['Place'])
    elif aa in eu:
    #elif aa=='CHURCH':
        Europe.append(robberies[i]['Place'])       
    #elif aa=='MUSEUM':
        #robberies[i]        

counter=collections.Counter(Europe)
objec=counter.keys() 

top_obj=[]
non_top_obj=[]
for i in objec:
    aa=counter[i]
    if counter[i]>4 and i!='NOT DEFINED DURING BRC':
        top_obj.append([i,aa])
    else:
        non_top_obj.append([i,aa])

kk=[]
for i in range(len(non_top_obj)):
    kk.append(non_top_obj[i][1])

top_obj.append(['Others',sum(kk)])
top_objs=sorted(top_obj,key=lambda l:l[1], reverse=True)    

ff=[]
for i in range(len(top_objs)):
    ff.append(top_objs[i][1])

recipe=[]
dara=[]
perce=[]
for i in range(len(top_objs)):
    perce.append(':'+str(round(top_objs[i][1]*100./sum(ff),1))+'%')
    
for i in range(len(top_objs)):
    recipe.append(top_objs[i][0]+perce[i])
    dara.append(top_objs[i][1])
    
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)                  

name_plot_2="plots/pie_art_thefts_objects-europe.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')

##########################################################################################
#Hisotgram artits
########################################################################################## 
artis =[ robberies[i]['Artist'] for i in range(len(robberies))]        
new_artis=[]
for i in range(len(artis)):
    aa=artis[i]
    aa=aa.upper()
    new_artis.append(aa)
    
counter=collections.Counter(new_artis)
artist=counter.keys()

top_artis=[]
for i in artist:
    aa=counter[i]
    if aa>1:
        top_artis.append([i,aa])


top_artists=sorted(top_artis,key=lambda l:l[1], reverse=True)        
tpartists=np.array([ top_artists[i][0] for i in range(len(top_artists))])
tprob_artists=[ top_artists[i][1] for i in range(len(top_artists))]
x=np.arange(len(tpartists))

tpartists_new=[]
for i in tpartists:
    pp=i.find('-')
    if pp>0:
        tpartists_new.append(i[0:pp])
    else:
        tpartists_new.append(i)      

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    ax2.text(x[i], tprob_artists[i]+0.2, str(tprob_artists[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')
ax2.bar(x,tprob_artists,color='orange',align='center', alpha=1.0)
ax2.set_xlabel('Artist')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,9])
plt.xticks(x, tpartists_new)
plt.xticks(rotation=90)
name_plot_2="plots/histogram_art_thefts_artists3.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Histogram months
########################################################################################## 
mont =[ robberies[i]['Uploading Date'] for i in range(len(robberies))]        
monts=[]
for i in range(len(mont)):
    aa=mont[i]
    bb=aa.find('-')
    monts.append(aa[bb+1:bb+3])
    
counter=collections.Counter(monts)
montss=counter.keys()

top_mon=[]
for i in montss:
    aa=counter[i]
    if aa>0:
        top_mon.append([i,aa])

top_mons=sorted(top_mon,key=lambda l:l[0])        
tpmons=np.array([ top_mons[i][0] for i in range(len(top_mons))])
tprob_mons=[ top_mons[i][1] for i in range(len(top_mons))]
x=np.arange(len(tpmons))
names_months=['January','February','March','April','May','June','July','August','September','October','November','December',]

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
for i in range(len(x)):
    ax2.text(x[i], tprob_mons[i]+1, str(tprob_mons[i]), color='k',
    horizontalalignment='center',
    verticalalignment='bottom',
    multialignment='center')
ax2.bar(x,tprob_mons,color='pink',align='center', alpha=1.0)
ax2.set_xlabel('Month')
ax2.set_ylabel('Number of large-scale ART thefts') 
ax2.set_ylim([0,50])
ax2.axhline(int(median(tprob_mons)))
plt.xticks(x, names_months)
plt.xticks(rotation=90)
name_plot_2="histogram_art_thefts_months.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Plot robberies per year
##########################################################################################  
Date = data_out['Uploading Date']
yrs=[]
for i in range(len(Date)):
    dd=Date[i]
    pp=dd.find('-')
    yrs.append(Date[i][0:pp])
    
counter=collections.Counter(yrs)
yr=counter.keys()
cases_value=[len(c_2009),len(c_2010),len(c_2011),len(c_2012),len(c_2013),len(c_2014),len(c_2015),len(c_2016),len(c_2017),len(c_2018)]

top_yrs=[]
for i in range(len(yr)):
    aa=counter[yr[i]]
    if aa>0:
        top_yrs.append([yr[i],aa])
                
cases=sorted(top_yrs,key=lambda l:l[0])        
cas_yr=np.array([ cases[i][0] for i in range(len(cases))])
cas_cas=[ float(cases[i][1])/float(cases_value[i]) for i in range(len(cases))]
x=range(len(cas_yr))

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
ax2.bar(x,cas_cas,color='brown',align='center', alpha=1.0)
ax2.set_xlabel('Year')
ax2.set_ylabel('Mean of artworks stolen \n per large-scale ART theft') 
#ax2.set_ylim([0,70])
plt.xticks(x, cas_yr)
name_plot_2="histogram_art_thefts_objects_mean.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################
#Plot robberies per year 2
########################################################################################## 
Ipsg = data_out['Ipsg Reference']
cas=[]
for i in range(len(Ipsg)):
    dd=Ipsg[i]
    pp=dd.find('.')
    cas.append(Ipsg[i][0:pp])

counter=collections.Counter(cas)
cases=counter.keys()

yearsss=OrderedDict()
yesrs=[]   
for i in range(len(cases)):
    year=int(cases[i][0:4])
    if year in yesrs:        
        yearsss[year].append(counter[cases[i]])        
    else:
        yesrs.append(year)
        yearsss[year]=[]
        yearsss[year].append(counter[cases[i]])        

keyss=yearsss.keys()
val=[]
stds=[]
for i in keyss:
    val.append(np.median(yearsss[i]))
    stds.append(np.std(yearsss[i]))
    

matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
kaeyss_new=keyss[:-1]
val_new=val[:-1]
stds_new=stds[:-1]
ax2.errorbar(kaeyss_new,val_new,yerr=stds_new,color='brown',fmt='o')
ax2.set_xlabel('Year')
ax2.set_ylabel('Mean of artworks stolen \n per large-scale ART theft') 
ax2.set_ylim([0,14])
#plt.xticks(x, cas_yr)
name_plot_2="histogram_art_thefts_objects_median.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')    
##########################################################################################
#Plot No.objects per theft (<3 and <2 objects)
##########################################################################################  
Ipsg = data_out['Ipsg Reference']
cas=[]
for i in range(len(Ipsg)):
    dd=Ipsg[i]
    pp=dd.find('.')
    cas.append(Ipsg[i][0:pp])

counter=collections.Counter(cas)
cases=counter.keys()
histo_objs=[]
for i in cases:
    aa=counter[i]
    histo_objs.append(aa)

counter=collections.Counter(histo_objs)
obs=counter.keys()
ob_0=[]
ob_1=[]
ob_2=[]
ob_3=[]
ob_4=[]
ob_5=[]
for i in obs:
    if i==1 or i==2:
        ob_0.append(counter[i])
    elif i==3 or i==4:
        ob_1.append(counter[i])        
    elif i>4 and i<11:
        ob_2.append(counter[i])        
    elif i>10 and i<51:
        ob_3.append(counter[i])        
    elif i>50 and i<100:
        ob_4.append(counter[i])                        
    elif i>99:
        ob_5.append(counter[i]) 

perce=[str(round(sum(ob_0)/4.19,0))+'%',str(round(sum(ob_1)/4.19,0))+'%',str(round(sum(ob_2)/4.19,0))+'%',
str(round(sum(ob_3)/4.19,0))+'%',str(round(sum(ob_4)/4.19,0))+'%',str(round(sum(ob_5)/4.19,0))+'%']
dara=[sum(ob_0),sum(ob_1),sum(ob_2),sum(ob_3),sum(ob_4),sum(ob_5)]
    
recipe=['1-2 Artworks','3-4 Artworks','5-9 Artworks','10-50 Artworks','51-99 Artworks','>100 Artworks']
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

ax.set_title("Art work stolen per large-scale art theft (2008-2019)")
name_plot_2="pie_art_thefts_objetos.pdf"
#plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################  
#Histogram objects stolen per art theft (<3 and < 2 objects)
##########################################################################################  
matplotlib.rcParams.update({'font.size': 22})        
fig3 = plt.figure(figsize=(12,12))  
ax2 = fig3.add_subplot(111)
binss=np.arange(0.0,51.0,1.0)
#binsss=np.arange(0.5,20.5,1.0)
a,b,c=ax2.hist(histo_objs,bins=binss)
binsss=list(binss)
binsss.remove(0.0)
binsss.remove(1.0)
ax2.bar(binsss,a,color='red',align='center', alpha=1.0)
zz=list(a)
zz.remove(0.0)
zz.remove(12.0)
aa,bb=numpy.polyfit(binsss, numpy.log(zz), 1,w=numpy.sqrt(zz))
y=np.exp(bb)*np.exp(aa*np.array(binsss))
ax2.plot(binsss,y,'k--')
ax2.set_xlabel('Artworks stolen')
ax2.set_ylabel('Number of large-scale ART thefts') 
#ax2.set_xticks(binss)
ax2.set_xlim([1.5,20])

name_plot_2="histogram_art_thefts_num_objects.pdf"
#plt.savefig(name_plot_2,bbox_inches='tight')
##########################################################################################  
#Pie objects stolen per art theft (ONLY >3
##########################################################################################  
objects =[ robberies[i]['Number of Objects'] for i in range(len(robberies))]   

counter=collections.Counter(objects)
objs=counter.keys()

obj_3_4=[]
obj_5_10=[]
obj_11_20=[]
obj_21_50=[]
obj_51_99=[]
obj_100=[]

for i in objs:
    if i==3 or i==4:
        obj_3_4.append(counter[i])
    elif i>4 and i<11:
        obj_5_10.append(counter[i])        
    elif i>10 and i<21:
        obj_11_20.append(counter[i])        
    elif i>20 and i<51:
        obj_21_50.append(counter[i])
    elif i>50 and i<100:
        obj_51_99.append(counter[i])
    elif i>99:
        obj_100.append(counter[i])                
    else:
        print('Algo anda mal')

dara=[round(sum(obj_3_4)/2.35,0),round(sum(obj_5_10)/2.35,0),round(sum(obj_11_20)/2.35,0),round(sum(obj_21_50)/2.35,0),round(sum(obj_51_99)/2.35,0),round(sum(obj_100)/2.35,0)]
recipe=['3-4','5-10','11-20','21-50','51-99','>100']

for i in range(len(dara)):
    print(recipe[i]+' is '+str(round(dara[i]*100/sum(dara),0)))
    
matplotlib.rcParams.update({'font.size': 22}) 
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

name_plot="pie_art_thefts_objetos+3.pdf"
#plt.savefig(name_plot,bbox_inches='tight')     
##########################################################################################  
#Pie objects stolen per art theft: countries
##########################################################################################  
robs =[]
for i in range(len(robberies)):     
    aa=robberies[i]['Number of Objects']
    if aa>20:
        robs.append(robberies[i])

Country =[ robs[i]['Country'] for i in range(len(robs))]
counter_country=collections.Counter(Country)
countries=counter_country.keys()
contries_plot=[]
contries_numbers_other=[]
for i in countries:
    if counter_country[i]>2:
        contries_plot.append([i,counter_country[i]])
    else:
        contries_numbers_other.append(counter_country[i])


contries_plot.append(['Others',sum(contries_numbers_other)])
top_contries_plot=sorted(contries_plot,key=lambda l:l[1], reverse=True)   
dara=[top_contries_plot[i][1] for i in range(len(top_contries_plot))]
recipe=[top_contries_plot[i][0] for i in range(len(top_contries_plot))]
for i in range(len(dara)):
    print(recipe[i]+' is '+str(round(dara[i]*100/sum(dara),0)))
    
matplotlib.rcParams.update({'font.size': 22}) 
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

name_plot="pie_art_thefts_objetos+21_countries.pdf"
#plt.savefig(name_plot,bbox_inches='tight')                             
##########################################################################################  
#Pie objects stolen per art thef: places   
##########################################################################################  
Place=[ robs[i]['Place'] for i in range(len(robs))]
counter_place=collections.Counter(Place)
places=counter_place.keys()
places_plot=[]
places_numbers_other=[]
for i in places:
    if counter_place[i]>3 and i!='NOT DEFINED DURING BRC':
        places_plot.append([i,counter_place[i]])
    else:
        places_numbers_other.append(counter_place[i])

places_plot.append(['Others',sum(places_numbers_other)])
top_places_plot=sorted(places_plot,key=lambda l:l[1], reverse=True)   
dara=[top_places_plot[i][1] for i in range(len(top_places_plot))]
recipe=[top_places_plot[i][0] for i in range(len(top_places_plot))]
for i in range(len(dara)):
    print(recipe[i]+' is '+str(round(dara[i]*100/sum(dara),0)))

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)             

name_plot="pie_art_thefts_objetos+100_places.pdf"
#plt.savefig(name_plot,bbox_inches='tight')
##########################################################################################
#Pie Media Imapct
##########################################################################################  

df=pd.read_csv('reco_media.csv')
media=df['media']
counter=collections.Counter(media)
media_im=[]
for i in counter.values():
    media_im.append(round(i*100/235.,0))

dara=media_im
recipe=['No results','One or Two reuslts','Covered Locally','Widely covered locally & few international','Widely covered internationally']
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

ax.set_title("Large-scale art thefts covered by virtual media (2008-2019)")
name_plot_2="pie_art_thefts_media.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')

##########################################################################################
#Pie Artist Recognition
##########################################################################################  
artist=df['artist']

counter=collections.Counter(artist)
media_im=[]
for i in counter.values():
    media_im.append(round(i*100/235.,0))

dara=media_im
recipe=['No record','Not classified',"Top 1'000,000",'Top 100,000','Top 10,000','Top 1,000','Top 100', 'Top 10']
fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts = ax.pie(dara, wedgeprops=dict(width=0.5), startangle=-40)

bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

ax.set_title("Artist recongnition of stolen artworks (2008-2019)")
name_plot_2="pie_art_thefts_recog_artist.pdf"
plt.savefig(name_plot_2,bbox_inches='tight')