class Antrag:
  def __init__(self, bezirk, filename):
    self.bezirk = bezirk  
    self.filename = filename
    self.url = filename
    self.html = open(filename).read()
    self.dsnr = dsnr
    self.status = status
    self.text = text 
    self.html = getAntragHTML(filename) 
    self.titel = titel
    self.parteien = parteien
    self.typ = typ 
    self.location = location
    self.url = url
    self.ID = "%s_%s" % (self.bezirk.kuerzel, self.dsnr) 
    self.getLocation()
    
    def extractantrag(self,scrapedpage,parteien):
      """extract the Antrag data from an ALLRis page"""
      
      parser = ET.XMLParser()
      parser.parser.UseForeignDTD(True)
      parser.entity.update((x, unichr(i)) for x, i in name2codepoint.iteritems())
      
      tf = tempfile.NamedTemporaryFile(delete=False)
      name = tf.name  
      tf.write(scrapedpage.encode('ascii', 'xmlcharrefreplace'))
      tf.close()  
      
      try:
        tree = ET.parse(name, parser=parser)               
        except ET.ParseError:
          print "parse error in", name, "for", parteien
          return []
          root = tree.getroot()  
          zl11 = root.findall(".//{http://www.w3.org/1999/xhtml}tr[@class='zl11']")
          zl12 = root.findall(".//{http://www.w3.org/1999/xhtml}tr[@class='zl12']")    
          trs = zl11 + zl12
          antraege = []
          for tr in trs: 
          tds = tr.findall('{http://www.w3.org/1999/xhtml}td') 
          words = tds[1].find('{http://www.w3.org/1999/xhtml}a').text.split() 
          dsnr = words[0]
          title = ' '.join(words[1:]) 
          href = self.baseurl+tds[1].find('{http://www.w3.org/1999/xhtml}a').attrib['href']
          #partei = tds[3].text
          typ = tds[5].text
          antrag = Antrag(bezirk , dsnr, url=href, parteien=parteien)
          antrag.title = unicode(title)  
          antrag.typ = unicode(typ)  
          antrag.html = self.getAntragHTML(href,bezirk)
          antrag.text = self.getAntragText(antrag.html)
          antrag.status = self.getStatus(antrag.html)
          antrag.ausschuss = self.getAusschussFields(antrag.html)
          antrag.updateLengths()
          antraege.append(antrag)
          return antraege        
          
          def updateLengths(self):            
          self.lenchars = len(self.text)
          self.lenws = len(self.text.split())
          self.lenws = len(self.parteien)
          
          def getLocation(self):         
          def queryNominatim(p): 
          via, number = p
          coords = None
          try:
            coords = self.bezirk.geodict[via]
            except KeyError: 
            urlstring = u'http://nominatim.openstreetmap.org/search/de/berlin/{}/{}?format=xml'.format(self.bezirk.name.replace(u'_',u'-').replace(u'ö',u'%C3%B6'),urllib1.quote(via.encode('utf8'))) 
            if number != '':  
            urlstring = u'http://nominatim.openstreetmap.org/search/de/berlin/{}/{}/{}?format=xml'.format(self.bezirk.name.replace(u'_',u'-').replace(u'ö',u'%C3%B6'),urllib1.quote(via.encode('utf8')),number)  
            info = urllib2.urlopen(urlstring).read()
            root = ET.fromstring(info)
            place = root.find('.//place')
            try:
              longitude = place.attrib['lon']
              latitude = place.attrib['lat']
              #print urlstring, longitude, latitude
              except AttributeError:
              #print via, number,
              print urlstring, "noresults"        
              self.bezirk.geodict[via] = ''
              return ''
              coords = '%s,%s'%(latitude,longitude)
              self.bezirk.geodict[via] = coords
              return coords
              
              nonstrasse = [u"Einbahnstraße","Einkaufsstraße",u"Fahrradstraße", u"Hauptverkehrsstraße", "Spielplatz", "Schulplatz", u"Hauptstraße", "Der Platz", "Den Platz", u"Die Straße", u"Der Straße", "Serviceplatz", "Stellplatz", "Arbeitsplatz", "Sportplatz", "Parkplatz"]
              
              viastring = u"(Straße|Strasse|Platz|Brücke|Allee)" 
              kleinvia = re.findall(u"([A-ZÖÜÄ][a-zäöüß]+%s) *([0-9]*)"%viastring.lower(),self.text)            
              grossvia = re.findall(u"([A-ZÖÜÄ][a-zäöüß]+ +%s) *([0-9]*)"%viastring,self.text)
              strichvia =  re.findall(u"([A-ZÖÜÄ][a-zäöüß-]+%s) *([0-9]*)"%viastring,self.text)
              vias = kleinvia + grossvia + strichvia
              places = []   
              places = [(x[0],x[2]) for x in vias]   
              d = {}
              for p in places:
                v = p[0].strip()
                n = p[1].strip()
                if v not in nonstrasse:
                  if v.endswith('spielplatz') or v.endswith('arbeitsplatz') or v.endswith('parkplatz') or v.endswith('sportplatz'):
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
                          candidates = [k]
                          continue
                        if d[k] == maxvalue:
                          candidates.append(k) 
                          coords = map(queryNominatim, candidates) 
                          
                          coords = [x for x in coords if x != None]
                          if len(coords) >0: 
                          self.location = coords[0]
                          
        def write(self,s, format='csv'):
        """output Antrag data in tabular form"""
        
        if format=='wiki':
            out = self.wikitemplate% u'\n'.join([self.wikirowtemplate.format(**a.__dict__) for a in s]) 
            print out
        if format=='csv':    
            out = self.csvtemplate % ('\n'.join([self.csvrowtemplate.format(**a.__dict__) for a in s]))
            print out
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
                if a.typ in ('Beschluss','Beschlussempfehlung', 'Dringlichkeitsantrag', 'Antrag_zur_Beschlussfassung', u"Änderungsantrag", u"Entschließung", "Dringlichkeitsbeschlussempfehlung", u"Entschließungsantrag", "Gemeinsamer_Antrag", "Gemeinsamer_Dringlichkeitsantrag", u"Drucksache_zurückgezogen", "Beschluss"):
                    a.typ = 'Antrag'
                a.parteifields = '\n'.join(['<field name="partei">%s</field>'%partei for partei in a.parteien])
                a.wordfields = '\n'.join(['<field name="word">%s</field>'%word for word in self.getWords(a.text)])
                a.status = self.getStatus(a.html)
                a.ausschussfields = self.getAusschussFields(a.html)
                a.text = a.text.replace('& ','&amp;')\
                                    .replace('<','&lt;')\
                                    .replace('>','&gt;')\
                                    .replace('&uuml;',u'ü')\
                                    .replace('&ouml;',u'ü')\
                                    .replace('&auml;',u'ü')\
                                    .replace('&Uuml;',u'Ü')\
                                    .replace('&Ouml;',u'Ö')\
                                    .replace('&Auml;',u'Ä')\
                                    .replace('&szlig;',u'ß')\
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
         
        
    #def fetch(self,store):
        #"""fetch all antraege"""
        #for a in store:
            #url = 'http://berlin.de%s' %a.href
            #print url
            #page = urllib2.urlopen(url).read().decode('latin-1') 
            #out = open('texts/%s-%s' % (a.bezirk.kuerzel,a.dsnr.replace('/','_')),'w')
            #out.write(page.encode('latin-1')) 

    def write(self,s, format='csv'):
        """output Antrag data in tabular form"""
        
        if format=='wiki':
            out = self.wikitemplate% u'\n'.join([self.wikirowtemplate.format(**a.__dict__) for a in s]) 
            print out
        if format=='csv':    
            out = self.csvtemplate % ('\n'.join([self.csvrowtemplate.format(**a.__dict__) for a in s]))
            print out
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
                if a.typ in ('Beschluss','Beschlussempfehlung', 'Dringlichkeitsantrag', 'Antrag_zur_Beschlussfassung', u"Änderungsantrag", u"Entschließung", "Dringlichkeitsbeschlussempfehlung", u"Entschließungsantrag", "Gemeinsamer_Antrag", "Gemeinsamer_Dringlichkeitsantrag", u"Drucksache_zurückgezogen", "Beschluss"):
                    a.typ = 'Antrag'
                a.parteifields = '\n'.join(['<field name="partei">%s</field>'%partei for partei in a.parteien])
                a.wordfields = '\n'.join(['<field name="word">%s</field>'%word for word in self.getWords(a.text)])
                a.status = self.getStatus(a.html)
                a.ausschussfields = self.getAusschussFields(a.html)
                a.text = a.text.replace('& ','&amp;')\
                                    .replace('<','&lt;')\
                                    .replace('>','&gt;')\
                                    .replace('&uuml;',u'ü')\
                                    .replace('&ouml;',u'ü')\
                                    .replace('&auml;',u'ü')\
                                    .replace('&Uuml;',u'Ü')\
                                    .replace('&Ouml;',u'Ö')\
                                    .replace('&Auml;',u'Ä')\
                                    .replace('&szlig;',u'ß')\
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
         
        
    #def fetch(self,store):
        #"""fetch all antraege"""
        #for a in store:
            #url = 'http://berlin.de%s' %a.href
            #print url
            #page = urllib2.urlopen(url).read().decode('latin-1') 
            #out = open('texts/%s-%s' % (a.bezirk.kuerzel,a.dsnr.replace('/','_')),'w')
            #out.write(page.encode('latin-1')) 
        #print out
     

     def getStatus(self, html):
       if "Der Antrag wird abgelehnt" in html:
         return "abgelehnt"
         if u"Der Änderungsantrag wird abgelehnt" in html:
           return "abgelehnt"
           if "in der BVV abgelehnt" in html:
             return "abgelehnt"
             if u"ohne Änderungen in der BVV beschlossen" in html:
               return "angenommen"
               
               
               def getAusschussFields(self, html):
                 ausschuesse =  list(set(re.findall(u"Ausschuss für ([A-Za-zÄÖÜäöüß]+)", html)))
                 return "\n".join(['<field name="ausschuss">%s</field>'%x for x in ausschuesse])
                 
                 def getAntragHTML(self,url,bezirk):
                   scrapedpage = self.sanitize(urllib2.urlopen(url).read().decode('latin-1'),bezirk)
                   return scrapedpage
                   
                   def getAntragText(self,html):
                     parser = ET.XMLParser()
                     parser.parser.UseForeignDTD(True)
                     parser.entity.update((x, unichr(i)) for x, i in name2codepoint.iteritems())
                     
                     #the parser can only read from a file, not from a string, so we create a file
                     tf = tempfile.NamedTemporaryFile(delete=False)
                     name = tf.name  
                     tf.write(html.encode('ascii', 'xmlcharrefreplace'))
                     tf.close()  
                     try:
                       tree = ET.parse(name, parser=parser) 
                       root = tree.getroot()  
                       bodys = root.findall('.//{http://www.w3.org/1999/xhtml}body')
                       text = '\n'.join([a for a in bodys[1].itertext()]) 
                       #print '.',
                       except ET.ParseError:
                         chunk = html.split('<meta name="generator" content="Aspose.Words for .NET')[1]
                         text = re.sub('<[^>]*?>','',chunk)
                         #print ''
                         return text
                         
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
                         if bezirk.name in ('Friedrichshain-Kreuzberg', u'Treptow-Köpenick' ):
                           offset = 2
                           divs = '\n'+  offset * '</div>'  
                           result = '\n'.join(a)+divs+'\n</body>\n        </html>'.encode('utf8') 
                           return result
                           
                           def conformspelling(self,b):
                             """Return the Bezirk's name in the way as it is used in the URL"""
                             
                             return b.lower().replace(u'ö', 'oe')
                             
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
                             return set([x for x in re.split(u'[^a-zäöüß]',txt.lower()) if len(x)>3 and x not in stopwords])        
                             
     
  def write(self,s, format='csv'):
    """output Antrag data in tabular form"""
    
    if format=='wiki':
    out = self.wikitemplate% u'\n'.join([self.wikirowtemplate.format(**a.__dict__) for a in s]) 
    print out
    if format=='csv':    
    out = self.csvtemplate % ('\n'.join([self.csvrowtemplate.format(**a.__dict__) for a in s]))
    print out
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
            if a.typ in ('Beschluss','Beschlussempfehlung', 'Dringlichkeitsantrag', 'Antrag_zur_Beschlussfassung', u"Änderungsantrag", u"Entschließung", "Dringlichkeitsbeschlussempfehlung", u"Entschließungsantrag", "Gemeinsamer_Antrag", "Gemeinsamer_Dringlichkeitsantrag", u"Drucksache_zurückgezogen", "Beschluss"):
            a.typ = 'Antrag'
            a.parteifields = '\n'.join(['<field name="partei">%s</field>'%partei for partei in a.parteien])
            a.wordfields = '\n'.join(['<field name="word">%s</field>'%word for word in self.getWords(a.text)])
            a.status = self.getStatus(a.html)
            a.ausschussfields = self.getAusschussFields(a.html)
            a.text = a.text.replace('& ','&amp;')\
            .replace('<','&lt;')\
            .replace('>','&gt;')\
            .replace('&uuml;',u'ü')\
            .replace('&ouml;',u'ü')\
            .replace('&auml;',u'ü')\
            .replace('&Uuml;',u'Ü')\
            .replace('&Ouml;',u'Ö')\
            .replace('&Auml;',u'Ä')\
            .replace('&szlig;',u'ß')\
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
              
              
              #def fetch(self,store):
                #"""fetch all antraege"""
                #for a in store:
                  #url = 'http://berlin.de%s' %a.href
                  #print url
                  #page = urllib2.urlopen(url).read().decode('latin-1') 
                  #out = open('texts/%s-%s' % (a.bezirk.kuerzel,a.dsnr.replace('/','_')),'w')
                  #out.write(page.encode('latin-1')) 
                  #print out
                  
                
                