#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import urllib.request
import os,sys
import re

baseUrl = "https://www.biquge.cc/html/129/129930/";
log = [];
def downloadText():
  global log;
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
  isFrist = True;
  if not isExists:
    os.makedirs('./txt/都市奇门医生/分章节');
    pass

  html = gethtml(baseUrl,0);
  #进一步处理HTML
  reg = re.compile(r'<div id="list">(?P<HTML>[\w\W]*)</div>');
  matched = re.search(reg, html);
  html = matched.group('HTML');

  #匹配目录文字
  reg = re.compile(r'<a.*href="(?P<URL>.+?)">(?P<NAME>.+?)</a>');
  res = reg.findall(html);
  #打印目录
  printList(res);
  #获取小说章节
  for i in range(len(res)):

    URL = res[i][0];
    NAME = res[i][1];
    NAME = dealName(NAME);
    reg = re.compile(r'(?P<ZHANG>第.*章.*)');
    matched = re.search(reg, NAME);
    if URL is None or NAME is None or matched is None:
      continue;
      pass
    #分章节创建文件
    itemTxtPath = "./txt/都市奇门医生/分章节/"+NAME+".txt";

    if URL.endswith('http'):
      newUrl = URL;
    else:
      newUrl = baseUrl+URL;
    
    text = getText(gethtml(newUrl,0));


    #文件存在(内容不为空) 并且 不是第一次就强制写入
    #判断文件已存在就不覆盖
    if judgeValidItemTxt(itemTxtPath,NAME) and not isFrist and judgeItemTxtEqualNewTxt(itemTxtPath,text):
      printLog(itemTxtPath + ">>文件已存在");
      continue;
      pass


    fm = open(itemTxtPath,'w');
    writeText(fm,text,NAME);
    printLog(str('%.2f' % (float(i)/float(len(res)) * 100)) + "% => "+NAME + "i="+str(i));
    pass

  mergeTxt("./txt/都市奇门医生/分章节/","./txt/都市奇门医生/都市奇门医生-ALL.txt");
  printLog("合并文件 >>> ./txt/都市奇门医生/都市奇门医生-ALL.txt");
  printLog("100%");
  logStr = '\n'.join(log);
  fm = open("./txt/都市奇门医生/都市奇门医生.log",'w');
  fm.write(logStr);
  fm.close();
  return;

def judgeValidItemTxt(itemTxtPath,NAME):
  itemTxtExists = os.path.exists(itemTxtPath);
  if itemTxtExists:
    fm = open(itemTxtPath,'r');
    itemTxt = fm.read();
    fm.close();
    return len(itemTxt) != 0 and itemTxt != "\n=========="+NAME+"==========\n";
  else:
    return False;
    pass

def judgeItemTxtEqualNewTxt(itemTxtPath,newTxt):
  itemTxtExists = os.path.exists(itemTxtPath);
  if itemTxtExists:
    fm = open(itemTxtPath,'r');
    itemTxt = fm.read();
    fm.close();
    return  itemTxt == newTxt;
    pass 
  return False;

def mergeTxt(itemTxtPath,allTxtPath):
  global log;
  allFm = open(allTxtPath,'w');
  allFm.close();
  path = os.listdir(itemTxtPath);
  path.sort();
  for p in path:
    arr = os.path.splitext(p);
    if arr[-1].lower() == ".txt":

      itemFm = open(itemTxtPath+p,"r");
      itemTxt = itemFm.read();
      itemFm.close();
      itemTxt = re.sub("[^=]第.*章.+[\n]","",itemTxt);
      itemTxt = re.sub("=+第.*=", arr[0], itemTxt);
      # itemTxt = itemTxt.replace("==========","");
      if len(itemTxt)<100 :
        printLog(itemTxtPath + ">>文件可能存在问题!!");
        pass
      allFm = open(allTxtPath,'a');
      allFm.write(itemTxt);
      allFm.close();
      pass
    pass
  return;

def printList(res):
  global log;
  printLog("============目录============");
  for i in range(len(res)):
    URL = res[i][0];
    NAME = res[i][1];
    reg = re.compile(r'(?P<ZHANG>第.*章.*)');
    matched = re.search(reg, NAME);
    if URL is None or NAME is None or matched is None:
      continue;
      pass
    NAME = dealName(NAME);
    log.append(NAME + " i = " + str(i));
    print(NAME + " i = " + str(i));
    pass
  printLog("============目录============");
  return;

def dealName(NAME):
  reg = re.compile(r'(?P<ZHANG>第.*章.*)');
  matched = re.search(reg, NAME);
  if not matched is None:
    NAME = str(matched.group('ZHANG'));
    pass

  reg = re.compile(r'(?P<NUM>[0-9]\d*)');
  matched = re.search(reg, NAME);
  NUM = "";
  if not matched is None:
    NUM = str(matched.group('NUM'));
    NAME = NAME.replace(NUM,"");
    pass

  NAME = NAME.replace("第","");
  NAME = NAME.replace("章","");
  NAME = NAME.replace(" ","");

  NAME = "第" + str(NUM.zfill(5)) + "章 " + NAME;
  return NAME;

def writeText(fm,text,name):
  fm.write("\n=========="+name+"==========\n");
  fm.write(text);
  fm.close();

def printLog(logStr):
  global log;
  print(logStr);
  log.append(logStr);

def getText(html):

  try:
    reg = re.compile(r'<div.*id="content">(?P<TEXT>[\w\W]*?)</div>[^<]');
    matched = re.search(reg, html);
    if matched is None:
      return "";
      pass


    text = matched.group('TEXT'); 

    text = text.replace("&lt;","<");
    text = text.replace("&gt;",">");
    text = re.sub("<br\s*[/]?>", "\n", text);
    text = re.sub("&nbsp;", " ", text);
    text = re.sub("<.*?>","",text);
    text = re.sub("热门推荐","",text);
    text = re.sub("\w+\(\)[;]","",text);
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
