from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import Http404

from .models import Team, Tag
from .forms import TeamForm, TeamPokemonFormSet


class IndexView(generic.ListView):
    model = Team
    template_name = "pokemonTeams/index.html"
    context_object_name = "teams"

    def get_queryset(self):
        q = self.request.GET.get("q")
        tag = self.request.GET.get("tag")
        queryset = Team.objects.all().order_by("-id")

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(author__username__icontains=q)
                | Q(pokemons__name__icontains = q)
                | Q(tags__name__icontains=q)
            )
        if tag:
            queryset = queryset.filter(
                tags__name=tag
            )

        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tags"] = Tag.objects.all()
        context["selected_tag"] = self.request.GET.get("tag", "")
        context["q"] = self.request.GET.get("q", "")

        return context


class TeamCreateView(LoginRequiredMixin, View):
    template_name = "pokemonTeams/create.html"

    def get(self, request):
        team_form = TeamForm()
        pokemon_formset = TeamPokemonFormSet()

        return render(request, self.template_name, {
            "team_form": team_form,
            "pokemon_formset": pokemon_formset,
        })

    def post(self, request):
        team_form = TeamForm(request.POST)
    
        if team_form.is_valid():
            team = team_form.save(commit=False)
            team.author = request.user
    
            pokemon_formset = TeamPokemonFormSet(
                request.POST,
                request.FILES,
                instance=team,
            )
    
            if pokemon_formset.is_valid():
                team.save()
    
                # タグを保存
                team_form.save_m2m()
    
                pokemon_formset.save()
    
                return redirect("pokemonTeams:index")
    
            print(pokemon_formset.errors)
            print(pokemon_formset.non_form_errors())
    
        else:
            pokemon_formset = TeamPokemonFormSet(
                request.POST,
                request.FILES,
            )
    
            print(team_form.errors)
    
        return render(request, self.template_name, {
            "team_form": team_form,
            "pokemon_formset": pokemon_formset,
        })

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("login")


class TeamDetailView(generic.DetailView):
    model = Team
    template_name = "pokemonTeams/detail.html"
    context_object_name = "team"


class TeamUpdateView(LoginRequiredMixin, View):
    template_name = "pokemonTeams/update.html"

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        print("記事の投稿者:", team.author)
        print("ログイン中:", request.user)

        if team.author != request.user:
            raise Http404

        team_form = TeamForm(instance=team)
        pokemon_formset = TeamPokemonFormSet(instance=team)

        return render(request, self.template_name, {
            "team_form": team_form,
            "pokemon_formset": pokemon_formset,
            "team": team,
        })

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        if team.author != request.user:
            raise Http404

        team_form = TeamForm(
            request.POST,
            instance=team,
        )

        pokemon_formset = TeamPokemonFormSet(
            request.POST,
            request.FILES,
            instance=team,
        )

        if team_form.is_valid() and pokemon_formset.is_valid():
            team_form.save()
            pokemon_formset.save()

            return redirect(
                "pokemonTeams:detail",
                pk=team.pk,
            )

        return render(request, self.template_name, {
            "team_form": team_form,
            "pokemon_formset": pokemon_formset,
            "team": team,
        })


class TeamDeleteView(LoginRequiredMixin, View):
    template_name = "pokemonTeams/delete.html"

    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        if team.author != request.user:
            raise Http404

        return render(request, self.template_name, {
            "team": team,
        })

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)

        if team.author != request.user:
            raise Http404

        team.delete()

        return redirect("pokemonTeams:index")