from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(label="Full Name", max_length=150)
    email = forms.EmailField(required=True)

    ROLE_CHOICES = [
        ('student', 'Tenant (Looking for housing)'),
        ('landlord', 'Landlord (Listing properties)')
    ]
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial='student',
        label="I am a..."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'email', 'phone', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'role' in self.fields:
            self.fields['role'] = self.fields.pop('role')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        email = cleaned_data.get('email')

        if role == 'student' and email:
            if not email.endswith('.ac.uk'):
                self.add_error('email', "Students must use a valid UK university email (.ac.uk).")

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "This email is already registered.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        names = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]

        if commit:
            user.save()
        return user