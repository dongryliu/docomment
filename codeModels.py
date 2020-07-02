#coding=utf-8
'''
@Author: dongry
@Date: 2020-06-28 16:51:59
@LastEditTime: 2020-07-02 12:20:55
@Description: 声明各种代码类
@FilePath: \docommit\codeModels.py
'''
import lib.StringLib as slib

class baseModel():
    '''
    @description:代码对象基类 
    '''
    def __init__(self,vDict={}):
        self.mod_type=""     # 类型
        self.mod_name=""     # 名称
        self.mod_id=-1       # id
        self.mod_level=-1    # 层级
        self.mod_parent_id=-1   # 父节点id
        self.mod_parent_name="" # 父节点名称 
        self.mod_define_line="" # 定义行
        self.mod_comment=""     # 注释内容
        self.mod_codeBracket="" # 代码块
    
    def _getLevel(self):
        '''
        @description:根据defineLine 分析该节点层级
        @return 返回层级 
        '''
        rtnLevel=0
        i=1
        if self.mod_define_line[0]==" ": 
            while self.mod_define_line[i]==" ":
                i=i+1
            rtnLevel=i//4
        elif self.mod_define_line[0]=='\t':
            while self.mod_define_line[i]=='\t':
                i=i+1
            rtnLevel=i
        return rtnLevel
    
    def _findComment(self):
        self.mod_comment=slib.lineStrip(slib.findBracket(self.mod_codeBracket,r"'''",r"'''").strip())
    
    def mdTable(self):
        return ""
           
class classModel (baseModel):
    '''
    @description:类模型 
    '''    
    def __init__(self,vDict={}):
        self.mod_type="class"
        self.mod_id=vDict["mod_id"]
        self.mod_level=0
        self.mod_parent_id=0
        self.mod_info={"father_class":""}
        self.mod_define_line=vDict["define_line"]
        self.__parserDefineLine()
        self.mod_codeBracket=vDict["code_bracket"]
        self._findComment()
    
    def __parserDefineLine(self):
        self.mod_name=self.mod_define_line[self.mod_define_line.find("class"+" ")+6:self.mod_define_line.find("(")].strip()
        fatherClasses=self.mod_define_line[self.mod_define_line.find("(")+1:self.mod_define_line.find(")")].strip()
        self.mod_info["father_class"]=fatherClasses

    def crtMd(self):
        rtnStr="# "+self.mod_name+"类\n"
        rtnStr=rtnStr+"- 父类："+self.mod_info["father_class"]
        return rtnStr+"\n- "+self.mod_comment.replace("\n","\n- ")+"\n\n"
    
    def mdTable(self):
        rtnStr="- ["+self.mod_name+"类](#"+self.mod_name+"类)\n"
        return rtnStr

class headModel(baseModel):
    '''
    @description: 开头类型 
    '''
    def __init__(self,vDict={}):
        self.mod_type="head"
        self.mod_id=vDict["mod_id"]
        self.mod_level=0
        self.mod_parent_id=0
        self.mod_codeBracket=vDict["code_bracket"]
        self._findComment()

    def crtMd(self):
        return "__文件信息:__\n- "+self.mod_comment.replace("\n","\n- ")+"\n\n"+"DocumentInformationEnd\n"
    
class defModel(baseModel):
    '''
    @description: 函数类型 
    '''
    def __init__(self,vDict={}):
        self.mod_type="def"
        self.mod_id=vDict["mod_id"]
        self.mod_info={"vars":""}
        self.mod_define_line=vDict["define_line"]
        self.__parserDefineLine()
        self.mod_codeBracket=vDict["code_bracket"]
        self._findComment()
        self.mod_level=self._getLevel()

    def __parserDefineLine(self):
        self.mod_name=self.mod_define_line[self.mod_define_line.find("def"+" ")+4:self.mod_define_line.find("(")].strip()
        vars=self.mod_define_line[self.mod_define_line.find("(")+1:self.mod_define_line.find(")")].strip()
        self.mod_info["vars"]=vars
    
    def crtMd(self):
        if self.mod_level>0:
            nameStr=self.mod_parent_name+":"+self.mod_name
        else:
            nameStr=self.mod_name
        rtnStr="#"*(self.mod_level+1)+" "+nameStr+"函数\n"
        rtnStr=rtnStr+"- 参数："+self.mod_info["vars"]
        return rtnStr+"\n- "+self.mod_comment.replace("\n","\n- ")+"\n\n"
    
    def mdTable(self):
        if self.mod_level>0:
            nameStr=self.mod_parent_name+":"+self.mod_name
        else:
            nameStr=self.mod_name
        rtnStr="  "*self.mod_level+"- ["+nameStr+"函数](#"+nameStr+"函数)\n"
        return rtnStr