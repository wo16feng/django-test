import os

path = ''
zippath = ''
uipath = ''

tablepath = ''
savepath = ''
xlsxdata = []

def updateSvn():
    if len(path) == 0:
        getPath()
    os.system('cd /d ' + path + '&& svn update')
    # os.system('cd /d ' + zippath + '&& svn update')


def submit():
    if len(path) == 0:
        getPath()
    os.system("cd /d " + path + "&& svn commit -m 提交表格")
    # os.system("cd /d " + zippath + "&& svn commit -m 提交表格数据")

def zipJsonSubmit():
    if len(path) == 0:
        getPath()
    os.system('start ' + zippath + 'zlib.bat')
    os.system('start ' + uipath + 'zcopy.bat')
    # os.system("cd /d " + zippath + "&& svn commit -m 提交表格数据")

def getPath():
    fo = open(os.getcwd() + "/testweb/config.txt", "r+")
    global path
    path = fo.__next__()[5:].splitlines()[0]
    global zippath
    zippath = fo.__next__()[8:].splitlines()[0]
    global uipath
    uipath = fo.__next__()[7:].splitlines()[0]
    global tablepath
    tablepath = fo.__next__()[9:].splitlines()[0]
    global savepath
    savepath = fo.__next__()[9:].splitlines()[0]
    print(path, zippath,uipath)
    fo.close()


def getRqst(codeid, param, name, des):
    content = '/*本文件由程序自动生成，请勿手动修改      协议名字：' + name + '备注：' + des + '*/\r'
    content += 'export default class Rqst' + str(codeid) + ' extends PacketBase{\r'
    content += '    constructor('
    array = []
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += item['netname'] + ':string,'
        elif netid < 8:
            content += item['netname'] + ':number,'
        else:
            content += item['netname'] + ':Array<Struck' + item['nettype'] + '>,'
            array.append('Struck' + item['nettype'])
    content = content[:-1]
    content += '){\r'
    content += '        super();\r'
    content += '        this.writeHead(' + str(codeid) + ');//写入协议号\r'
    bool = False
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += '        ' + 'this.bytes.writeUTFString(' + item['netname'] + ');    // ' + item[
                'netdes'] + '\r'
        elif netid == 1 or netid == 5:
            content += '        ' + 'this.bytes.writeUint8(' + item['netname'] + ');    // ' + item['netdes'] + '\r'
        elif netid == 2:
            content += '        ' + 'this.bytes.writeUint16(' + item['netname'] + ');    // ' + item['netdes'] + '\r'
        elif netid == 3 or netid == 4:
            content += '        ' + 'this.bytes.writeUint32(' + item['netname'] + ');    // ' + item['netdes'] + '\r'
        elif netid == 7:
            content += '        ' + 'Tools.writeQword(this.bytes,' + item['netname'] + ');    // ' + item[
                'netdes'] + '\r'
            bool = True
        else:
            content += '        ' + 'this.bytes.writeUint16(' + item['netname'] + '.length);    // ' + item[
                'netdes'] + '\r'
            content += '        ' + 'for (var index = 0; index < ' + item['netname'] + '.length; index++){\r'
            sub_param = item['sub']
            for tem in sub_param:
                netid = int(tem['netid'])
                if netid == 6 or netid == 0 or netid == 8:
                    content += '            ' + 'this.bytes.writeUTFString(' + item['netname'] + '.' + tem[
                        'netname'] + ');\r'
                elif netid == 1 or netid == 5:
                    content += '            ' + 'this.bytes.writeUint8(' + item['netname'] + '.' + tem[
                        'netname'] + ');\r'
                elif netid == 2:
                    content += '            ' + 'this.bytes.writeUint16(' + item['netname'] + '.' + tem[
                        'netname'] + ');\r'
                elif netid == 3 or netid == 4:
                    content += '            ' + 'this.bytes.writeUint32(' + item['netname'] + '.' + tem[
                        'netname'] + ');\r'
                elif netid == 7:
                    content += '            ' + 'Tools.writeQword(this.bytes,' + item['netname'] + '.' + tem[
                        'netname'] + ');\r'
                    bool = True
            content += '        }\r'
    for item in array:
        content = 'import ' + item + ' from "../strucks/' + item + '";\r' + content
    if bool:
        content = 'import PacketBase from "../PacketBase";\rimport Tools from "../../utils/Tools";\r' + content
    else:
        content = 'import PacketBase from "../PacketBase";\r' + content

    content += '    }\r'
    content += '}\r'
    return content


