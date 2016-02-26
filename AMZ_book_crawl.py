# coding: utf-8

# In[2]:

## Useful libraries
import re
from lxml import html
from lxml import etree
import datetime
import requests
import csv, io, time
import threading, Queue
import random

## Read a csv file
def read_data(filename):
    csvf = io.open(filename, encoding='Windows-1252', errors='ignore')
    rows = csv.reader(csvf,delimiter=';', quoting=csv.QUOTE_NONE)
    data = [row for row in rows]
    csvf.close()
    return data

## Write a csv file
def write_data(path,data):
    f = open(path, "wb")
    w = csv.writer(f,delimiter=';')
    for row in data:
        w.writerow(row)
    f.close()

## Write a csv file with append mode
def write_data_append(path,data):
    fd = open(path,'ab')
    a = csv.writer(fd, delimiter=';',quoting=csv.QUOTE_MINIMAL);
    a.writerows(data);
    fd.close()

            
## Checks the duration
class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
  
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time # Force timer reinit

## Check Index of a value in a list
from itertools import izip as zip, count ## izip for maximum efficiency
def find_index(list, value):
    return [i for i, j in zip(count(), list) if j == value]

## Cleans a string
def strclean(s):
    s =s.replace('\n','').replace('\x96','').strip()
    return s


# In[15]:

## Use this to scrap Amazon Book Webpages content
## Get the tree for a URL string
def getTreeFromUrl(url):
    page = requests.get(url)
    tree = html.fromstring(page.text)
    return tree

## Get the tree of the product from the research URL
def getProductTreeFromSearchUrl(searchurl):
    search_results = getTreeFromUrl(searchurl).xpath('//a[@class="a-link-normal a-text-normal"]/@href')
    product_tree = getTreeFromUrl(search_results[0])
    return product_tree

## Get the title of the item
def getTitleFromTree(tree):
    return tree.xpath('//div[@id="booksTitle"]//span[@id="productTitle"]/text()')[0].strip()

## Get the Editeur of a book
def getEditorFromTree(tree):
    editor = tree.xpath('//div[@id="detail_bullets_id"]//li//text()')#[find_index(editor,u'Editeur\xa0:')[0]+1].replace(';','').strip()
    editeurs = editor[find_index(editor,u'Editeur\xa0:')[0]+1].strip()
    editeur = re.sub('\((.*)\)','',editeurs).replace(';','').strip()
    return editeur

## Get All the reliure mode of a book
def getReliureModeFromTree(tree):
    reliure = tree.xpath('//h1[@id="title"]//span[@class="a-size-medium a-color-secondary a-text-normal"]//text()')[0].strip()
    reliure_bis = tree.xpath('//span[@class="a-button a-spacing-mini a-button-toggle format"]//text()')
    reliure_clean = map(strclean,reliure_bis)
    if len(reliure_clean)>0:
        set_indices = []
        for k in range(len(reliure_clean)):
            if (len(reliure_clean[k])==0) or (re.search('EUR',reliure_clean[k])!=None):
                set_indices.append(k)
        rel = [v for i, v in enumerate(reliure_clean) if i not in set_indices]
        if len(rel)>0:
            for k in range(len(rel)):
                if len(rel[k])>1:
                    reliure=reliure+"--"+rel[k]
    return reliure

## Get Date of parution of the book
def getDateFromTree(tree):
    return tree.xpath('//h1[@id="title"]//span[@class="a-size-medium a-color-secondary a-text-normal"]//text()')[1].replace('\x96','').strip()
    
## Get the number of comments from the book page
def getNumberOfComments(tree):
    nb_comments =tree.xpath('//span[@id="acrCustomerReviewText"]//text()')
    if len(nb_comments)>0:
        nb_commentaires=nb_comments[0].replace('commentaires client','').replace('commentaire client','').strip()
    else: 
        nb_commentaires='0'
    return nb_commentaires

## Get the amazon sell rank of a book
def getSellRank(tree):
    num_top = tree.xpath('//li[@id="SalesRank"]//text()')
    if len(num_top)>0:
        top_number=num_top[find_index(num_top,"Classement des meilleures ventes d'Amazon:")[0]+1].replace('\n','').replace('(','').replace('.','').replace('en Livres','').strip()
    else:
        top_number='0'
    return top_number

## Get the book category
def getCategory(tree):
    return tree.xpath('//div[@class="bucket"][h2="Rechercher des articles similaires par rubrique"]//div[@class="content"]//li//text()')[2]

## Get the stock status
def getStockStatus(tree):
    stockl=tree.xpath('//div[@id="availability"]//text()')
    if len(stockl)>0:
        stock = stockl[1].replace('\n','').strip()
    else:
        stock="Pas d'infos de stock"
    return stock

## Gathering all the informations from the EAN and url template
def getAllInfosFromSearchUrl(ean,url_template):
    searchurl = url_template.replace("EAN",ean)
    tree = getProductTreeFromSearchUrl(searchurl)
    file_out_line=ean
    now = datetime.datetime.now()
    file_out_line=now.strftime("%Y-%m-%d")+"|"+file_out_line+"|"+getTitleFromTree(tree)+"|"+getEditorFromTree(tree)+"|"+getDateFromTree(tree)+"|"+getNumberOfComments(tree)+"|"+getSellRank(tree)+"|"+getCategory(tree)+"|"+getStockStatus(tree)+"|"+getReliureModeFromTree(tree)
    file_out_line=file_out_line.replace('"','')
    write_data_append("result_livres.csv",[[file_out_line]])
    return file_out_line
    




## Improvement : multi threading !!!
ean = ["9782817900049","9782013480529","9782916124049","9782296082595","9782730215862","9782051011624","9786131509322","9782070423620","9786134285346","9782070771691","9782070444724","9782916972480","9790006482900","9782070138296","9782070405848","9782862533926","9782915740264","9782844663085","9786131590955","9782211048583","9782841356690","9781274448989","9781271609253","9782844663054","9782751406454","9782918758327","9782731693003","9782858229918","9782915612172"]
url_template = "http://www.amazon.fr/s/ref=nb_sb_noss?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Dstripbooks&field-keywords=EAN"

## Launching the timer
timer = Timer()  
timer.start()

queue = Queue.Queue()
for current_product in ean:
    queue.put(current_product)


num_connections = 10

class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            try:
                current_product = self.queue.get_nowait()
            except Queue.Empty:
                raise SystemExit

            getAllInfosFromSearchUrl(current_product,url_template)

# start threads
threads = []
for dummy in range(num_connections):
    t = WorkerThread(queue)
    t.start()
    threads.append(t)


# Wait for all threads to finish
for thread in threads:
    thread.join()
    
## Stop the timer and print the elapsed time
timer.stop()
print ' '
print 'Total time in seconds :', timer.interval



