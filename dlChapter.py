#!/usr/bin/python3
import sys
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def getId(url,headers):
    ##Gets all the video and topic id's in key: value pairs in the form of a dictionary for any given site(it has to be downloaded)
    site=requests.get(url,headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    vIDdict={}
    nameDict={}
    vIDList=[] #Ordered list so i can display numbers
    for li in soup.find_all('li'):
        vID=li.get('data-video-id')
        tID=li.get('data-topic-id')

        #Only take video id's that are not none
        if vID!=None:
            vIDdict.update({vID:tID})
            nameDict.update({vID:li.span.string})
            vIDList.append(vID)

        #Check if vID dictionary is empty
    if not vIDdict:
        raise NameError("Wrong cookie/url bro,can't get in the site(or maybe the chapter doesn't have any videos)")
    return [vIDdict,nameDict,vIDList]


  

def dlVideo(headers,vID,tID,name): ##Add chapname, subchapname
    ##Download the video with streamlink

    #Make the POST request to get the token
    data=f'tID={tID}&vID={vID}&videoViewType=2'
    resTok = requests.post('https://bagrut.gool.co.il/api/Tokens/Add',headers=headers,data=data)
    token=resTok.text
    ##DOWNLOADING PART
    #Formats a url with the vID and tID
    dlUrl=(f'https://5a153f939af4b.streamlock.net/bagrut/{vID}/manifest.mpd?tID={tID}&videoView=2&accessToken={token}')

    #Check if download directory exists, if not make one.
    if not(os.path.isdir('downloads')):
        os.mkdir('downloads')


    #Make directiories for chapters and their subchapters
    #if not(os.path.isdir(f'{}')):
     #   os.mkdir('downloads')

    #Download with streamlink
    os.system(f"streamlink '{dlUrl}' 'best' -o 'downloads/{name}.mp4' ")
    os.system(f"ffmpeg -i 'downloads/{name}.mp4' -c copy 'downloads/{name}Fix.mp4'")

    os.remove(f'downloads/{name}.mp4')
    os.rename(f"downloads/{name}Fix.mp4",f"downloads/{name}.mp4")


    
def promptAndDl():
    ##Prompts the user for cookie and link, either as arguments or by logging in themselves
    keepGoing=True
    while(keepGoing):
        try:
            if "http" in sys.argv[2]:
                url=sys.argv[2]
                cookie=sys.argv[1]
            elif "http" in sys.argv[1]:
                url=sys.argv[1]
                cookie=sys.argv[2]
            else:
                raise NameError('lol')
            if '.ASPXAUTH=' not in cookie:
                cookie=f".ASPXAUTH={sys.argv[1]}"
        except:
            driver = webdriver.Chrome("./chromedriver.exe")
            driver.get("https://bagrut.co.il")
            print("Login into your account\n")
            input("Enter when you're done:")
            url=(driver.current_url)
            cookie=driver.get_cookie(".ASPXAUTH")['value']

        #Create the headers
        headers = {
            'Cookie': cookie,
            'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        #Get the site, create the id dicts and the list + stupid handling
        getIdOut=getId(url,headers)
            
        #dictionary of 'vID':'tID'
        ids=getIdOut[0]
        #dictionary of 'vID':'name'
        names = getIdOut[1]
        #G
        idsList=getIdOut[2]

        #Chapter and subchapter names(not done yet)
        ##chapN=getIdO(headers,url,getChapSubChap)[0]
        #Dictionary of 'tID':'Topic name" 
        ##subChapN=getIdO(headers,url,getChapSubChap)[1]
        #Ask which videos are wanted
        inp = input("Do you want all the videos? or just a specific one?['a' = all, Any other key = one]: ")


        if (inp.lower()=='a'):
            i=1
            for key in ids:
                dlVideo(headers,key,ids[key],f"{str(i)}) {names[key]}")
                i+=1
        else:
            #Display possible videos to download
            i=1
            for v in ids:
                print(f"{i}) {names[v]}")
                i+=1

            inp=input('Which one? ')
            vID=idsList[int(inp)-1]
        
            dlVideo(headers,vID,ids[vID],f"{inp}) {names[vID]}")

        #Ask if user wants to keep going
        kg=input("Wanna do other episode/s?[Yes:y,No:Any key]")
        if (kg.lower()=='y'):
            cookie=driver.get_cookie(".ASPXAUTH")['value']
            urlC = input("Change url?[Yes:y,No:Any key]")
            if urlC.lower()=='y':
                url = input("Enter new url: ")

        keepGoing=False

##Run the prompt
promptAndDl()
#getChapSubChap("Test.html")

#How do i know if the cookie/url is ok?if i know it's not how do i know which one isn't?Also how do i change it?
#Debug, make better, test, bettercookie
#Get chapter and subchapter with beautifulsoup, and make subdirectories accordingly
#Make script to download everything
#Figure out out to get AUTHASPX from credentials/ one time login.



###Unifinished functions
def dlAll(cookie,url):
    ##Simply download all of the course
    headers = {
        'Cookie': cookie,
        'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    getIdOut=getId(url,headers)
    ids=getIdOut[0]
    names = getIdOut[1]

    for key in ids:
        dlVideo(headers,key,ids[key],names[key])

def getChapSubChap(filename):
    ##Gets all the video and topic id's in key: value pairs in the form of a dictionary for any given site(it has to be downloaded)
    site=open(filename)
    soup = BeautifulSoup(site, 'html.parser')
    #Chapter name
    ##chapN
    #'tID':"Topic name"
    ##subChapN={}
    for li in soup.find_all('li'):
        vID=li.get('data-video-id')
       # if vID!=None:           
            #vIDdict.update({vID:tID})
            #vIDList.append(vID)
        #return [vIDdict,nameDict,vIDList]
        if vID!=None:
            print(li.previous_sibling)
    ##return [chapN,subChapN]
    


##Pretty much useless function
def argAndDl(cookie,url,dlAll):
    ##Alternative to the prompter,takes arguments
    headers = {
        'Cookie': cookie,
        'User-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    getIdOut=getId(url,headers)
    ids=getIdOut[0]
    names = getIdOut[1]
    idsList=getIdOut[2]

    if dlAll:
        for key in ids:
            dlVideo(headers,key,ids[key],names[key])
    else:
        i=1
        for v in ids:
            print(f"{i})  {names[v]}")
            i+=1

        vID=int(input('Which one? '))-1
        vID=idsList[vID]
        dlVideo(headers,vID,ids[vID],names[vID])

