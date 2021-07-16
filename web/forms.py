from django import forms

class AdminSongForm(forms.ModelForm):
	canciones = forms.FileField(widget=forms.FileInput(
		attrs={'multiple': True}), 
		required=False
	)