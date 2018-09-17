import pickle
import numpy as np
import gmplot # you need to install this from the above link
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as cm
import matplotlib.colors as colors
import six

fbase='.'
floc='.' #/Users/ratlifflj/Dropbox/stPCA/src/data'
floc2=fbase+'/figs/'

xl  = pd.ExcelFile(fbase+'/data/ps_pay_stn_blkface.xlsx')
dfsup = xl.parse('Sheet 1')
xl  = pd.ExcelFile(fbase+'/data/crossreferencesheet.xlsx')
dfcf = xl.parse('PS 4.22.15')
elkeys=dfcf['ELMNTKEY']

locs=pickle.load(open(fbase+'/data/bloclocs.p','rb')) # load location data


#get unique paid areas
paidareas=dfcf['PAIDAREA'].unique()
# get coordinates for each of those sub areas
sub={}
#locs=pickle.load(open('./data/blockfacelocs.p','rb')) # load location data
for pa in paidareas:
    mask=(dfcf['PAIDAREA']==pa)
    dftemp=dfcf[mask]
    elkey0=dftemp['ELMNTKEY']
    sub[str(pa)]={}
    for key in elkey0.values.tolist():
        if key in locs.keys():
            sub[str(pa)][key]=locs[key]
            
'''
    Draw all blocks
'''
def drawAllBlocks(locsvals, st='map'):
    '''
        input:
            locsvals=np.asarray(locs.values())
            st = 'mapname'
    '''
    gmap=gmplot.GoogleMapPlotter(47.6097,-122.3331,13) # this centers the map in seattle
    clusterlocs=np.asarray(locsvals)
    for b in range(np.size(clusterlocs,0)):
        gmap.polygon([clusterlocs[b,1],clusterlocs[b,3]],[clusterlocs[b,0],
                   clusterlocs[b,2]],color='r',edge_width=3)

    fi=st+".html"
    gmap.draw(floc2+fi)
#plt.show()

'''
    Draw subareas
'''
def drawSubAreas(paidareas,st='mapsub'):
    gmap2=gmplot.GoogleMapPlotter(47.6097,-122.3331,13) 
    c=list(six.iteritems(colors.cnames))
    i=0
    fi=st+".html"
    clusterlocs={}
    for pa,cl in zip(paidareas,c):
        clusterlocs[str(pa)]=np.asarray(sub[str(pa)].values())
        for b in range(np.size(clusterlocs[str(pa)],0)):
            gmap2.polygon([clusterlocs[str(pa)][b,1],clusterlocs[str(pa)][b,3]],
                      [clusterlocs[str(pa)][b,0], clusterlocs[str(pa)][b,2]],
                      color=cl[0],edge_width=3)
        i=i+1
    gmap2.draw(floc2+fi)


def drawBlock(bloc,st='mapblock', cind=0, newmap=True):
    gmap2=gmplot.GoogleMapPlotter(47.6097,-122.3331,13) 
    c=list(six.iteritems(colors.cnames))
    i=0
    fi=st+".html"
    for b in range(np.size(bloc,0)):
        gmap2.polygon([bloc[b][1],bloc[b][4]],
                      [bloc[b][0], bloc[b][3]],
                      color=c[b][0],edge_width=3)
        print (c[b][0])
    #i=i+1
    gmap2.draw(floc2+fi)

def drawBlocks(blocs,st='mapblock', cind=0, newmap=True):
    gmap2=gmplot.GoogleMapPlotter(47.6097,-122.3331,13) 
    c=list(six.iteritems(colors.cnames))
    i=0
    fi=st+".html"
    for bloc in blocs.values():
      for b in range(np.size(bloc,0)):
        gmap2.polygon([bloc[b][1],bloc[b][4]],
                      [bloc[b][0], bloc[b][3]],
                      color=c[b][0],edge_width=20)
        print (c[b][0])
    gmap2.draw(floc2+fi)

bell=sub['Belltown'] 
blst=[9354, 9353] 
blocs={}

for b in blst:
  blocs[b]=bell[b]

bloc=blocs.values()
drawBlock(bloc, st='map-bell-img-ex')
