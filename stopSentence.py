#coding:utf-8
from bs4 import BeautifulSoup as bs
import re
import sys

def findStopSen(path):
	pf=open(path,'r')
	content=pf.read()
	pf.close()

	content=content.splitlines()
	
	senDict={}
	
	for line in content:
		line =line.split('\t')
		if len(line)<3:
			continue
		line[2]=line[2].replace('<',',<')
		line[2]=line[2].replace('>','>,')
		text=bs(line[2]).get_text()

		text=re.sub('\d+',',',text)
		text=re.sub(u'[\uFF00-\uFFEF]+',',',text)
		
		sepList=[u'，',u'。',u'；',u'“',u'”',u'?',u'《',u'》',u'"',u'（',u'）',u'(',u')',u'-',u'——',u'.',
		u'【',u'】',u',',u'←',u'.',u':',u'[',u']',u'{',u'}',u' ',u'？',u'·',u'、',u'%',u'☆',u'★',u'~',
		u'■',u'*',u'↑',u'!',u'！',u'●']
		rp = '|'.join(map(re.escape, sepList))
		#rp = re.compile(r"[，。；“”?《》\"（）()-——.【】,←.:\[\]{}？·、]")
		
		senList=re.split(rp,text)
		for se in senList:
			if se==None:
				continue
			se=se.strip()
			if se=='':
				continue
			se=se.encode('utf-8')
			if se in senDict:
				senDict[se]+=1
			else:
				senDict[se]=1

	pf=open('rawSta.txt','w+')
	for k,v in senDict.items():
		if v>1:
			wStr=k+'\t'+str(v)+'\n'
			pf.write(wStr)
	pf.close()


def sortSen(path='rawSta.txt'):
	pf=open(path,'r')
	content=pf.read()
	pf.close()

	content=content.splitlines()

	senList=[]

	for line in content:
		line=line.split('\t')
		line[1]=line[1].strip()
		if int(line[1])>70 and len(line[0])>12:
			senList.append((line[0],int(line[1])))

	senList.sort(key=lambda x:x[1],reverse=True)

	pf=open('st1.txt','w+')
	for ks in senList:
		wStr=ks[0]+'\t'+str(ks[1])+'\n'
		pf.write(wStr)

	pf.close()


	

findStopSen(sys.argv[1])
sortSen()

