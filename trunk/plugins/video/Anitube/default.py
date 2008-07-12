import urllib,urllib2,re,xbmcplugin,xbmcgui
#anitube V2008

def INDEXCATS():
        res=[]
        req = urllib2.Request('http://www.anitube.net/faqs/list-of-anime.html')
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        code=re.sub('&#39;','',link)
        code2=re.sub('&nbsp;','',code)
        code3=re.sub('&auml;','',code2)
        response.close()
        p=re.compile('<a href="(.+?)">(.+?)</a>.+?</p>')
        match=p.findall(code3)
        del match[0:3]
        for li,name in match:
                urlage="http://www.anitube.net/"+li
                res.append((urlage,name))
        for url,name in res:
                addDir(name,url,1,"")
        addDir("Suzuka","http://www.anitube.net/anime-videos/anime-episodes-p-t/suzuka-2.html",1,"")
       
def INDEX(url,name):
        res=[]
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        p=re.compile('<a href="(.+?)">(.+?)</a></div>\r\n\t</td>\r\n')
        matchdir=p.findall(link)
        if len(matchdir)>0:
                for lia,name in matchdir:
                        url=urllib.unquote(lia)
                        addDir(name,url,1,"")
        else:
                p=re.compile('<td width="1%" align="right"><a href="(.+?)"><img src="http://www.anitube.net/components/com_seyret/themes/Dark_0.3/images/right.png" border="0">')
                match=p.findall(link)
                for li in match:
                        addDir("NEXT PAGE",li,1,"")
        
                p=re.compile('<a href="(.+?)"><img title=".+?<table><tr><td width=.+?>Title</td><td width=.+?>:</td><td width=.+?>(.+?)</td></tr><tr>')
                match=p.findall(link)
                for li2,name in match:
                        url=urllib.unquote(li2)
                        res.append((name,url))
                for name,url in res:
                        addDir(name,url,2,"")
                
                
def VIDEOLINK(url):
        f=urllib.urlopen(url)
        a=f.read()
        f.close()
        p=re.compile('flashvars="file=(.+?)&showdigits')
        match=p.findall(a)
        for url in match:
                f=urllib.urlopen(url)
                b=f.read()
                f.close()
                p=re.compile('<location>(.+?)</location>\r\n<image>(.+?)</image>')
                match=p.findall(b)
                for url,thumb in match:
                        addLink(name,url+".flv",thumb)
                
               
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
        print "CATEGORY INDEX : "
        INDEXCATS()
elif mode==1:
        print "GET INDEX OF PAGE : "+url
        INDEX(url,name)
elif mode==2:
        print "GET INDEX OF PAGE : "+url
        VIDEOLINK(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
