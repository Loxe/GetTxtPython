#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import urllib.request
import os,sys
import re

baseUrl = "http://m.sangwu.org/book/1/1852/";
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
  html = gethtml(baseUrl);
  reg = re.compile(r'<li><a href="(?P<URL>.+)">(?P<NAME>.+)<span></span></a></li>');
  res = reg.findall(html);
  #打印目录
  printList(res,log);

  #获取小说章节
  for i in range(len(res)):

    URL = res[i][0];
    NAME = res[i][1];
    NAME = "第"+ NAME.split("第")[-1];

    if URL.endswith('http'):
      newUrl = URL;
    else:
      newUrl = baseUrl+URL;
    
    text = getText(gethtml(newUrl)); 
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
    NAME = "第"+ NAME.split("第")[-1];
    log.append(NAME + " i = " + str(i));
    print(NAME + " i = " + str(i));
    pass
  printLog("============目录============",log);

def writeText(fm,text,name):
  fm.write("\n=========="+name+"==========\n");
  fm.write(text);
  fm.close();

def printLog(logStr,logArr):
  print(logStr);
  logArr.append(logStr);

def getText(html):
  try:
    reg = re.compile(r'<div class="txt" id="txt">(?P<TEXT>.*)</div>');
    matched = re.search(reg, html);
    if matched is None:
      return "";
      pass
    text = matched.group('TEXT');
    text = text.replace("&nbsp;"," ");
    text = text.replace("<br />","\n");
    text = text.replace("【如遇网页无法打开,请开启手机的飞行模式，然后关闭,换个IP即可】","");
    text = text.replace("【其他情况无法打开网站,请开启手机的飞行模式，然后关闭,换个IP即可】","");
    text = text.replace("<font color=red><b>【请记住本站网址：m.sangwu.org】UC浏览器用户如遇到无法访问，请把设置里面极速省流的【云加速】关闭,</b></font>","");
    pass
  except Exception as e:
    text = "";
    raise
  else:
    pass
  finally:
    pass
  
  return text;

def gethtml(url): 
  try:
    response = urllib.request.urlopen(url) 
    html = response.read().decode('gbk')
    pass
  except Exception as e:
    html = "";
    pass
  else:
    pass
  finally:
    pass
  return html

downloadText();
