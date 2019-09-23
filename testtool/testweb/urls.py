from django.urls import path,re_path
from . import views
from . import config

app_name = '[testweb]'
config.getPath()
urlpatterns = [
    path('index/', views.index,name='index'),
    path('index/<str:page>', views.index, name='index_page'),

    path('module/', views.module, name='module'),#模块的协议列表
    path('module/action', views.module_action, name='module_action'),#添加模块
    path('module/code<int:code>', views.module_code, name='module_code'),#单个模块的协议列表
    path('module/code', views.module_code_action, name='module_code_action'),#添加协议
    path('module/code/', views.module_code_info, name='module_code_info'),#checkbox 选择框的变化
    path('module/code/rqst<int:codeid>', views.module_code_net_rqst, name='module_code_net_rqst'),#rqst 数据表的信息
    path('module/code/rspd<int:codeid>', views.module_code_net_rspd, name='module_code_net_rspd'),#rspd 数据表的信息
    path('module/code/net', views.module_code_net, name='module_code_net'),# net协议字段的生成
    path('module/code/delrqst<int:wordid>', views.module_code_delrqst, name='module_code_delrqst'),#rqst 删除某个字段
    path('module/code/delrspd<int:wordid>', views.module_code_delrspd, name='module_code_delrspd'),  # rspd 删除某个字段
    path('module/code/sortnet', views.module_code_sortnet, name='module_code_sortnet'),#字段排序
    path('module/code/changenet', views.module_code_changenet, name='module_code_changenet'),#修改字段信息
    path('module/code/changenet/action', views.module_code_changenet_action, name='module_code_changenet_action'),#修改字段
    path('module/code/crate<int:code>', views.module_code_create, name='module_code_create'),#生成文件

    path('struct/', views.struct, name='struct'),#结构体列表
    path('struct/select', views.struck_select, name='struck_select'),#选择框信息获取
    path('struct/action', views.struck_action, name='struck_action'),#添加
    path('struct/find', views.struck_find, name='struck_find'),
    path('struct/revise', views.struck_revise, name='struck_revise'),
    path('struct/revise/select<int:struck_id>', views.struck_revise_select, name='struck_revise_select'),
    path('struct/table/info<int:struck_id>', views.struck_table_info, name='struck_table_info'),
    path('struct/table/action', views.struck_table_action, name='struck_table_action'),
    path('struct/table/del<int:struck_id>', views.struck_table_del, name='struck_table_del'),
    path('struct/table/sort', views.struck_table_sort, name='struck_table_sort'),
    path('struct/table/revise<int:struck_id>', views.struck_table_revise_info,name='struck_table_revise_info'),
    path('struct/table/revise/', views.struck_table_revise,name = 'struck_table_revise'),
    path('struct/crate<int:code>', views.struck_creat, name='struck_creat'),

    path('createdata/', views.createdata, name='createdata'),#结构体列表
    # test
    path('address/', views.address, name='address'),
    path('address/<int:address_id>', views.addressAPI, name='address'),
]
