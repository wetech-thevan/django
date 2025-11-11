from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    # Tên công việc
    ten_cong_viec = models.CharField(
        max_length=255, 
        verbose_name="Tên công việc"
    )
    
    # Đơn vị gửi / đơn vị giao việc
    don_vi_gui = models.CharField(
        max_length=100, 
        verbose_name="Đơn vị gửi"
    )
    
    # Người nhận (Foreign Key đến User mặc định của Django)
    nguoi_nhan = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks', 
        verbose_name="Người nhận"
    )
    
    # Thời gian phải hoàn thành/trả kết quả
    thoi_gian_tra = models.DateTimeField(
        verbose_name="Thời gian trả"
    )
    
    # Đã nhận (BooleanField)
    da_nhan = models.BooleanField(
        default=False, 
        verbose_name="Đã nhận"
    )
    
    # Hoàn thành (BooleanField)
    hoan_thanh = models.BooleanField(
        default=False, 
        verbose_name="Hoàn thành"
    )
    
    # Ngày giờ nhận công việc
    ngay_nhan = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Ngày giờ nhận"
    )
    
    # Ngày giờ hoàn thành công việc
    ngay_hoan_thanh = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Ngày giờ hoàn thành"
    )
    
    # Thời gian tạo
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Thời gian tạo"
    )
    
    # Thời gian cập nhật cuối
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Thời gian cập nhật"
    )

    class Meta:
        verbose_name = "Công việc"
        verbose_name_plural = "Quản lý Công việc"
        ordering = ['thoi_gian_tra'] # Sắp xếp theo thời gian trả

    def __str__(self):
        return self.ten_cong_viec