from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from .models import Team, TeamPokemon, Tag


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["title", "description", "tags"]
        labels = {
            "title": "チーム名",
            "description": "説明",
            "tags":"タグ",
        }
        widgets = {
            "title" : forms.TextInput(attrs={
                "placeholder" : "例 ガブガルゲンボルトバシャスイクン"
            }),
            "description":forms.Textarea(attrs={
                "placeholder" : "ポケモンの名前、技など詳細に書くほど検索にヒットしやすくなります。"
            }),
            "tags": forms.CheckboxSelectMultiple(),
        }


class TeamPokemonForm(forms.ModelForm):
    class Meta:
        model = TeamPokemon
        fields = [
            "slot", "image", "name", "item", "ability", "nature",
            "h_Status", "a_Status", "b_Status",
            "c_Status", "d_Status", "s_Status",
            "move1", "move2", "move3", "move4",
        ]
        labels = {
            "slot": "順番",
            "name": "ポケモン",
            "item": "持ち物",
            "ability": "特性",
            "nature": "性格",
            "h_Status": "HP",
            "a_Status": "こうげき",
            "b_Status": "ぼうぎょ",
            "c_Status": "とくこう",
            "d_Status": "とくぼう",
            "s_Status": "すばやさ",
            "move1": "技1",
            "move2": "技2",
            "move3": "技3",
            "move4": "技4",
        }


class BaseTeamPokemonFormSet(BaseInlineFormSet):
    pass


TeamPokemonFormSet = inlineformset_factory(
    Team,
    TeamPokemon,
    form=TeamPokemonForm,
    formset=BaseTeamPokemonFormSet,
    extra=6,
    min_num=1,
    max_num=6,
    validate_min=True,
    validate_max=True,
    can_delete=True,
)