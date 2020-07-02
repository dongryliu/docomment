'''
@Author: dongry
@Date: 2020-06-20 10:51:48
@LastEditTime: 2020-06-22 13:38:57
@LastEditors: Please set LastEditors
@Description: 升级的文件操作
@FilePath: \docommit\lib\FileLib.py
'''
#coding=utf-8

import os
import shutil


def getFiles(path, suffix):
    '''
    @description:返回给定路径下，指定扩展名的所有文件 \n 
    @param path {type string} 搜索路径  \n
    @param suffix {type string} 文件扩展名  \n   
    @return: 文件路径list
    '''
    return [os.path.join(root,file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]

def copyFile(soureFile,destFile):
    '''
    @description:将源文件复制到目标文件，如果目标目录结构不存在，就创建后复制 \n
    @param sourceFile {type string} 源文件  \n
    @param destFile {type string} 目标文件  \n
    @return:无 
    ''' 
    newDir=os.path.dirname(destFile)
    if not os.path.exists(newDir):
        os.makedirs(newDir)

    shutil.copyfile(soureFile,destFile)



if __name__=="__main__":
    pass
    # i=0
    # for root,dirs,files in os.walk("."):
    #     i=i+1
    #     for name in files:
    #         if name.endswith("py"):
    #             print(root," ",name)
    # f=io.StringIO()
    # help=pydoc.Helper(output=f)
    # help.help("ParserLib") 
    # print(f.getvalue())
    # print(getFiles(r"/home/ml","py"))