from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),  # changed to class based view
    path('products/<int:id>/', views.ProductDetail.as_view()),  # changed to class based view
    path('collections/', views.CollectionList.as_view(), name='collection-list'),  # changed to class based view
    # note the trailing slash is important, Django by default expects a trailing slash
    path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),  # changed to class based view
    # also note for above, we used 'pk' as the parameter name to match the default expected by HyperlinkedRelatedField
]
