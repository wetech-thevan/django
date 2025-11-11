from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Task

# Form dành cho Admin thêm/sửa Task
class TaskForm(forms.ModelForm):
    # Tùy chỉnh trường người nhận để chọn từ danh sách User
    nguoi_nhan = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        label="Người nhận",
        # Custom widget để hiển thị đẹp hơn
        widget=forms.Select(attrs={'class': 'form-select'}) 
    )
    
    # Tùy chỉnh trường Thời gian trả
    thoi_gian_tra = forms.DateTimeField(
        label="Thời gian trả",
        # Sử dụng input type datetime-local của HTML5 cho việc chọn ngày giờ
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'], 
    )

    class Meta:
        model = Task
        fields = ['ten_cong_viec', 'don_vi_gui', 'nguoi_nhan', 'thoi_gian_tra']
        # Thêm class Bootstrap cho các trường còn lại
        widgets = {
            'ten_cong_viec': forms.TextInput(attrs={'class': 'form-control'}),
            'don_vi_gui': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'ten_cong_viec': 'Tên công việc',
            'don_vi_gui': 'Đơn vị gửi',
        }

# Form tạo User cho Admin
class AdminUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(
        required=False, 
        label="Là Quản trị viên (Admin)?",
        help_text="Nếu chọn, user sẽ có quyền truy cập admin."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'is_admin')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # Thiết lập is_staff = True nếu checkbox 'is_admin' được chọn
        if self.cleaned_data.get('is_admin'):
            user.is_staff = True
        
        if commit:
            user.save()
        return user

# Form chỉnh sửa User cho Admin
class AdminUserChangeForm(UserChangeForm):
    is_admin = forms.BooleanField(
        required=False, 
        label="Là Quản trị viên (Admin)?",
        help_text="Nếu chọn, user sẽ có quyền truy cập admin."
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_admin')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thiết lập giá trị ban đầu của checkbox is_admin
        self.fields['is_admin'].initial = self.instance.is_staff
        # Loại bỏ trường password mặc định của UserChangeForm
        if 'password' in self.fields:
            self.fields.pop('password')
            
        # Thêm class Bootstrap
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # Bỏ class form-control cho checkbox để hiển thị đúng
        self.fields['is_active'].widget.attrs.pop('class', None)
        self.fields['is_admin'].widget.attrs.pop('class', None)
            
    def save(self, commit=True):
        user = super().save(commit=False)
        # Cập nhật is_staff dựa trên checkbox
        user.is_staff = self.cleaned_data.get('is_admin')
        
        if commit:
            user.save()
        return user