'''
@Author: dongry
@Date: 2020-06-17 21:37:04
@LastEditTime: 2020-07-02 10:28:15
@Description: 
@FilePath: \docommit\crtMd.py
'''
import lib.StringLib as slib
import lib.debugLib as dlib 
import lib.FileLib as flib
import codeModels as cm
import sys
import os

def codeParser(vcode,keyWords=[]):
    '''
    @description: 代码分析主进程    \n
    @param vcode {type string} 代码 \n  
    @param keyWords {type list} 需要分析的关键字类型 \n
    @return: 分析后的代码对象列表
    '''
    findStart=0
    modId=0
    findList=[{"type":"head","start":findStart,"mod_id":modId}]
    codeObjList=[]

    #把数据整理到findList中
    while True:
        nearPos=-1
        nearKey=""
        
        for key in keyWords:
            tmpPos=vcode.find(key+" ",findStart)
            if nearPos<0 or (tmpPos>0 and nearPos>tmpPos):
                nearPos=tmpPos
                nearKey=key

        if nearPos==-1:
            findList[-1]["end"]=len(vcode)
            findList[-1]["code_bracket"]=vcode[findList[-1]["start"]:findList[-1]["end"]]
            break
        else:
            findList[-1]["end"]=vcode[:nearPos].rfind("\n")
            findList[-1]["code_bracket"]=vcode[findList[-1]["start"]:findList[-1]["end"]]
            
            defineLine=vcode[findList[-1]["end"]+1:vcode.find(":",nearPos)]
            modId=modId+1
            findList.append({"type":nearKey,"start":nearPos,"mod_id":modId,"define_line":defineLine})

            findStart=nearPos+len(nearKey)
    
    # 将findlist整理成codeObjList对象列表
    codeMod=sys.modules["codeModels"]
    for codeDict in findList:
        className=codeDict["type"]+"Model"
        newClass=getattr(codeMod,className)
        codeObjList.append(newClass(codeDict))
        
    # 计算其从属关系
    parentList=[]
    for codeObj in codeObjList:
        if not parentList or codeObj.mod_level>=len(parentList):
            parentList.append(codeObj.mod_id)
        else:
            parentList[codeObj.mod_level]=codeObj.mod_id
            
        if codeObj.mod_level==0:
            codeObj.mod_parent_id=0
        else:
            codeObj.mod_parent_id=parentList[codeObj.mod_level-1]
            codeObj.mod_parent_name=codeObjList[codeObj.mod_parent_id].mod_name

    return codeObjList

def crtMd(objList):
    '''
    @description: 通过codeObj的数据生成markdown文件
    @param objList {type list} 代码对象的list 
    @return: 无
    '''    
    mdStr=""
    mdTableStr=""

    for obj in objList:
        mdStr=mdStr+obj.crtMd()
        mdTableStr=mdTableStr+obj.mdTable()

    mdStr=mdStr.replace("DocumentInformationEnd","__代码结构:__\n"+mdTableStr+"***")
    return mdStr
    
def makeDocument(sPath,dPath):
    '''
    @description:分析源目录下所有python文件，生成md文件保存在目标目录下 
    @param sPath {type string} 需要分析的源路径
    @param dPath {type string} 文档文件生成的目标路径 
    @return: 无
    '''
    suffix=".py"

    # 生成目录下的py文件绝对路径列表
    files=flib.getFiles(sPath,suffix)
    codeDir=dPath+os.sep+"code"
    docDir=dPath+os.sep+"doc"
    
    # 生成文件相对路径列表
    relFiles=[]
    relDocs=[]
    
    for file in files:
        relFiles.append(os.path.relpath(file,sPath))
    relDocs=list(map(lambda x: slib.rReplace(x,suffix,".md",1),relFiles))
    
    # 生成复制源文件，目标路径对list    
    copyList=list(zip(files,[os.path.join(codeDir,file) for file in relFiles]))
    docList=list(zip(files,[os.path.join(docDir,file) for file in relDocs]))
    

    # 复制文件
    for sourceFile,destFile in copyList:
        flib.copyFile(sourceFile,destFile)
    
    # 生成对应文本文档    
    for sourceFile,destFile in docList:
        codeFp=open(sourceFile,encoding="utf-8")
        context=codeFp.read()
        
        objList=codeParser(context,keyWords=["class","def"])
        mdStr=crtMd(objList)
        
        newDir=os.path.dirname(destFile)
        if not os.path.exists(newDir):
            os.makedirs(newDir)
        
        mdFp=open(destFile,"w",encoding="utf-8")
        mdFp.write(mdStr)

        mdFp.close
        codeFp.close

def main():
    '''
    @description:主控文件接受命令行参数，生成说明文档 
    @usage：pyton crtmd.py sourcefile desctinationfile
    '''
    if os.path.isdir(sys.argv[1]):
        makeDocument(sys.argv[1],sys.argv[2])
    else:
        print("Error:no directory exist-"+sys.argv[1])

if __name__=="__main__":
    main()    