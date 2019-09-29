from django.shortcuts import render
from django.http import JsonResponse
from .models import ModuleName
from .models import ModuleCode
from .models import AddressInfo
from .models import ModuleDataType
from .models import ModuleRqst
from .models import ModuleRspd
from .models import ModuleStruct
from django.db.models import Q
from . import config as c
import win32ui
import re
import xlrd
import struct
from .src import xlsxitem
def index(request, page=None):
    if page != None:
        return render(request, 'index.html', {'page': '/testweb/' + page})
    return render(request, 'index.html', {'page': '/testweb/module'})


def module(request):
    data = ModuleName.objects.all()
    return render(request, 'module.html', {'data': data})


def module_action(request):
    module_name = request.POST.get('modulename', '')
    if len(module_name) == 0:
        return render(request, 'showmsg.html', {'msg': "模块名不能为空"})
    module_id = request.POST.get('moduleid', 0)
    module_des = request.POST.get('moduledes', '')
    if module_id == 0:
        data100 = ModuleName.objects.filter(id=100)
        if data100:
            ModuleName.objects.create(name=module_name, des=module_des)
        else:
            ModuleName.objects.create(id=100, name=module_name, des=module_des)
    else:
        curdata = ModuleName.objects.get(pk=module_id)
        curdata.name = module_name
        curdata.des = module_des
        curdata.save()
    data = ModuleName.objects.all()
    return render(request, 'module.html', {'data': data})


def module_code(request, code=0):
    if code == 0:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})
    data = ModuleCode.objects.filter(classes__id=code)
    return render(request, 'modulecode.html', {'data': data, 'code': code})


def module_code_info(request):
    try:
        type = request.GET.get('type', 0)
        type = int(type)
        module_id = request.GET.get('moduleid', 0)
        pre_wordid = request.GET.get('pre_wordid', 0)
        list = []
        if type == 0:
            data = ModuleDataType.objects.filter(struct_id__exact=0).values('id', 'name')
        else:
            if int(module_id == 0):
                data = ModuleDataType.objects.filter(struct_id__gt=0).values('id', 'name')
            else:
                data = ModuleDataType.objects.filter(struct_id__gt=0).filter(
                    Q(module_id=0) | Q(module_id=module_id)).values('id', 'name')
        if pre_wordid != 0:
            net_data = ModuleRqst.objects.get(word_id=pre_wordid)
            cur_data_type = ModuleDataType.objects.get(id=net_data.word_type)
            if (cur_data_type.struct_id == 0 and type == 0) or (cur_data_type.struct_id > 0 and type > 0):
                list.append({'id': cur_data_type.id, 'content': cur_data_type.name})
            for a in data:
                if a['id'] != cur_data_type.id:
                    list.append({'id': a['id'], 'content': a['name']})
        else:
            for a in data:
                list.append({'id': a['id'], 'content': a['name']})
        return JsonResponse(list, content_type='application/json', safe=False)
    except:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})


def module_code_net_rqst(request, codeid=0):
    try:
        data = ModuleRqst.objects.filter(classes_id=codeid)
        list = []
        for a in data:
            if a.word_struct:
                word_struct = '是'
            else:
                word_struct = '否'
            if a.word_type:
                data_type = ModuleDataType.objects.get(id=a.word_type)
                word_type = data_type.name
            else:
                word_type = ''
            list.append(
                {'word_id': a.word_id, 'word_name': a.word_name, 'word_struct': a.word_struct, 'type': word_type,
                 'codeid': codeid, 'net_type': 0,
                 'word_type': a.word_type, 'word_sort': a.word_sort, 'word_content': a.word_content,
                 'is_struct': word_struct})
        return JsonResponse(list, content_type='application/json', safe=False)
    except:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})


def module_code_net_rspd(request, codeid=0):
    try:
        data = ModuleRspd.objects.filter(classes_id=codeid)
        list = []
        for a in data:
            if a.word_struct:
                word_struct = '是'
            else:
                word_struct = '否'
            if a.word_type:
                data_type = ModuleDataType.objects.get(id=a.word_type)
                word_type = data_type.name
            else:
                word_type = ''
            list.append(
                {'word_id': a.word_id, 'word_name': a.word_name, 'word_struct': a.word_struct, 'type': word_type,
                 'codeid': codeid, 'net_type': 1,
                 'word_type': a.word_type, 'word_sort': a.word_sort, 'word_content': a.word_content,
                 'is_struct': word_struct})
        return JsonResponse(list, content_type='application/json', safe=False)
    except:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})


