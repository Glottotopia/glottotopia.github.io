# -*- coding: utf8 -*-
import re
#import urllib as urllib1
from urllib.request import urlopen
from urllib.parse import quote 
from xml.etree  import ElementTree as ET 

def queryNominatim(p,bezirk): 
  via, number = p
  coords = None 
  urlstring = 'http://nominatim.openstreetmap.org/search/de/berlin/{}/{}?format=xml'.format(bezirk.name.replace('_','-').replace('ö','%C3%B6'),quote(via)) 
     
  try:
    coords = bezirk.geodict[(via,number)]
    return coords
  except KeyError:  
    urlstring = 'http://nominatim.openstreetmap.org/search/de/berlin/{}/{}?format=xml'.format(bezirk.name.replace('_','-').replace('ö','%C3%B6'),quote(via)) 
    if number != '':   
      urlstring =  'http://nominatim.openstreetmap.org/search/de/berlin/{}/{}/{}?format=xml'.format(bezirk.name.replace('_','-').replace('ö','%C3%B6'),quote(via),number) 
  info = urlopen(urlstring).read()
  root = ET.fromstring(info)
  place = root.find('.//place')
  try:
    longitude = place.attrib['lon']
    latitude = place.attrib['lat']
    #print urlstring, longitude, latitude
  except AttributeError:
    #print via, number,
    print(urlstring, "noresults")
    bezirk.geodict[(via,number)] = ''
    return ''
  coords = '%s,%s'%(latitude,longitude)  
  print(via,number,coords)
  bezirk.geodict[(via,number)] = coords
  return coords
  
      
def getLocation(text,bezirk):    
  nonstrasse = ["Einbahnstraße","Einkaufsstraße","Fahrradstraße", "Hauptverkehrsstraße", "Spielplatz", "Schulplatz", "Hauptstraße", "Der Platz", "Den Platz", "Dem Platz", "Die Straße", "Der Straße", "Serviceplatz", "Stellplatz", "Arbeitsplatz", "Sportplatz", "Parkplatz", "Stadtplatz", "Schulplatz"]              
  viastring = "(Straße|Strasse|Platz|Brücke|Allee|Chaussee|Landstraße|Landstrasse|Ufer)" 
  kleinvia = re.findall("([A-ZÖÜÄ][a-zäöüß]+%s) *([0-9]*)"%viastring.lower(),text)            
  grossvia = re.findall("([A-ZÖÜÄ][a-zäöüß]+ +%s) *([0-9]*)"%viastring,text)
  strichvia =  re.findall("([A-ZÖÜÄ][a-zäöüß-]+%s) *([0-9]*)"%viastring,text)
  vias = kleinvia + grossvia + strichvia
  places = []   
  places = [(x[0],x[2]) for x in vias]   
  d = {}
  #compute which via is mentioned most often
  for p in places:
    v = p[0].strip()
    n = p[1].strip()
    if v in nonstrasse:      
      continue
    if v.endswith('spielplatz') or v.endswith('arbeitsplatz') or v.endswith('parkplatz') or v.endswith('sportplatz') or v.endswith('schulplatz'):
      continue
    try:
      d[p] += 1
    except KeyError:
        d[p] = 1
        #max(d.iterkeys(), key=(lambda key: d[key])) 
  maxvalue = 0
  candidates = []
  for k in d:
    if d[k]>maxvalue:
      maxvalue = d[k]
      #new highest candidate
      candidates = [k]
      continue
    if d[k] == maxvalue:
      candidates.append(k) 
  coords = [(c,queryNominatim(c,bezirk)) for c in candidates]
  if len(coords) >0:  
    return coords[0] 
  return '',None
            