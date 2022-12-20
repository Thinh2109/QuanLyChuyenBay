from datve import admin, db
from datve.models import Category, Product, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request
from datetime import datetime
import dao


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CategoryView(AuthenticatedModelView):
    column_labels = {
        'name': 'Hạng ghế'
    }


class ProductView(AuthenticatedModelView):
    column_display_pk = True
    column_searchable_list = ['place', 'to']
    column_filters = ['place', 'to', 'price']
    can_view_details = True
    column_sortable_list = ['place', 'to', 'price']
    can_export = True
    details_modal = True
    column_exclude_list = ['image', 'active', 'created_time']
    column_labels = {
        'place': 'Nơi xuất phát',
        'to': 'Nơi đến',
        'price': 'Gía',
        'created_time': 'Ngày tạo',
        'category': 'Hạng ghế'
    }


class AdminView(AuthenticatedModelView):
    can_export = True
    column_labels = {
        'name': 'Tên người dùng',
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'active': 'Hoạt động',
        'joined_date': 'Ngày tạo',
        'avatar': 'Hình cá nhân',
        'user_role': 'Vai trò'
    }


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html', month_stats=dao.product_month_stats(year=year))

    # , stats = dao.product_stats()

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(CategoryView(Category, db.session, name='Hạng ghế'))
admin.add_view(ProductView(Product, db.session, name='Chuyến bay'))
admin.add_view(AdminView(User, db.session, name='Khách hàng'))
admin.add_view(LogoutView(name='Đăng xuất'))
admin.add_view(StatsView(name='Doanh thu'))
