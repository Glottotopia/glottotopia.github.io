#!/usr/bin/python
# -*- coding: utf8 -*-

#import urllib as urllib1
#import urllib2
import pickle
import re
import glob
from drucksache import Drucksache
from bvvberlin import Land
import json

class ALLRis:  
    #wikitemplate = u""" 
    #{| class="wikitable sortable" border="1"
    #|+ Sortable table
    #|-
    #! bezirk || dsnr || titel || url || parteien || typ
    #%s
    #|-
    #|}
    #"""

    #wikirowtemplate=u"""|-
    #| {kuerzel} || {dsnr} || {titel} || {url} || {parteien} || {typ}"""

    #csvtemplate = u"""        bezirk        dsnr        titel        url        partei        typ
 
    #%s
    #"""

    #csvrowtemplate=u"""{bezirk}        {dsnr}        {title}        {url}        {partei}        {typ}        """
    
    #solrtemplate  = u"""<add><doc>
  #<field name="id">{ID}</field>  
  #<field name="typ">{typ}</field>  
  #<field name="titel">{title}</field>  
  #<field name="bezirk">{bezirk.name}</field>  
  #{parteifields} 
  #{wordfields}
  #{ausschussfields}
  #<field name="text_de">{text}</field> 
  #<field name="status">{status}</field>
  #{locationfield}
  #<field name="url">{url}</field>  
  #<field name="#words">{lenws}</field>  
  #<field name="#chars">{lenchars}</field>  
  #<field name="parteien">{lenparties}</field>   
#</doc></add>
#""" 

    
    
    locationstore = {}
 
    
if __name__ == '__main__':
    berlin = Land()
    allris = ALLRis()   
    for bezirk in berlin.bezirke:    
      kuerzel = bezirk.kuerzel
      #print(kuerzel)
      files = glob.glob("bezirksdrucksachen/%s/*/*241"%kuerzel)
      drucksachen = []
      for f in files:
       ds = Drucksache(bezirk,f,"Parteien",berlin.baseurl)
       ds.generatejson()
       ds.write()
       drucksachen.append(ds)
      
      print(len(drucksachen))
      allfeaturejson = [ds.geojson 
                        for ds in drucksachen 
                        if ds.geojson["geometry"]["coordinates"][1] != 52.561944]
      globaljson = { 
        "type": "FeatureCollection",
        "features": allfeaturejson
      }       
      f = open('out/global-%s.geojson'%kuerzel, 'w')
      f.write(json.dumps(globaljson))
      f.close()
      
 