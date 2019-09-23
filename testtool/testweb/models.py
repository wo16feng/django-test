from django.db import models
from django.db.migrations import migration
class ModuleName(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True,verbose_name='ID')
    name = models.CharField(max_length=32)
    des = models.CharField(max_length=64,null=True)
    class Meta:
        db_table = 'ModuleName'

class ModuleCode(models.Model):
    code_id = models.IntegerField(primary_key=True)
    code_name = models.CharField(max_length=32)
    code_des = models.CharField(max_length=64)
    classes = models.ForeignKey(ModuleName, on_delete=models.CASCADE)# 关联‘父表’，设置外键
    class Meta:
        db_table = 'ModuleCode'

class ModuleRqst(models.Model):
    word_id =models.IntegerField(auto_created=True,primary_key=True)
    word_name = models.CharField(max_length=16)
    word_struct = models.BooleanField(default=False)
    word_type = models.CharField(max_length=8)
    word_sort = models.IntegerField(default=0)
    word_content = models.CharField(max_length=32)
    classes = models.ForeignKey(ModuleCode, on_delete=models.CASCADE)  # 关联‘父表’，设置外键
    class Meta:
        db_table = 'ModuleRqst'
        ordering = ['word_sort']  # 指定按照上面字段排序

class ModuleRspd(models.Model):
    word_id = models.IntegerField(auto_created=True, primary_key=True)
    word_name = models.CharField(max_length=16)
    word_struct = models.BooleanField(default=False)
    word_type = models.CharField(max_length=8)
    word_sort = models.IntegerField(default=0)
    word_content = models.CharField(max_length=32)
    classes = models.ForeignKey(ModuleCode, on_delete=models.CASCADE)  # 关联‘父表’，设置外键
    class Meta:
        db_table = 'ModuleRspd'
        ordering = ['word_sort']  # 指定按照上面字段排序

class ModuleDataType(models.Model):
    id = models.IntegerField(auto_created=True,primary_key=True)
    struct_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=32,default='')
    module_id = models.PositiveIntegerField(default=0)
    des = models.CharField(max_length=32,default='')
    class Meta:
        db_table = 'ModuleDataType'

class ModuleStruct(models.Model):
    struct_id = models.IntegerField(auto_created=True, primary_key=True)
    struct_name = models.CharField(max_length=16)
    struct_type = models.PositiveIntegerField(default=0)
    struct_sort = models.PositiveIntegerField(default=0)
    struct_content = models.CharField(max_length=32)
    classes = models.ForeignKey(ModuleDataType, on_delete=models.CASCADE)  # 关联‘父表’，设置外键
    class Meta:
        db_table = 'ModuleStruct'
        ordering = ['struct_sort']  # 指定按照上面字段排序




























class AddressInfo(models.Model):
    address = models.CharField( max_length=200,null=True,blank=True,verbose_name='地址')
    pid = models.ForeignKey('self',null=True,blank=True,verbose_name='自关联',on_delete=models.CASCADE)
    def __str__(self):
        return self.address
    class Meta:
        db_table = 'AddressInfo'
        # ordering = ['pid'] #指定按照上面字段排序
        verbose_name = '省市县地址信息'
        verbose_name_plural = verbose_name
        # abstract = True#生成基类不生成数据 用于基础
        # managed = False #是否创建删除


