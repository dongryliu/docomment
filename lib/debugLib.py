'''
@Author: dongry
@Date: 2020-06-30 09:01:03
@LastEditTime: 2020-06-30 10:11:05
@LastEditors: Please set LastEditors
@Description: 一些调试用工具
@FilePath: \docommit\lib\debugLib.py
'''
def oprint(obj):
    '''
    @description:打印对象中所有变量 \n 
    @param obj {type object} 对象 \n
    @return: 无
    ''' 
    print ('\n'.join(['%s:%s' % item for item in obj.__dict__.items()])) 