from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='main'),
    path('addBook',views.addBook,name='addBook'),
    path('favorite/<int:bookId>',views.favorite,name='favorite'),
    path('<int:bookId>',views.showBook,name='showBook'),
    path('handlingBook/<int:bookId>',views.handlingBook,name='handlingBook'),
    path('un_favorite/<int:bookId>',views.un_favorite,name='un_favorite')
    # path('update/<int:bookId>',views.update,name='update')
]
