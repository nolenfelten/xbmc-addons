import urllib,urllib2,re,sys,socket,xbmcplugin,xbmcgui,htmllib

#[(url,show)]
def getSouthparkepisodes(url,name):
        res=[]
        f=urllib.urlopen(url)
        a=f.read()
        f.close()
        p=re.compile(r'target="mainFrame" href=".+?url=(.+?)">(.+?)</a>')
        match=p.findall(a)
        for url,name in match:
                res.append((url,name))
        return res

#[(url,show)]
def getSouthparkvidlinks(url):
        res=[]
        f=urllib.urlopen("http://allsp.com/"+url)
        a=f.read()
        f.close()
        p=re.compile(r"<embed src=\'/.+?.swf\?url=(.+?)'")
        match=p.findall(a)
        for url in match:
                res.append(url)
        return res


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

       
def addLink(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def showCats():
        cat=[("http://allsp.com/e.php?season=1", "Season 1"),("http://allsp.com/e.php?season=2", "Season 2"),("http://allsp.com/e.php?season=3", "Season 3"),("http://allsp.com/e.php?season=4", "Season 4"),("http://allsp.com/e.php?season=5", "Season 5"),("http://allsp.com/e.php?season=6", "Season 6"),("http://allsp.com/e.php?season=7", "Season 7"),("http://allsp.com/e.php?season=8", "Season 8"),("http://allsp.com/e.php?season=9", "Season 9"),("http://allsp.com/e.php?season=10", "Season 10"),("http://allsp.com/e.php?season=11", "Season 11"),("http://allsp.com/e.php?season=12", "Season 12")]
        for url,name in cat:
                addDir(name,url,1)

def showShows(url,name):
        shows=getSouthparkepisodes(url,name)
        for url,name in shows:
                addDir(name,url,2)
                
def showVidlinks(url):
        vids=getSouthparkvidlinks(url)
        for url in vids:
                addLink("WATCH SOUTHPARK EPISODE",url)
        
        
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
        print "categories"
        showCats()
elif mode==1:
        print "index of : "+url
        showShows(url,name)
elif mode==2:
        print "Next: "+url
        showVidlinks(url)
elif mode==3:
        print "show eps: "+url+" - "+name
        showEpisodes(url)
elif mode==4:
        print "show vidlinks: "+url
        showVidLinks(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
