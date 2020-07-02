'''
@Author: your name
@Date: 2020-06-18 15:17:21
@LastEditTime: 2020-07-01 23:36:47
@LastEditors: Please set LastEditors
@Description: 处理字符串的应用库
@FilePath: \docommit\lib\StringLib.py
'''

def findSubStrs(vString,subStr):
    '''
    @description:查找字符串中中所有子字符串的位置 \n
    @param vString {type string} 整个字符串     \n
    @param subStr {type string} 要查找的子字符串  \n
    @return: 所有子字符串起始位置的列表，没有找到为空 \n
    '''
    findStart=0
    foundList=[]
    
    findLoc=vString.find(subStr,findStart)
    while findLoc>=0:
        foundList.append(findLoc)
        findStart=findLoc+len(subStr)
        findLoc=vString.find(subStr,findStart)
    
    return foundList

def findBracket(vString,startB,endB):
    '''
    @description:取整个字符串中，开始结束标志的中间字符串 \n
    @param vString {type string} 整个字符串     \n
    @param startB {type string} 开始标志  \n
    @param startB {type string} 结束标志  \n
    @return: 子字符串    
    '''
    rtnStr=""
    startPos=vString.find(startB)
    if startPos>=0:    
        endPos=vString.find(endB,startPos+len(startB))
        if endPos>=0:
            rtnStr=vString[startPos+len(startB):endPos]
    return rtnStr         
        

def findKeyWords(vString,keyWords=[],findList=[],findStart=0):
    '''
    @description: 找到字符串中包含的所有子字符串，并返回按先后排序的子字符串和位置的列表 \n
    @param vString {type string} 字符串 \n
    @param keyWords {type list} 需要查找的子字符合集 \n
    @param findList {type list} 初始为空，运行结束为查找结果的List \n
    @param findStart {type int} 查找的起始位置 \n
    @return: 无
    '''
    # print(keyWords)
    nearPos=-1
    nearKey=""
        
    for key in keyWords:
        tmpPos=vString.find(key,findStart)
        if nearPos<0 or (tmpPos>0 and nearPos>tmpPos):
            nearPos=tmpPos
            nearKey=key

    if nearPos==-1:
        return
    else:
        findList.append({nearKey:nearPos})
        findKeyWords(vString,keyWords,findList,nearPos+len(nearKey))

def lineStrip(vString):
    '''
    @description:去除每行前后的空格制表格等 
    @param vString {type string} 含有多行的字符串 
    @return: 去除空格制表格等后的字符串集
    '''
    lines=vString.split("\n")
    return "\n".join(map(lambda x: x.strip(),lines))

def rReplace(self,old,new,max=0):
    '''
    @description:从右面替换字符串
    @param old {type string} 原字符串
    @param new {type string} 替换成字符串
    @param max {type int} 最大替换数
    @return: 新生成的字符串
    '''
    count=max if max>0 else len(self)
    return new.join(self.rsplit(old,count))
        

if __name__=="__main__":
    line="""adb
       credits
       edf
    ab"""
    commSign=r"'''"
    print(line.rReplace("a","f",1))