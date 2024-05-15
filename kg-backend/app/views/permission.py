from django.views.decorators.csrf import csrf_exempt
from app.utils.jsonResponse import json_response
from app.models import User, UserPermission, AdminPermission, Permission
import json


# 查询某一用户对应权限
@csrf_exempt
def get_user_permission(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        is_admin = User.objects.filter(user_id=user_id).first().role
        if is_admin == 1:
            user_permission = AdminPermission.objects.filter(user_id=user_id)
        else:
            user_permission = UserPermission.objects.filter(user_id=user_id)
        if user_permission.first() is None:
            return json_response(204, '该用户不存在')
        else:
            user_permission_data = list(user_permission.values())
            response_data = {
                'data': user_permission_data,
                'role': is_admin,
            }

            # 返回修改后的数据
            return json_response(200, '权限查询成功', response_data)
    else:
        return json_response(203, '请求方式错误')


# 修改用户权限
@csrf_exempt
def change_permission(request):
    """管理员权限-用户权限
       7 - 1 and 2
       8 - 3 and 4
       9 - 5
       10 - 6"""
    if request.method == 'POST':
        admin_email = request.user_info
        admin_id = User.objects.filter(email=admin_email).first().user_id
        admin_role = User.objects.filter(email=admin_email).first().role
        user_id = request.POST.get('user_id')
        is_admin = User.objects.filter(user_id=user_id).first().role
        permission_id = [int(num) for num in request.POST.get('permission_id').split(",")]
        is_allowed = [int(num) for num in request.POST.get('is_allowed').split(",")]
        print(user_id, permission_id, is_allowed)

        if admin_role == 1:
            # 获取管理员当前的权限列表
            admin_per = AdminPermission.objects.filter(user_id=admin_id).values_list('is_allowed', flat=True)

            # 获取用户当前的权限列表
            cur_is_allowed = UserPermission.objects.filter(user_id=user_id).values_list('is_allowed', flat=True)

            # 对比权限是否有变化
            changed_is_allowed = [i ^ j for i, j in zip(is_allowed, cur_is_allowed)]
            print("用户权限变化{}".format(changed_is_allowed))

            changed = [changed_is_allowed[0] or changed_is_allowed[1], changed_is_allowed[2] or changed_is_allowed[3],
                       changed_is_allowed[4], changed_is_allowed[5]]
            print(changed)

            # 判断管理员是否有权限修改用户权限
            for i in range(len(changed)):
                if admin_per[i] == 0 and changed[i] == 1:
                    return json_response(206, '无权限此操作')

        for i in range(len(permission_id)):
            if is_admin == 1:  # 超管修改管理员权限
                userpermission = AdminPermission.objects.filter(user_id=user_id, permission_id=permission_id[i]).first()
            else:  # 管理员修改用户权限
                userpermission = UserPermission.objects.filter(user_id=user_id, permission_id=permission_id[i]).first()
            userpermission.is_allowed = is_allowed[i]
            userpermission.save()
        return json_response(200, '修改成功')
    else:
        return json_response(203, '请求方式错误')


# 授予管理员权限
@csrf_exempt
def grant_admin(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_admin = User.objects.filter(user_id=user_id).first()
        new_admin.role = 1
        new_admin.save()
        userpermission = UserPermission.objects.filter(user_id=user_id)
        userpermission.delete()

        # 添加管理员权限表
        user_id = User.objects.filter(user_id=user_id).first()
        permission_list = Permission.objects.filter(is_admin=1).values_list('permission_id')
        for permission in permission_list:
            admin_permission = AdminPermission(user=user_id, permission_id=permission[0], is_allowed=1)
            admin_permission.save()
        return json_response(200, '操作成功')
    else:
        return json_response(203, '请求方式错误')


# 删除用户
@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user_del = User.objects.filter(user_id=user_id).first()
        if user_del is None:
            return json_response(204, '该用户不存在')
        user_del.delete()
        return json_response(200, '操作成功')
    else:
        return json_response(203, '请求方式错误')
