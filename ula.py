# -*- coding: utf-8 -*-
"""
Created on Sat May 29 23:11:46 2021

@author: Admin
"""

import time
import send_notify as sn
from bs4 import BeautifulSoup


import task as t
def move_cookie(url):
    try:
        req = urllib.request.Request(url,headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
       
#        req.add_header('cookie', cookies)
        html = urllib.request.urlopen(req).read()
        
        return html
    except:
        time.sleep(.5)
def search_aim(url,e,ep,arg,n):
    global last_obj
    global id_ur
    global nocallFlag
    id_ur=arg['id']
    nocallFlag=n
    ic=0
    

    last_obj=''
    cookies='u=2oo1nu2b.1n70e6a.1kef6x0q2g400; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; __cfduid=d2ddd99101f420ac9e4ef2286f42d93971619340117; abp=1; _ym_uid=161934012867593413; _ym_d=1619340128; _gcl_au=1.1.1891493782.1619340128; _ym_isad=1; _ga=GA1.2.444167857.1619340131; _gid=GA1.2.1086308075.1619340131; showedStoryIds=64-63-62-61-58-50-49-48-47-42-32; lastViewingTime=1619340132981; no-ssr=1; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBYnlzVGk3VTVKRW8wVkZQNXBSVll0ZVlpM0lxVUJ1Q2JQVUtjS0FnSGJvRXNPOXVlbnlYSzJhWndMMFZZQ0J4MDhUNHdwNEl6ZEtNN29SbjhFYmdKcFdCQlBhTWtGazh0OHVaajd2dm8vRXNqR3ZRekZrNGREcHg4RHM1SWNqRUticmtvRERmU3dXRGhZZVdxNzlrbkh6RExVT2tRL2dMZWtlMnpYMmdHWXVOM1lUTW1qcVZycUpxK1Foa0h0U2FWamRjTkR1SmNPei8wS3AyaEQ3c1loTGFWQWZaTnEzcnlIUVdoaE1wSE9NU2tNWmJVNFN0a0w5aUNSMDNiUUJ6NE5GWW1Xa3BFdWNRRWorR2FjMG8zWEszdlNHQzA5dWxiV0JKeDcyTnppYkciLCJpYXQiOjE2MTkzNDAxMjksImV4cCI6MTYyMDU0OTcyOX0.x56NtN0vT_szQ72LKHb_rPN248fdQmmrD2VR2V-mVWs; __gads=ID=f95604c8309bede7:T=1619340137:S=ALNI_MbP8PZ56jLKn0t-8dwSdrEvXFL4hg; f=5.df155a60305e515a2d6059f4e9572c01630247e51b9c7ed6630247e51b9c7ed6630247e51b9c7ed6630247e51b9c7ed6357212485bdbc727357212485bdbc727357212485bdbc72738b4a54cef5443c13afa3d284af961c234bd85fe5e85ba0346b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8068fd850112c943dbcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0acf722fe85c94f7d0c0df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f2da10fb74cac1eab0df103df0c26013a93e76904ac7560d30c79affd4e5f1d11162fe9fd7c8e9767d7c49cf6b81d2f60cdba646c82fa93525e61d702b2ac73f71edb2dc30b444aa77ddd833b009ab2722af9e5c04fd1603f47b0e452571a73fb8db57d0f7c7638d40df103df0c26013a0df103df0c26013aafbc9dcfc006bed997fd17c411415984742c3d3ce384d4af3de19da9ed218fe23de19da9ed218fe2d6fdecb021a45a31b3d22f8710f7c4ed78a492ecab7d2b7f; ft="x4bkXgVCiM9j0Q8nZP5vvMELl2J0125Pu/0FWvBLWJ4VCtWvA1boCBg30jupzPKpVkNmC7EwOcjoaZ6Ab9bYqMzfIbMWBeVd3GqxToLsAyZAHODxs0IUxrYFr9Wiw+ACTq81ynRmBxEfcxIX0bQH6JFVkKbb17fLSVmVE0ti7pEpNrRyDHCaUc74NAYFZLCl"; sessid=b945dc22bfc4bbaf86804379312e7965.1619340520; auth=1; buyer_popup_location=0; SEARCH_HISTORY_IDS=4; __utmc=99926606; __utmz=99926606.1619340630.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=99926606.444167857.1619340131.1619340630.1619348709.2; sx=H4sIAAAAAAACA5WRQZLaQAxF79LrWci22i1zG1sQGSsZDTRjGaa4e0SqmArZZdv1++np6yt1y2kq65iNqhAysDmzG3DafaU17dKyrevNT+N+jmdkjZQoAnElV7P0lg5p1/TNgG2fge5vKXPTzaU7wkEiyghCAlbBnkj6OE91k7aMlauxsFZ0U7WggtFfyC43HQRynHr9uSxmBhqWMZlY0EGeyPcL98P187ZO6ATAYQlItWqFSL9YFmgflvvbMbfjpgUjSxgCFH+q6hN5/hy2dSHtS0C0qpODgrk/lhd5tYSHZfvj6pHojnqtZBhpNqmA38hLyQsshf3DwQXBRAiiUTZmJH5FYhfIoYi5Oc6g0Y+g1TANIn5b1u7X/rwsFxFVNnCKAiRWISWS+orMfSC5vLfnMl/W/KdFixvFDFF4IjMdbpvOzRQzwx4iEbeOPisp8j+WQwlkL2W16+EkM5myY2wtro+N/h/ZZ2ru99/PTAhDmQIAAA==; buyer_from_page=item'
    while e.isSet()==False:
            if ep.isSet()==False:
                
                ep.wait()
            
            try:
                req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' })
                req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
                
                req.add_header('cookie', cookies)
                html = urllib.request.urlopen(req).read()
                
                 
                soup = BeautifulSoup(html, 'lxml')
            except :
             
                time.sleep(4)
                continue
            obj=soup.find_all('li',class_="product_item")
          
            for s in obj:
                if  len(s['class'])==1:
                    find=s
                    break
            sal=find.find('a').get('href')

            print(sal)
            if sal != last_obj and last_obj!='' and sal!='':
                
                if len(t.getSale(id_ur)['sales'])>0:
                    ic=0
                    for s in t.getSale(id_ur)['sales']:
                        if s['sale']==sal:
                            ic+=1
                    if ic>0:
                        pass
                       
                if ic==0:
            
                    sn.send_notify('Обьявление найдено '+'https://www.youla.ru/'+sal,id_ur,url)
                    t.addSale(id_ur,sal,url)
#                    getphonThread=thGetPhone(item,'https://www.avito.ru'+sal)
#                    getphonThread.daemon=True
#                    getphonThread.start() 
                   
                  
            
               
            print(sal)
            last_obj=sal
            time.sleep(10)   
    print('stoped '+url)
    
    return 'abort'
