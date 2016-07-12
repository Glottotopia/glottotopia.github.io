# -*- coding: utf8 -*-

from xml.etree  import ElementTree as ET 
from helpers import getLocation

from  html.entities import name2codepoint

import tempfile  
import re
import json 
from bs4 import BeautifulSoup
import pprint

class Drucksache:
  def __init__(self, bezirk, filename, parteien, baseurl):
    self.filename = filename 
    self.bezirk = bezirk  
    self.parsetree = None
    self.dsnr = None
    self.title = None
    self.url = None
    self.typ = None 
    self.html = None 
    self.text = None 
    self.status = None
    self.parteien = parteien
    self.address = None
    self.location = None
    self.ausschuss = None
    self.date=None
    self.ID=None
    
    self.html = self.getAntragHTML() 
    
    soup = BeautifulSoup(self.html, 'html.parser')
    self.soup = soup
    #parser = ET.XMLParser()
    #parser.parser.UseForeignDTD(True)
    #parser.entity.update((k, chr(name2codepoint[k])) for k in name2codepoint)      
    #tf = tempfile.NamedTemporaryFile(delete=False)
    #tempfilename = tf.name  
    #tf.write(bytes(self.html\
                    #.replace('<!doctype html>','')\
                    #.replace('&','&amp;'), 'utf8'))
    #tf.close()  
    #try:
      #self.parsetree = ET.parse(tempfilename, parser=parser)      
    #except ET.ParseError:
      #print(tempfilename, "could not be parsed")
      #return
    #root = self.parsetree.getroot()  
    root = soup
    #the relevant information is found in tr's with classes zl11 and zl12
    zl11 = root.find_all(".//tr[@class='zl11']")
    zl12 = root.find_all(".//tr[@class='zl12']")  
    title_ = root.find("title").text 
    try:
      useless, self.dsnr, self.title =  title_.split(' - ')
      self.dsnr = self.dsnr.replace('/','-')
    except:
      return
    trs = zl11 + zl12 
    for tr in trs: 
      tds = tr.findall('td') 
      try:
        self.text = tds[1].find('a').text
        self.words = self.text.split()  
        self.date = self.words[0]         
      except AttributeError:
        continue
      self.url = baseurl+tds[1].find('a').attrib['href']
      #partei = tds[3].text
      self.typ = tds[5].text   
      print(self.typ)
      
    self.ID = "%s_%s" % (self.bezirk.kuerzel, self.dsnr)  
    print(self.ID)
    self.text = self.getAntragText()
    self.status = self.getStatus()
    self.ausschuss = self.getAusschussFields()
    metadatadict = self.getMetadata()
    initiatoren = metadatadict.get('Initiator:').lower()
    self.parteien = []
    for p in (("spd","SPD"),
              ("cdu","CDU"),
              ("fdp","FDP"), 
              ("link","Linke"),
              ("pirat","Piraten"),
              ("grünen","Grüne"),
                ):
      if p[0] in initiatoren:
        self.parteien.append(p[1])        
    self.verfasser = metadatadict.get('Verfasser:')
    self.typ = metadatadict.get('Drucksache-Art:')
    #self.ausschuss = metadatadict.get('Beratungsfolge:')
    self.address,self.location = getLocation(self.text,self.bezirk)
    
  def getMetadata(self):
    categories = self.soup.find_all("td", class_="kb1")
    values = [k.find_next_sibling() for k in categories]
    c2s = [c.text for c in categories]
    v2s = []
    for v in values:
      try: 
        text = v.text.strip()
      except AttributeError:
        text = None
      v2s.append(text)
    #pprint.pprint(list(zip(c2s,v2s)))
    return(dict(zip(c2s,v2s)))
      
    
  def getAntragHTML(self):
    return self.sanitize(open(self.filename, encoding="latin-1").read(),self.bezirk)
                   
  def getAntragText(self):
    bodys = self.soup.find_all('body')
    #print(len(bodys))
    #print(bodys[0])
    try:
      text = bodys[1].text
    except IndexError:
      text = ''
    #chunk = html.split('<meta name="generator" content="Aspose.Words for .NET')[1]
    #text = re.sub('<[^>]*?>','',chunk) 
    return text
    
    
  def getStatus(self):
    if "Der Antrag wird abgelehnt" in self.html:
      return "abgelehnt"
    if "Der Änderungsantrag wird abgelehnt" in self.html:
      return "abgelehnt"
    if "in der BVV abgelehnt" in self.html:
      return "abgelehnt"
    if "ohne Änderungen in der BVV beschlossen" in self.html:
      return "angenommen"
               
               
  def getAusschussFields(self):
    ausschuesse =  list(set(re.findall("Ausschuss für ([A-Za-zÄÖÜäöüß]+)", self.html)))
    return "; ".join(ausschuesse)
                 
          
  def sanitize(self,f,bezirk): 
        """
        repair invalid XHTML served by ALLRis
        
        ALLRis pages show a number of recurrent errors. These are repaired in this method
        * one META tag is not properly closed 
        * a path within a comment has slashes
        * one ampersand is not propely escaped
        * a number of closing divs are missing. The precise number varies.
        * extra XML declarations inline
        * duplicate attributes
        """
        opendivs = f.count('<div')
        closeddivs = f.count('</div>')
        offset = opendivs-closeddivs-1 
        a = f.strip().split('\n')  
        #add encoding
        a[0] = a[0].replace('<?xml version="1.0"','<?xml version="1.0" encoding="utf8" ')
        a = [l.replace('&showall=true','&amp;showall=true')\
            .replace('<?xml version="1.0" encoding="utf-8" standalone="no"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">','')\
            .replace('<?xml version="1.0" encoding="iso-8859-1" standalone="no"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">','')\
            .replace('<hr>','<hr />')\
            .replace('target="_blank"','')
            .replace('bvv-online/images/link_pdoc.gif" alt="PDF-Dokument">','bvv-online/images/link_pdoc.gif" alt="PDF-Dokument" />')                          
            for l in a 
              if '<meta name="ROBOTS" content="INDEX, NOFOLLOW">' not in l
                and ' den Pfad /bvv-online/ aufgerufen werden' not in l
                  and '<!--@set var="std-layout" val="land" --' not in l
            ]
        a = a[:-2]  
        if bezirk.name in ('Friedrichshain-Kreuzberg', 'Treptow-Köpenick' ):
          offset = 2
        #print(offset)
        #divs = '\n'+  offset * '</div>'  
        divs = ''
        result = '\n'.join(a)+divs+'\n</body>\n        </html>' 
        return result
                           
  def conformspelling(self,b):
    """Return the Bezirk's name in the way as it is used in the URL"""
    
    return b.lower().replace('ö', 'oe')
    
  def getWords(self,txt): 
    stopwords=[ x for x in """ wird 
    bezirksamt 
    werden 
    bezirksverordnetenversammlung 
    eine 
    sich 
    nicht 
    beschließen 
    dass 
    möge 
    sind 
    auch 
    berlin 
    durch 
    einer 
    nach 
    begründung 
    soll 
    oder 
    ersucht 
    diese 
    über 
    kann 
    bezirk 
    einen 
    wurde 
    ausschuss 
    sitzung 
    sowie 
    ihrer 
    bereits 
    haben 
    dieser 
    sollen 
    unter 
    können 
    dafür 
    alle 
    beschlossen 
    damit 
    einem 
    wenn 
    dazu 
    stellen 
    antrag 
    eines 
    gebeten 
    keine 
    welche 
    einzusetzen 
    rahmen 
    dies 
    beauftragt 
    hier 
    sein 
    beschließt 
    berichten 
    diesem 
    dabei 
    bürger 
    noch 
    beschluss 
    wurden 
    drucksache 
    möglichkeit 
    zuständigen 
    berliner 
    möglich 
    dieses 
    anderen 
    bezirks 
    fraktion 
    gibt 
    insbesondere 
    zwischen 
    bezirksbürgermeister 
    erledigt 
    ihre 
    mehr 
    muss 
    aufgefordert 
    erhalten  """.split()]
    return set([x for x in re.split('[^a-zäöüß]',txt.lower()) if len(x)>3 and x not in stopwords])        
  
  def generatejson(self):
    latitude = 52.561944 #Insel Großer Wall in Spandau
    longitude = 13.226944
    try:
      latitude, longitude = self.location.split(',')
    except AttributeError:
      pass
    except ValueError:
      pass
    contentd = dict(bezirk=self.bezirk.name,
             dsnr=self.dsnr,
             typ=self.typ,
             title=self.title,
             text=self.text,
             url=self.url,
             date=self.date,
             ausschuss=self.ausschuss,
             address=self.address,
             parteien=self.parteien
             )
    geojsonfeature = { "type": "Feature",
          "geometry": {"type": "Point", "coordinates": [float(longitude), float(latitude)]},
          "properties": contentd
          }
    self.geojson = geojsonfeature  
    
    
  def write(self):        
    singled = { 
      "type": "FeatureCollection",
      "features": [
        self.geojson
       ]
     }        
    f = open('out/%s.geojson'%self.ID, 'w')
    f.write(json.dumps(singled))
    f.close()
    
  def writeold(self,s, format='csv'):
    """output Antrag data in tabular form"""
    
    if format=='wiki':
      out = self.wikitemplate% '\n'.join([self.wikirowtemplate.format(**a.__dict__) for a in s]) 
      print(out)
    if format=='csv':    
      out = self.csvtemplate % ('\n'.join([self.csvrowtemplate.format(**a.__dict__) for a in s]))
      print(out)
    if format=='solr':     
      for a in s:
        path = './bvvsolr/%s_%s.xml' % (a.bezirk.kuerzel,a.dsnr.replace('/','-'))
        #print path 
        out = open(path, 'w')
      try:
          a.status = a.status.replace(' ','_')
      except AttributeError:
          a.status = ''
          out = open(path, 'w')
      try:
            a.typ = a.typ.replace(' ','_')
      except AttributeError:
            a.typ = ''
      try:
              a.url = a.url.replace('&','&amp;')
      except AttributeError:
              a.url = ''
      a.bezirk.name = a.bezirk.name.replace('-','_') 
      a.updateLengths()
      a.getLocation()
      #print a.parteien
    if a.typ in ('Beschluss','Beschlussempfehlung', 'Dringlichkeitsantrag', 'Antrag_zur_Beschlussfassung', "Änderungsantrag", "Entschließung", "Dringlichkeitsbeschlussempfehlung", "Entschließungsantrag", "Gemeinsamer_Antrag", "Gemeinsamer_Dringlichkeitsantrag", "Drucksache_zurückgezogen", "Beschluss"):
            a.typ = 'Antrag'
            a.parteifields = '\n'.join(['<field name="partei">%s</field>'%partei for partei in a.parteien])
            a.wordfields = '\n'.join(['<field name="word">%s</field>'%word for word in self.getWords(a.text)])
            a.status = self.getStatus(a.html)
            a.ausschussfields = self.getAusschussFields(a.html)
            a.text = a.text.replace('& ','&amp;')\
            .replace('<','&lt;')\
            .replace('>','&gt;')\
            .replace('&uuml;','ü')\
            .replace('&ouml;','ü')\
            .replace('&auml;','ü')\
            .replace('&Uuml;','Ü')\
            .replace('&Ouml;','Ö')\
            .replace('&Auml;','Ä')\
            .replace('&szlig;','ß')\
            .replace('&nbsp;','')\
            .replace('&copy;','(c)')
            d = a.__dict__        
    if d['location'] == None or d['location'].strip() in ('52.5166,13.3833',''):
            d['locationfield'] = ''
    else:
              d['locationfield'] = '<field name="location">%s</field>' % d['location']
              d.update({'lenparties':len(a.parteien)}) 
              t = self.solrtemplate.format(**d)
              out.write(t.encode('utf8'))
              out.close() 
    if format == 'pickle': 
              pickle.dump( s, open( "allris.pkl", "wb" ) )
              