def module_code_delrqst(request, wordid=0):
    data = ModuleRqst.objects.get(pk=wordid)
    codeid = data.classes_id
    data.delete()
    list = [{'id': codeid, 'type': 0}]
    return JsonResponse(list, content_type='application/json', safe=False)


def module_code_delrspd(request, wordid=0):
    data = ModuleRspd.objects.get(pk=wordid)
    codeid = data.classes_id
    data.delete()
    list = [{'id': codeid, 'type': 1}]
    return JsonResponse(list, content_type='application/json', safe=False)


def module_code_sortnet(request):
    moduleid = request.POST.get('moduleid', 0)
    if moduleid == 0:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})
    data = ModuleCode.objects.filter(classes__id=moduleid)
    code_id = request.POST.get('modulecode_id', 0)
    code_type = request.POST.get('modulecodetype', 0)
    if int(code_type) == 0:
        net_data = ModuleRqst.objects.filter(classes_id=int(code_id))
    else:
        net_data = ModuleRspd.objects.filter(classes_id=int(code_id))
    i = 0
    for item in net_data:
        sortnet = request.POST.get('sortnet' + str(i), '')
        item.word_sort = int(sortnet)
        item.save()
        i = i + 1
    return render(request, 'modulecode.html', {'data': data, 'code': moduleid, 'netid': code_id, 'nettype': code_type})


def module_code_changenet(request):
    try:
        wordid = request.GET.get('wordid', 0)
        wordid = int(wordid)
        if wordid == 0:
            data = ModuleName.objects.all()
            return render(request, 'module.html', {'data': data})
        type = request.GET.get('type', 0)
        if int(type) == 0:
            net_data = ModuleRqst.objects.get(word_id=wordid)
        else:
            net_data = ModuleRspd.objects.get(word_id=wordid)
        code_data = ModuleCode.objects.get(code_id=net_data.classes_id)
        cur_data_type_id = net_data.word_type
        cur_data_type = ModuleDataType.objects.get(id=cur_data_type_id)
        if int(cur_data_type.struct_id) == 0:
            data_type = ModuleDataType.objects.filter(struct_id__exact=0)
        else:
            data_type = ModuleDataType.objects.filter(struct_id__gt=0).filter(
                Q(module_id=0) | Q(module_id=code_data.classes_id))
        # data_type = ModuleDataType.objects.filter(struct_id=cur_data_type.struct_id)
        list = [{'id': cur_data_type.id, 'name': cur_data_type.name}]
        for item in data_type:
            if item.id != cur_data_type.id:
                list.append({'id': item.id, 'name': item.name})
        list.append({'id': -1, 'name': net_data.word_name})
        list.append({'id': -2, 'name': net_data.word_content})
        list.append({'id': -3, 'name': net_data.word_struct})
        return JsonResponse(list, content_type='application/json', safe=False)
    except:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})


def module_code_changenet_action(request):
    try:
        modulenetid = request.POST.get('modulenetid', 0)
        modulenettype = request.POST.get('modulenettype', 0)
        modulenet_name = request.POST.get('modulenet-name', '')
        modulenet_des = request.POST.get('modulenet-des', '')
        net_struct = request.POST.get('net_struct', 0)
        net_type = request.POST.get('net_type', 0)
        if int(modulenettype) == 0:
            net_data = ModuleRqst.objects.get(word_id=modulenetid)
        else:
            net_data = ModuleRspd.objects.get(word_id=modulenetid)
        net_data.word_name = modulenet_name
        net_data.word_content = modulenet_des
        net_data.word_struct = net_struct
        net_data.word_type = net_type
        net_data.save()
        code_id = net_data.classes_id
        module_id = ModuleCode.objects.get(code_id=code_id).classes_id
        data = ModuleCode.objects.filter(classes__id=module_id)
        return render(request, 'modulecode.html',
                      {'data': data, 'code': module_id, 'netid': code_id, 'nettype': modulenettype})
    except:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})


def module_code_action(request):
    module_id = request.POST.get('moduleid', 0)
    if module_id == 0:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})
    data = ModuleCode.objects.filter(classes__id=module_id)
    code_id = request.POST.get('modulecodeid', 0)
    code_name = request.POST.get('modulecodename', '')
    code_des = request.POST.get('modulecodedes', '')
    if code_id == 0:
        id = len(data)
        code_id = int(module_id) * 100 + id
        ModuleCode.objects.create(code_name=code_name, code_des=code_des, code_id=code_id, classes_id=module_id)
    else:
        curdata = ModuleCode.objects.get(code_id=code_id)
        curdata.code_name = code_name
        curdata.code_des = code_des
        curdata.save()
    data = ModuleCode.objects.filter(classes__id=module_id)
    return render(request, 'modulecode.html', {'data': data, 'code': module_id})


