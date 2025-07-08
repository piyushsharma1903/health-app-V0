from django.urls import path
from .views import UploadLabReport
from .views import ReportListAPIView, ReportDeleteView
from django.conf import settings
from django.conf.urls.static import static
#endpoints
urlpatterns = [
    path('upload-lab/', UploadLabReport.as_view(), name='upload-lab'),
    path('reports/', ReportListAPIView.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDeleteView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
