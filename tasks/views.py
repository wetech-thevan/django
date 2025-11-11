from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views import View

from .models import Task
from .forms import TaskForm, AdminUserCreationForm, AdminUserChangeForm

# =========== MIXIN TÙY CHỈNH CHO PHÂN QUYỀN ===========

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin để giới hạn quyền truy cập chỉ dành cho Admin (user có is_staff=True).
    Nếu không phải Admin, redirect về trang Dashboard.
    """
    def test_func(self):
        # Admin là user có quyền is_staff (staff/admin)
        return self.request.user.is_staff 

    def handle_no_permission(self):
        # Gửi thông báo và chuyển hướng
        messages.error(self.request, "Bạn không có quyền truy cập trang này.")
        return redirect('dashboard')


# =========== QUẢN LÝ CÔNG VIỆC (TASKS) ===========

class TaskListView(LoginRequiredMixin, ListView):
    """
    Trang Dashboard - Danh sách công việc.
    Hiển thị TẤT CẢ Task nếu là Admin, chỉ hiển thị Task được giao nếu là User thường.
    """
    model = Task
    template_name = 'tasks/dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        # Nếu là Admin (is_staff=True), hiển thị tất cả Task
        if user.is_staff:
            return Task.objects.all().select_related('nguoi_nhan')
        # Nếu là User thường, chỉ hiển thị các Task được giao cho họ
        return Task.objects.filter(nguoi_nhan=user).select_related('nguoi_nhan')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Truyền thông tin về quyền Admin để ẩn/hiện các nút Sửa/Xóa trong template
        context['is_admin'] = self.request.user.is_staff
        return context

class TaskCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """
    Trang Thêm công việc (Admin Only).
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Thêm công việc mới"
        return context

    def form_valid(self, form):
        # Gán thông báo thành công
        messages.success(self.request, "Thêm công việc thành công.")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """
    Trang Sửa công việc (Admin Only).
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Chỉnh sửa công việc"
        return context

    def form_valid(self, form):
        # Gán thông báo thành công
        messages.success(self.request, "Cập nhật công việc thành công.")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    Trang Xóa công việc (Admin Only).
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'task'

    def form_valid(self, form):
        # Gán thông báo thành công
        messages.success(self.request, f"Đã xóa công việc: {self.object.ten_cong_viec}.")
        return super().form_valid(form)


class TaskToggleStatusView(LoginRequiredMixin, View):
    """
    Xử lý việc tick/untick trạng thái 'Đã nhận' và 'Hoàn thành'
    """
    def post(self, request, pk, status_field):
        from django.utils import timezone
        
        task = get_object_or_404(Task, pk=pk)
        user = request.user

        # Phân quyền: Chỉ người được giao công việc mới được tick/untick
        if task.nguoi_nhan != user:
            messages.error(request, "Bạn không có quyền thay đổi trạng thái công việc này.")
            return HttpResponseRedirect(reverse_lazy('dashboard'))

        # Lấy giá trị mới từ POST
        new_value = request.POST.get(status_field) == 'on'
        
        # Logic: Chỉ cho phép tick 'Hoàn thành' nếu đã 'Đã nhận'
        if status_field == 'hoan_thanh' and new_value is True and task.da_nhan is False:
             messages.error(request, "Bạn cần 'Đã nhận' công việc trước khi 'Hoàn thành'.")
             return HttpResponseRedirect(reverse_lazy('dashboard'))

        # Cập nhật trường tương ứng
        if status_field == 'da_nhan':
            task.da_nhan = new_value
            # Ghi lại thời gian nhận khi tick
            if new_value:
                task.ngay_nhan = timezone.now()
            else:
                # Nếu untick 'Đã nhận', xóa thời gian và untick luôn 'Hoàn thành'
                task.ngay_nhan = None
                task.hoan_thanh = False
                task.ngay_hoan_thanh = None
        elif status_field == 'hoan_thanh':
            task.hoan_thanh = new_value
            # Ghi lại thời gian hoàn thành khi tick
            if new_value:
                task.ngay_hoan_thanh = timezone.now()
            else:
                # Nếu untick 'Hoàn thành', xóa thời gian
                task.ngay_hoan_thanh = None

        task.save()
        messages.success(request, f"Cập nhật trạng thái công việc '{task.ten_cong_viec}' thành công.")
        return HttpResponseRedirect(reverse_lazy('dashboard'))


# =========== QUẢN LÝ TÀI KHOẢN (ADMIN ONLY) ===========

class AccountManageListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """
    Trang Quản lý tài khoản (Admin Only).
    """
    model = User
    template_name = 'tasks/account_manage.html'
    context_object_name = 'users'

    def get_queryset(self):
        # Liệt kê tất cả user, trừ user hiện tại (tránh tự xóa/sửa quyền mình)
        return User.objects.all().exclude(pk=self.request.user.pk).order_by('username')

class AccountCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """
    Trang Thêm User mới (Admin Only).
    """
    model = User
    form_class = AdminUserCreationForm
    template_name = 'tasks/user_form.html'
    success_url = reverse_lazy('account_manage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Thêm người dùng mới"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Đã thêm người dùng '{form.cleaned_data['username']}' thành công.")
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """
    Trang Sửa User (Admin Only).
    """
    model = User
    form_class = AdminUserChangeForm
    template_name = 'tasks/user_form.html'
    success_url = reverse_lazy('account_manage')
    context_object_name = 'target_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Chỉnh sửa người dùng"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Đã cập nhật người dùng '{self.object.username}' thành công.")
        return super().form_valid(form)

class AccountDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    Trang Xóa User (Admin Only).
    """
    model = User
    template_name = 'tasks/user_confirm_delete.html' 
    success_url = reverse_lazy('account_manage')
    context_object_name = 'target_user'

    def form_valid(self, form):
        messages.success(self.request, f"Đã xóa người dùng: {self.object.username}.")
        return super().form_valid(form)