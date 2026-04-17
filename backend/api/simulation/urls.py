"""Register all API endpoint urls."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from api.simulation import views

router = DefaultRouter()
router.register('terrains', views.TerrainViewSet)
router.register('simulations', views.SimulationViewSet)
router.register('viruses', views.VirusViewSet)
router.register('preventions', views.PreventionViewSet)
router.register('scenarios', views.ScenarioViewSet)
router.register('agent_configs', views.AgentConfigViewSet)
router.register('runs', views.RunViewSet)
router.register('exports', views.ExportViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('admin/resetdb/', views.ResetDB.as_view()),
    path('exports/<int:pk>/download/', views.DownloadExportFile.as_view()),
    path('importer/configs/', views.ListConfigs.as_view()),
    path('importer/import/', views.ImportConfig.as_view()),
    path('mapfiles/', views.ListMapfiles.as_view()),
    path('runs/<int:pk>/exports/', views.ListRunExports.as_view()),
    path('runs/<int:pk>/outputs/', views.ListRunOutputs.as_view()),
    path('runs/<int:pk>/status/', views.CheckRunStatus.as_view()),
]
