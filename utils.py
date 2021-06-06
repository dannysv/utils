import pickle
import os
import re
import pathlib
import sys
import codecs
import json

from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring 

from bs4 import BeautifulSoup

# Error report
def error_message(e):
    print('error in %s'%str(os.path.dirname(os.path.abspath(__file__)))+'/'+str(__file__) )
    print('\tdetails ... %s' %str(e)[:120])
    print('falta retornar la linea donde ocurrio el problema')

# IO functions
def read_pick(path):
    try:
        f = open(path, 'rb')
        data = pickle.load(f)
        f.close()
        return data
    except Exception as e:
        error_message(e)
        return None

def save_pick(path, data):
    f=open(path, 'wb') 
    pickle.dump(data, f)
    f.close()

def read_txt(path):
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
        print('ok')
        return lines
    except Exception as e:
        error_message(e)
        return None

#function to read file with one of two available encodings
def read_file(path):
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

def read_json(path):
    try:
        with open(path, 'r') as f:
            rdict = json.load(f)
        return rdict 
    except Exception as e:
        return None 

def save_txt(path, lines):
    with open(path, 'w') as f:
        for item in lines:
            f.write("%s\n"%item)
    f.close()
    print('saved in %s'%path)

def save_xml(path, str_xml):
    out = codecs.open(path, 'w')
    out.writelines(str_xml)
    out.close()
    print('saved in %s'%path)

## strings
def find_matchpositions(line, subline):
    matches = re.finditer(subline, line)
    matches_positions = [match.start() for match in matches]
    return matches_positions 


#read xml and if bs return xml else txt
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

def save_xml(path, root):
    try:
        with open(path, 'w') as f:
            f.writelines(root)
        f.close()
        print('saved in %s'%path)
    except Exception as e:
        error_message(e)

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

#xml --> search the tag in content 
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

#Micellaneous
def novazios(listas):
    try:
        lens = [(i, len(l)) for i,l in enumerate(listas) if l is not None]
        return lens
    except Exception as e:
        error_message(e)
        return None 