def module_code_net(request):
    code_id = request.GET.get('modulecodeid', 0)
    if code_id == 0:
        data = ModuleName.objects.all()
        return render(request, 'module.html', {'data': data})
    code_type = request.GET.get('modulecodetype', 0)

    modulenetname = request.GET.get('modulenetname', '')
    is_struct = request.GET.get('isstruct', '')
    if int(is_struct) == 0:
        is_struct = False
    else:
        is_struct = True
    filed_type = request.GET.get('filedtype', '')
    modulenetdes = request.GET.get('modulenetdes', '')
    if int(code_type) == 0:  # rqst
        ModuleRqst.objects.create(word_name=modulenetname, word_struct=is_struct, word_type=filed_type,
                                  word_content=modulenetdes, classes_id=code_id)
    else:  # rspd
        ModuleRspd.objects.create(word_name=modulenetname, word_struct=is_struct, word_type=filed_type,
                                  word_content=modulenetdes, classes_id=code_id)
    list = [{'id': code_id, 'type': code_type}]
    return JsonResponse(list, content_type='application/json', safe=False)


def module_code_create(request, code=0):
    # c.updateSvn()
    fo = open(c.path + "/rqst/Rqst" + str(code) + '.ts', "w+", encoding='utf-8')
    data = ModuleCode.objects.get(code_id=code)
    rqst_data = ModuleRqst.objects.filter(classes_id=code)
    param = []
    for item in rqst_data:
        data_type = ModuleDataType.objects.get(id=item.word_type)
        param_data = {'netid': data_type.id, 'netname': item.word_name, 'netdes': item.word_content,
                      'nettype': data_type.name, 'sub': []}
        if data_type.struct_id > 1:
            sub_data = ModuleStruct.objects.filter(classes_id=data_type.id)
            for tem in sub_data:
                sub_data_type = ModuleDataType.objects.get(id=tem.struct_type)
                sub_param_data = {'netid': sub_data_type.id, 'netname': tem.struct_name, 'netdes': tem.struct_content,
                                  'nettype': sub_data_type.name}
                param_data['sub'].append(sub_param_data)
        param.append(param_data)

    fo.write(c.getRqst(code, param, data.code_name, data.code_des))
    fo.close()

    fo = open(c.path + "/rspd/Rspd" + str(code) + '.ts', "w+", encoding='utf-8')
    rspd_data = ModuleRspd.objects.filter(classes_id=code)
    param = []
    for item in rspd_data:
        data_type = ModuleDataType.objects.get(id=item.word_type)
        param_data = {'netid': data_type.id, 'netname': item.word_name, 'netdes': item.word_content,
                      'nettype': data_type.name}
        param.append(param_data)
    fo.write(c.getRspd(code, param, data.code_name, data.code_des))
    fo.close()

    module_id = data.classes_id
    # c.submit()
    return render(request, 'showmsg.html', {'msg': "生成成功", 'module_id': module_id})


def struct(request,struct_id = 0):
    data = ModuleDataType.objects.filter(struct_id__gt=1)
    list = []
    for item in data:
        if item.module_id > 0:
            moduleowner = ModuleName.objects.get(id=item.module_id).name
        else:
            moduleowner = '公共'
        list.append({
            'id': item.struct_id, 'name': item.name, 'owner': moduleowner, 'des': item.des, 'ownerid': item.module_id
        })
    return render(request, 'struct.html', {'data': list,'struct_id':struct_id})


def struck_select(request):
    data = ModuleName.objects.all()
    list = [{'id': 0, 'owner': '请选择模块'}]
    for item in data:
        list.append({
            'id': item.id, 'owner': item.name
        })
    return JsonResponse(list, content_type='application/json', safe=False)


def struck_action(request):
    struck_name = request.POST.get('struck_name', '')
    if len(struck_name) == 0:
        return render(request, 'showmsg.html', {'msg': "参数错误"})
    module_id = request.POST.get('add_struck', 0)
    struck_des = request.POST.get('struck_des', '')
    length = len(ModuleDataType.objects.all())
    ModuleDataType.objects.create(name=struck_name, module_id=module_id, des=struck_des, struct_id=length)
    return struct(request)


