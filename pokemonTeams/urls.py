from django.urls import path
from . import views


app_name = "pokemonTeams"

urlpatterns = [
    path('',views.IndexView.as_view(), name="index"),
    path('create/',views.TeamCreateView.as_view(), name="create"),
    path("detail/<int:pk>/", views.TeamDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", views.TeamUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.TeamDeleteView.as_view(), name="delete"),
    path("signup/", views.SignUpView.as_view(), name="signup"),

]
