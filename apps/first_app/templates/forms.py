class UserForm(ModelForm):
    class Meta:
        model = User

TripFormset = inlineformset_factory(User, Trip,
    fields=('current_travelers'), extra=1,
    can_delete=False)
