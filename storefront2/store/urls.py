from django.urls import include, path
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

# from pprint import pprint

router = routers.DefaultRouter()  # creates a router instance

# register the viewsets with the router
router.register(r'products', views.ProductViewSet)
router.register(r'collections', views.CollectionViewSet)
# next is to include the router urls in the urlpatterns
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(router, r'products', lookup='product')
# let's register our child routes with the nested router
products_router.register(r'reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path(r'', include(router.urls)),  # include the router urls
    path(r'', include(products_router.urls)),  # include the nested router urls
]

# urlpatterns = router.urls + products_router.urls # combine the two router urls
# we can use the below if we have other paths or url patterns for a specific purpose
# urlpatterns = [
#     path('', include(router.urls)),
# ]

# but since we only have the router urls, we can directly assign it to urlpatterns
# urlpatterns = router.urls

# there's also another router called DefaultRouter which also creates a default API root view
# and also provides an optional way to include format suffixes in the URLs
# we can use it as follows:
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)


# URLConf
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),  # changed to class based view
#     path('products/<int:pk>/', views.ProductDetail.as_view()),  # changed to class based view
#     path('collections/', views.CollectionList.as_view(), name='collection-list'),  # changed to class based view
#     # note the trailing slash is important, Django by default expects a trailing slash
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),  # changed to class based view
#     # also note for above, we used 'pk' as the parameter name to match the default expected by HyperlinkedRelatedField
# ]
