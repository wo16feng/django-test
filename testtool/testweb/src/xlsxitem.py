from struct import *
from .. import config as c

import sys
import encodings

class ItemTool(object):
    def __init__(self, cur):
        self.cur = cur
        self.table = self.cur.sheet_by_index(0)
        self.nrows = self.table.nrows  # 获取table工作表总行数
        self.ncols = self.table.ncols  # 获取table工作表总列数

    def filtrate(self):
        print("sheetName:" + self.tablename + "行数：" + repr(self.nrows) + "列数：" + repr(self.ncols))
        list = []
        i = 0
        while i < self.ncols:
            xssfCol = self.table.col_values(i)
            if xssfCol == None:
                print("空列跳出了！！！"+i)
                break
            if str(xssfCol[0]).find('c') != -1:
                value_name = xssfCol[3]
                value_des = xssfCol[4]
                value_type = xssfCol[1]
                list.append({'name':value_name,'des':value_des,'type':value_type,'id':len(list) + 1})
            print(xssfCol[0])
            i = i + 1
        return list
    @property
    def tableName(self):
        return self.tablename
    @tableName.setter
    def tableName(self,name):
        self.tablename = name

    data = None