def struck_revise(request):
    struct_id = request.POST.get('revise_struck_id', 0)
    if int(struct_id) == 0:
        return render(request, 'showmsg.html', {'msg': "参数错误"})
    struck_name = request.POST.get('revise_struck_name', '')
    module_id = request.POST.get('revise_struck_select', 0)
    struck_des = request.POST.get('revise_struck_des', '')
    curdata = ModuleDataType.objects.get(struct_id=struct_id)
    curdata.name = struck_name
    curdata.des = struck_des
    curdata.module_id = module_id
    curdata.save()
    return struct(request)


def struck_revise_select(request, struck_id):
    list = []
    if struck_id > 0:
        cur_data = ModuleName.objects.get(id=struck_id)
        list.append({'id': struck_id, 'owner': cur_data.name})
    data = ModuleName.objects.all()
    list.append({'id': 0, 'owner': '请选择模块'})
    for item in data:
        if item.id != struck_id:
            list.append({
                'id': item.id, 'owner': item.name
            })
    return JsonResponse(list, content_type='application/json', safe=False)


def struck_find(request):
    struck_name = request.POST.get('struck_name', '')
    struck_name = struck_name.lower()
    module_id = int(request.POST.get('find_struck', 0))
    data = ModuleDataType.objects.filter(struct_id__gt=1)
    list = []
    for item in data:
        bool = False
        if len(struck_name) > 0:
            if item.name.lower() == struck_name:
                bool = True
        elif module_id > 0:
            if module_id == item.module_id:
                bool = True
        else:
            bool = True
        if bool:
            if item.module_id > 0:
                moduleowner = ModuleName.objects.get(id=item.module_id).name
            else:
                moduleowner = '公共'
            list.append({
                'id': item.struct_id, 'name': item.name, 'owner': moduleowner, 'des': item.des,
                'ownerid': item.module_id
            })
    return render(request, 'struct.html', {'data': list})


def struck_table_info(request, struck_id):
    data = ModuleDataType.objects.filter(struct_id=struck_id)[0]
    data = ModuleStruct.objects.filter(classes_id=data.id)
    list = []
    for item in data:
        data_type = ModuleDataType.objects.get(id=item.struct_type)
        list.append({
            'id': item.struct_id, 'name': item.struct_name, 'typename': data_type.name, 'des': item.struct_content,
            'sortid': item.struct_sort
        })
    return JsonResponse(list, content_type='application/json', safe=False)


def struck_table_action(request):
    struck_id = request.POST.get('fieldinfo_struckid', 0)
    data = ModuleDataType.objects.filter(struct_id=struck_id)[0]
    struck_name = request.POST.get('fieldinfo_name', '')
    struck_type = request.POST.get('fieldinfo_type', 0)
    struck_des = request.POST.get('fieldinfo_des', '')
    ModuleStruct.objects.create(classes_id=data.id,struct_name= struck_name,struct_type=struck_type,struct_content = struck_des)
    return struct(request,struck_id)

def struck_table_del(request,struck_id = 0):
    data = ModuleStruct.objects.get(struct_id=struck_id)
    data.delete()
    struct_id = data.classes_id
    data = ModuleDataType.objects.filter(id=struct_id)[0]
    return struct(request, data.struct_id)

def struck_table_sort(request):
    struct_id = request.POST.get('fieldinfo_struckid_table',0)
    data = ModuleDataType.objects.get(struct_id=struct_id)
    data = ModuleStruct.objects.filter(classes_id=data.id)
    index = 0
    for item in data:
        sort_id = request.POST.get('sorttable' + str(index),0)
        item.struct_sort = int(sort_id)
        item.save()
        index = index + 1
    return struct(request,struct_id)

def struck_table_revise_info(request, struck_id):
    data = ModuleStruct.objects.get(struct_id=struck_id)
    is_struct = 0
    if data.struct_type > 8:
        is_struct = 1
        data_type = ModuleDataType.objects.filter(struct_id__gt=1)
    else:
        data_type = ModuleDataType.objects.filter(struct_id__exact=0)
    cur_tyoe = ModuleDataType.objects.get(id=data.struct_type)
    list = [{
        'id': -1, 'name': data.struct_name, 'is_struct': is_struct, 'des': data.struct_content,
    }]
    list.append({
        'id':cur_tyoe.id,'name':cur_tyoe.name
    })
    for item in data_type:
        if item.id != cur_tyoe.id:
            list.append({
                'id': item.id, 'name': item.name
            })
    return JsonResponse(list, content_type='application/json', safe=False)

def struck_table_revise(request):
    struct_id = request.POST.get('revise_field_id', 0)
    data = ModuleStruct.objects.get(struct_id=struct_id)
    parent_data = ModuleDataType.objects.get(id=data.classes_id)
    data.struct_name = request.POST.get('revise_field_name', '')
    data.struct_type = request.POST.get('revise_field_type', 0)
    data.struct_content = request.POST.get('revise_field_des', 0)
    data.save()
    return struct(request, parent_data.struct_id)