def getRspd(codeid, param, name, des):
    content = '/*本文件由程序自动生成，请勿手动修改      协议名字：' + name + '备注：' + des + '*/\r'
    content += 'export default class Rspd' + str(codeid) + ' extends PacketBase{\r'
    array = []
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += '    public ' + item['netname'] + ':string;    // ' + item['netdes'] + '\r'
        elif netid < 8:
            content += '    public ' + item['netname'] + ':number    // ' + item['netdes'] + '\r'
        else:
            content += '    public ' + item['netname'] + ':Array<Struck' + item['nettype'] + '>;    // ' + item['netdes'] + '\r'
            array.append('Struck' + item['nettype'])
    content += '    constructor(){\r        super();\r    }\r'
    content += '    public readFromByte(bytes:laya.utils.Byte){\r'

    bool = False
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += '        this.' + item['netname'] + ' = bytes.getString();\r'
        elif netid == 1 or netid == 5:
            content += '        this.' + item['netname'] + ' = bytes.getUint8();\r'
        elif netid == 2:
            content += '        this.' + item['netname'] + ' = bytes.getUint16();\r'
        elif netid == 3 or netid == 4:
            content += '        this.' + item['netname'] + ' = bytes.getUint32();\r'
        elif netid == 7:
            content += '        this.' + item['netname'] + ' = Tools.readQword(bytes);\r'
            bool = True
        else:
            content += '        this.' + item['netname'] + ' = [];\r'
            content += '        var ' + item['netname'] + 'Size:number = bytes.getUint16();\r'
            content += '        for(var index = 0; index < ' + item['netname'] + 'Size; index++){\r'
            struct_name = item['nettype'][:1].lower() + item['nettype'][1:]
            content += '            var ' + struct_name + ':Struck' + item['nettype'] + '= new Struck' + item['nettype'] + ';\r'
            content += '            ' + struct_name + '.readFromByte(bytes);\r'
            content += '            this.' + item['netname'] + '.push(' + struct_name + ');\r'
            content += '        }\r'
    for item in array:
        content = 'import ' + item + ' from "../strucks/' + item + '";\r' + content
    if bool:
        content = 'import PacketBase from "../PacketBase";\rimport Tools from "../../utils/Tools";\r' + content
    else:
        content = 'import PacketBase from "../PacketBase";\r' + content

    content += '    }\r'
    content += '}\r'
    return content

def getStruck(name,des,param):
    content = '/*本文件由程序自动生成，请勿手动修改      ' + '备注：' + des + '*/\r'
    content += 'export default class Struck' + str(name) + '{\r'
    array = []
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += '    public ' + item['netname'] + ':string;    // ' + item['netdes'] + '\r'
        elif netid < 8:
            content += '    public ' + item['netname'] + ':number    // ' + item['netdes'] + '\r'
        else:
            content += '    public ' + item['netname'] + ':Array<Struck' + item['nettype'] + '>;    // ' + item[
                'netdes'] + '\r'
            array.append('Struck' + item['nettype'])
    content += '    constructor(){\r    }\r'
    content += '    public readFromByte(bytes:laya.utils.Byte){\r'

    bool = False
    for item in param:
        netid = int(item['netid'])
        if netid == 6 or netid == 0 or netid == 8:
            content += '        this.' + item['netname'] + ' = bytes.getString();\r'
        elif netid == 1 or netid == 5:
            content += '        this.' + item['netname'] + ' = bytes.getUint8();\r'
        elif netid == 2:
            content += '        this.' + item['netname'] + ' = bytes.getUint16();\r'
        elif netid == 3 or netid == 4:
            content += '        this.' + item['netname'] + ' = bytes.getUint32();\r'
        elif netid == 7:
            content += '        this.' + item['netname'] + ' = Tools.readQword(bytes);\r'
            bool = True
        else:
            content += '        this.' + item['netname'] + ' = [];\r'
            content += '        var ' + item['netname'] + 'Size:number = bytes.getUint16();\r'
            content += '        for(var index = 0; index < ' + item['netname'] + 'Size; index++){\r'
            struct_name = item['nettype'][:1].lower() + item['nettype'][1:]
            content += '            var ' + struct_name + ':Struck' + item['nettype'] + '= new Struck' + item[
                'nettype'] + ';\r'
            content += '            ' + struct_name + '.readFromByte(bytes);\r'
            content += '            this.' + item['netname'] + '.push(' + struct_name + ');\r'
            content += '        }\r'
    for item in array:
        if item !=  'Struck'+ name:
            content = 'import ' + item + ' from "../strucks/' + item + '";\r' + content
    if bool:
        content = 'import PacketBase from "../PacketBase";\rimport Tools from "../../utils/Tools";\r' + content
    else:
        content = 'import PacketBase from "../PacketBase";\r' + content

    content += '    }\r'
    content += '}\r'
    return content


def getTableVo(name,data):
    content = 'export default class '+ name +' implements IByteReader{\r'

    for item in data:
        if item.get('type') == 'string':
            content += '    public ' + item['name'] + ':string;    // ' + item['des'] + '\r'
        else:
            content += '    public ' + item['name'] + ':number    // ' + item['des'] + '\r\r'
    content += '    constructor(){\r    }\r\r'
    content += '    public readFromByte(bytes:laya.utils.Byte){\r'
    for item in data:
        if item.get('type') == 'string':
            content += '        this.' + item['name'] + ' = bytes.getString();\r'
        elif item.get('type') == 'byte':
            content += '        this.' + item['name'] + ' = bytes.getUint8();\r'
        elif item.get('type') == 'short':
            content += '        this.' + item['name'] + ' = bytes.getUint16();\r'
        elif item.get('type') == 'int':
            content += '        this.' + item['name'] + ' = bytes.getUint32();\r'
    content += '    }\r'
    content += '}\r'
    return content