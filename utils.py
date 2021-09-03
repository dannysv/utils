import pickle
import os
import re
import pathlib
import sys
import codecs
import json

from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring 

from bs4 import BeautifulSoup
import requests

# IO FUNCTIONS
## create folder if not existis
def create_folder(path):
    try:
        if os.path.exists(path):
            print('exists : %s'%path)
        else:
            os.mkdir(path) 
            print('succesfully created : %s'%path)
    except Exception as e:
        error_message(e)

# split folder in subfolders of size k
def split_folder(folder, itemspersub, extention):
    number = itemspersub
    files = os.listdir(folder)
    files = [f for f in files if str(f).endswith('.'+extention)]
    n = len(files)
    partes = n//number
    #print(partes)
    for part in range(partes):
        print("limites -> %i : %i", (part*number,(part+1)*number))
        if os.path.exists('part'+str(part))== False:
            print('crear carpeta')
            os.mkdir('part'+str(part))
            #mover los part 200
            for i in range(part*number,(part+1)*number):
                cmd = 'cp '+os.path.join(folder,files[i]) + ' '+ 'part'+str(part) + "/"
                print(cmd)
                os.system(cmd)
    
    if n%number>0:
        part=part+1
        print('resto')
        print("limites -> %i : %i", (part*number,(part+1)*number))
        print(n)
        if os.path.exists('part'+str(part))== False:
            print('crear carpeta')
            os.mkdir('part'+str(part))
	#mover los part 200
        for i in range(part*number,n):
            cmd = 'cp '+ os.path.join(folder, files[i]) + ' '+ 'part'+str(part) + "/"
            print(cmd)
            os.system(cmd)
        print('The folder %s, was split into %i subfolders'%(folder, partes+1))
    else:
        print('The folder %s, was split into %i subfolders'%(folder, partes))


## Read serialize object with pickle
def read_pick(path): 
    try:
        f = open(path, 'rb')
        data = pickle.load(f)
        f.close()
        return data
    except Exception as e:
        error_message(e)
        return None

## Write object as serialized file pickle
def write_pick(path, data): 
    f=open(path, 'wb') 
    pickle.dump(data, f)
    f.close()

## Read txt file by using the defaul encoding=utf-8
def read_txt(path): 
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        print('ok')
        return lines
    except Exception as e:
        error_message(e)
        return None

## Read txtfile with one of two available encodings - util for portuguese
def read_txt_pt(path):
    try:
        with codecs.open(path, 'r', encoding="utf-8") as f:
            resp = f.readlines()
        print('read %s with utf-8'%path)
        return resp 
    except Exception as e:
        if "'utf-8' codec can't" in str(e):
        #try to read with iso-8859-1
            try: 
                with codecs.open(path, 'r', encoding="iso-8859-1") as f:
                    resp = f.readlines()
                print('read %s with iso-8859-1'%path)
                return resp 
            except Exception as e:
                print(e)
                return None
        else:
            print(e)
            return None 

## Write txt file default case (utf-8)
def write_txt(path, lines):
    with open(path, 'w') as f:
        for item in lines:
            f.write("%s\n"%item)
    f.close()
    print('saved in %s'%path)


## Read json file 
def read_json(path):
    try:
        with open(path, 'r') as f:
            rdict = json.load(f)
        return (rdict, None)
    except Exception as e:
        return (None, e)
 
# Write json file
def write_json(path, data):
    try: 
        with open(path, 'w') as f:
            #json.dump(data, f, indent=4, sort_keys=True)
            json.dump(data, f, indent=4)
        f.close()
        print('saved in %s'%path)
    except Exception as e:
        return None
        error_message(e)

## Write object as xml file
def write_xml(path, str_xml):
    out = codecs.open(path, 'w')
    out.writelines(str_xml)
    out.close()
    print('saved in %s'%path)

## Read xml file as str-object or beautifulsoup file(bs = True)
def read_xml(path, bs):
    try:
        content = []
        with open(path, 'r') as f:
            content = f.readlines()
            content_str = "".join(content)
            if bs:
                bs_content = BeautifulSoup(content_str, 'lxml')
                return bs_content
            else:
                return content_str 
    except Exception as e:
        error_message(e)
        return None

## Write xml file 
def write_xml(path, root):
    try:
        with open(path, 'w') as f:
            f.writelines(root)
        f.close()
        print('saved in %s'%path)
    except Exception as e:
        error_message(e)

## Remove all files of a given path
def removeall(path):
    try:
        if path != "":
            cmd = 'rm '+path+'/*'
            os.system(cmd)
        lista = os.listdir(path)
        for item in lista:
            path_rec = os.path.join(path, item)
            removeall(path_rec)
    except Exception as e:
        error_message(e)

## Remove all files asking for confirmation
def removefiles(path):
    try:
        resp = query_yes_no('tem certeza de apagar os arquivos em : %s'%path)
        if resp:
            removeall(path)
            print('Arquivos apagados corretamente')
        else:
            print('Finalizado sem modificacoes')
    except Exception as e:
        error_message(e)

# LISTAS, STRINGS, MISCELLANEOUS
## For a given list of lists, return the non-none ones
def novazios(listas):
    try:
        lens = [(i, len(l)) for i,l in enumerate(listas) if l is not None]
        return lens
    except Exception as e:
        error_message(e)
        return None 

## Find match positions of substring in a given string
def find_matchpositions(line, subline):
    matches = re.finditer(subline, line)
    matches_positions = [match.start() for match in matches]
    return matches_positions 


# INTERACTIVE
## Interactive pronpt to select two options (y, n)
def query_yes_no(question):
    try:
        valid = {"y":True, "n": False}
        prompt = " [y/n] "
        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if choice=='':
                return valid['no']
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Por favor, responda com 'yes'  ou 'no'"
                                 "(or 'y' or 'n')")
    except Exception as e:
        error_message(e)

# ERROR HANDLING
## Error report
def error_message(e):
    print('error in %s'%str(os.path.dirname(os.path.abspath(__file__)))+'/'+str(__file__) )
    #print('\tdetails ... %s' %str(e)[:120])
    print('\tdetails ... %s' %str(e))
    #print('falta retornar la linea donde ocurrio el problema')


## xml and html --> search the tag in content 
def get_xmltag(content, bs, tag):
    try:
        if bs:
            res = content.find_all(tag.lower())
            #if res==None or len(res)==0:
            #    print('Are you sur that tag %s exists?. Please, verify the casing' %tag)
            #else:
            #    print('ok')
            return res
        elif bs==False:
            bs_content = BeautifulSoup(str(content), 'lxml')
            res = bs_content(tag.lower())
            #if res==None or len(res)==0:
            #    print('Are you sur that tag %s exists?. Please, verify the casing' %tag)
            #else:
            #    print('ok')
            return res
        else:
            print('Opcion no valida para bs %s' %str(bs))
            return None
    except Exception as e:
        error_message(e)
        return None

def get_xmlattribute(bscontent, attribute):
    try:
        return bscontent[attribute]
    except Exception as e:
        #error_message(e)
        return None 


# request link by using requests lib
def get_link(link, timeout):
    try:
        resp_link = requests.get(link, timeout=timeout)
        return (resp_link, None)
    except Exception as e:
        return (None, e)

# search exact match items
def exactmatch_items(resp_requests, tag, attribute, value):
    soup = BeautifulSoup(resp_requests.content)
    items = soup.findAll(tag, {attribute:value})
    return items

# search exact match item
def exactmatch_item(resp_requests, tag, attribute, value):
    soup = BeautifulSoup(resp_requests.content)
    item = soup.find(tag, {attribute:value})
    return item 