def struck_creat(request,code = 0):
    # c.updateSvn()
    if code == 0:
        data = ModuleDataType.objects.filter(struct_id__gt=1)
        for item in data:
            struck_creat_write(item.struct_id)
    else:
        struck_creat_write(code)
    # c.submit()
    return render(request, 'showmsg.html', {'msg': "生成成功", 'struck_id': 1})

def struck_creat_write(code):
    cur_data = ModuleDataType.objects.get(struct_id=code)
    fo = open(c.path + "/strucks/Struck" + cur_data.name + '.ts', "w+", encoding='utf-8')
    data = ModuleStruct.objects.filter(classes_id=cur_data.id)
    param = []
    for item in data:
        data_type = ModuleDataType.objects.get(id=item.struct_type)
        param_data = {'netid': data_type.id, 'netname': item.struct_name, 'netdes': item.struct_content,
                      'nettype': data_type.name, 'sub': []}
        if data_type.struct_id > 1:
            sub_data = ModuleStruct.objects.filter(classes_id=data_type.id)
            for tem in sub_data:
                sub_data_type = ModuleDataType.objects.get(id=tem.struct_type)
                sub_param_data = {'netid': sub_data_type.id, 'netname': tem.struct_name, 'netdes': tem.struct_content,
                                  'nettype': sub_data_type.name}
                param_data['sub'].append(sub_param_data)
        param.append(param_data)

    fo.write(c.getStruck(cur_data.name, cur_data.des, param))
    fo.close()


def createdata(request):
    c.zipJsonSubmit()
    return render(request, 'showmsg.html', {'msg': "生成成功", 'page': 1})







def xlsxtable(request):
    return render(request, 'xlsxtable.html')

def xlsxtable_init(request):
    return JsonResponse({'openurl':c.tablepath,'saveurl':c.savepath}, content_type='application/json', safe=False)

def xlsxtable_open(request):
    dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框 0 是另存为
    openurl = request.POST.get('openurl','')
    saveurl = request.POST.get('saveurl', '')
    if len(openurl) == 0:
        dlg.SetOFNInitialDir('E:')  # 设置打开文件对话框中的初始显示目录
    else:
        dlg.SetOFNInitialDir(openurl)  # 设置打开文件对话框中的初始显示目录
    if len(saveurl) > 0:
        c.savepath = saveurl
    flag = dlg.DoModal()
    if 1 == flag:
        filename = dlg.GetPathName()
        filename = str(filename)
        start = filename.rfind('\\')
        end = filename.rfind('.xlsx')
        c.tablepath = filename[0:start]
        file_name = filename[start + 1:end]
        save_name = file_name[0].upper() + file_name[1:] + 'Vo'
        tem = xlrd.open_workbook(filename)
        item = xlsxitem.ItemTool(tem)
        item.tableName = file_name
        c.xlsxdata = item.filtrate()
        return render(request, 'xlsxtable.html',{'filename':file_name,'savename':save_name,'data':c.xlsxdata})
    else:
        print("取消打开文件...")
        return render(request, 'xlsxtable.html')

def xlsxtable_save(request):
    filename = request.POST.get('filename', '')
    savename = request.POST.get('savename', '')
    if len(filename) == 0 or len(savename) == 0:
        return render(request, 'showmsg.html', {'msg': "参数错误或未打开文件", 'page': 2})
    data = c.xlsxdata
    length = len(data)
    for i in range(1,length + 1):
        cur_name = request.POST.get('table' + str(i), '')
        data[i-1].update({'name':cur_name})

    content = c.getTableVo(savename,data)
    fo = open(c.savepath + savename + '.ts', "w+", encoding='utf-8')
    fo.write(content)
    fo.close()
    return render(request, 'showmsg.html', {'msg': "生成成功", 'page': 2})





























def address(request):
    return render(request, 'address.html')


def addressAPI(request, address_id=0):
    try:
        if int(address_id) == -1:
            data = []
        if int(address_id) == 0:
            data = AddressInfo.objects.filter(pid__isnull=True).values('id', 'address')
        else:
            data = AddressInfo.objects.filter(pid_id=int(address_id)).values('id', 'address')
        list = []
        for a in data:
            list.append({'id': a['id'], 'address': a['address']})
        return JsonResponse(list, content_type='application/json', safe=False)
        # return  render(request,'address.html',{'data':list})
    except:
        return render(request, 'address.html')
