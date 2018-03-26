#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import urllib.request
import os,sys
import re

baseUrl = "https://www.23us.cc/html/81/81001/";
dict = {}

def downloadText():
  log = [];
  # "r"   以读方式打开，只能读文件 ， 如果文件不存在，会发生异常      
  # "w"   以写方式打开，只能写文件， 如果文件不存在，创建该文件
  #       如果文件已存在，先清空，再打开文件
  # "rb"  以二进制读方式打开，只能读文件 ， 如果文件不存在，会发生异常      
  # "wb"  以二进制写方式打开，只能写文件， 如果文件不存在，创建该文件
  #       如果文件已存在，先清空，再打开文件
  # "rt"  以文本读方式打开，只能读文件 ， 如果文件不存在，会发生异常      
  # "wt"  以文本写方式打开，只能写文件， 如果文件不存在，创建该文件
  #       如果文件已存在，先清空，再打开文件
  # "rb+" 以二进制读方式打开，可以读、写文件 ， 如果文件不存在，会发生异常      
  # "wb+" 以二进制写方式打开，可以读、写文件， 如果文件不存在，创建该文件
  #       如果文件已存在，先清空，再打开文件

  isExists = os.path.exists('./txt/都市奇门医生/分章节');
  if not isExists:
    os.makedirs('./txt/都市奇门医生/分章节');
    pass

  fm = open("./txt/都市奇门医生/都市奇门医生-ALL.txt",'w');
  fm.close();
  html = gethtml(baseUrl,0);
  reg = re.compile(r'<a style=""=style="" href="(?P<URL>.+)">(?P<NAME>.+)</a>');
  res = reg.findall(html);
  #打印目录
  printList(res,log);

  #获取小说章节
  for i in range(1,10):

    URL = res[i][0];
    NAME = res[i][1];
    NAME = dealName(NAME);

    if URL.endswith('http'):
      newUrl = URL;
    else:
      newUrl = baseUrl+URL;
    
    text = getText(gethtml(newUrl,0)); 
    if text == "" and text is None:
      continue;
      pass
    #分章节创建文件
    fm = open("./txt/都市奇门医生/分章节/"+NAME,'w');
    writeText(fm,text,NAME);
    #全集追加
    fm = open("./txt/都市奇门医生/都市奇门医生-ALL.txt",'a');
    writeText(fm,text,NAME);
    printLog(str('%.2f' % (float(i)/float(len(res)) * 100)) + "% => "+NAME + "i="+str(i),log);
    pass
  printLog("100%",log);
  log = '\n'.join(log);
  fm = open("./txt/都市奇门医生/都市奇门医生.log",'w');
  fm.write(log);
  fm.close();
  return;

def printList(res,log):
  printLog("============目录============",log);
  for i in range(len(res)):
    URL = res[i][0];
    NAME = res[i][1];
    NAME = dealName(NAME);

    log.append(NAME + " i = " + str(i));
    print(NAME + " i = " + str(i));
    pass
  printLog("============目录============",log);

def dealName(NAME):
  NAME = NAME.replace("第","");
  NAME = NAME.replace("章","");
  reg = re.compile(r'(?P<NUM>[0-9]\d*)');
  matched = re.search(reg, NAME);
  NUM = str(matched.group('NUM').zfill(5));
  NAME = NAME.replace(" ","");
  NAME = NAME.replace(NUM,"");
  NAME = "第" + NUM + "章 " + NAME;
  return NAME;

def writeText(fm,text,name):
  fm.write("\n=========="+name+"==========\n");
  fm.write(text);
  fm.close();

def printLog(logStr,logArr):
  print(logStr);
  logArr.append(logStr);

def getText(html):
  try:
    reg = re.compile(r'<div.*?id=[\'""]content[\'\"\"]>(?P<TEXT>[\W\w]*?)</div>');
    matched = re.search(reg, html);
    if matched is None:
      return "";
      pass


    text = matched.group('TEXT');
    text = re.sub("<br\s*/>", "\n", text);
    text = re.sub("&nbsp;", " ", text);
    text = text.replace("readx();","");
    text = re.sub("[\\|].*[\\|]","",text);
    text = re.sub("www.*cc","",text);
    pass
  except Exception as e:
    print(e);
    text = "";
    raise
  else:
    pass
  finally:
    pass
  
  return text;

def gethtml(url,count): 
  try:
    response = urllib.request.urlopen(url) 
    html = response.read().decode('utf-8')
    pass
  except Exception as e:
    if count >= 2:
      return "";
      pass
    html = gethtml(url,count+1);
    pass
  else:
    pass
  finally:
    pass
  return html

downloadText();
