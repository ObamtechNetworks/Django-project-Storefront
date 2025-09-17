from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('products/', views.ProductList.as_view()),  # changed to class based view
    path('products/<int:id>/', views.ProductDetail.as_view()),  # changed to class based view
    # path('collections/', views.collection_list, name='collection-list'),  # added name for hyperlinked related field
    # note the trailing slash is important, Django by default expects a trailing slash
    # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),  # added name for hyperlinked related field
    # also note for above, we used 'pk' as the parameter name to match the default expected by HyperlinkedRelatedField
]
