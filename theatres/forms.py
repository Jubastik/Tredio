from django import forms
from django.forms import ModelForm, widgets

from core.models import City, Contact, ContactsGroup, ContactType, Location
from core.validators import AddressValidator
from rating.models import ReviewGroup
from theatres.models import Event, Theatre, Troupe, TroupeMember
from users.models import ActorProfile


class MultipleKeyValueForm(ModelForm):
    field_count = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, key_field, value_field, *args, **kwargs):
        self.fields_count = int(kwargs.pop("fields", 0))

        super().__init__(*args, **kwargs)
        self.fields["field_count"].initial = self.fields_count

        for index in range(self.fields_count):
            self.fields[f"key_{index}"] = key_field
            self.fields[f"value_{index}"] = value_field

    def multiple_fields(self):
        for index in range(self.fields_count):
            yield (f"key_{index}", f"value_{index}")


class CreateTroupeMembersForm(MultipleKeyValueForm):
    def __init__(self, *args, **kwargs):
        super().__init__(
            forms.ModelChoiceField(queryset=ActorProfile.objects.filter(is_published=True)),
            forms.CharField(max_length=TroupeMember._meta.get_field("role").max_length, required=False),
            *args,
            **kwargs,
        )

    def save(self, commit=True):
        troupe_data = {self.cleaned_data[key]: self.cleaned_data[value] for (key, value) in self.multiple_fields()}

        troupe = Troupe.objects.create()
        troupe_members = []
        for profile, role in troupe_data.items():
            troupe_members.append(TroupeMember(profile=profile, troupe=troupe, role=role if role else None))
        TroupeMember.objects.bulk_create(troupe_members)

        return troupe


class CreateContactsForm(MultipleKeyValueForm):
    def __init__(self, *args, **kwargs):
        super().__init__(
            forms.ModelChoiceField(queryset=ContactType.objects.all()),
            forms.CharField(max_length=Contact._meta.get_field("value").max_length),
            *args,
            **kwargs,
        )

    def save(self, commit=True):
        contacts_data = {self.cleaned_data[key]: self.cleaned_data[value] for (key, value) in self.multiple_fields()}

        contacts = ContactsGroup.objects.create()
        contacts_objects = []
        for contact_type, contact_value in contacts_data.items():
            contacts_objects.append(Contact(contacts_group=contacts, type=contact_type, value=contact_value))
        Contact.objects.bulk_create(contacts_objects)

        return contacts


class TheatreForm(CreateTroupeMembersForm):
    fias = forms.CharField(widget=forms.HiddenInput(attrs={"id": "location-fias"}))
    city = forms.CharField(widget=forms.HiddenInput(attrs={"id": "location-city"}))
    address = forms.CharField(
        label="?????????????? ?????????? ????????????",
        required=True,
        widget=widgets.TextInput(
            attrs={
                "id": "theatre-location",
                "class": "multi-form-input",
                "placeholder": "??????????",
                "minlength": 1,
                "maxlength": Location._meta.get_field("query").max_length,
            }
        ),
    )

    def save(self, commit=True):
        theatre = ModelForm.save(self, commit=False)
        troupe = CreateTroupeMembersForm.save(self, commit=True)

        location, _ = Location.objects.get_or_create(
            query=self.cleaned_data["address"],
            city=City.objects.get_or_create(name=self.cleaned_data["city"])[0],
            fias=self.cleaned_data["fias"],
        )

        theatre.troupe = troupe
        theatre.reviews = ReviewGroup.objects.create()
        theatre.location = location
        theatre.contacts = ContactsGroup.objects.create()

        if commit:
            theatre.save()
        return theatre

    def clean(self):
        cleaned_data = super().clean()
        address_validator = AddressValidator(
            cleaned_data.get("address"), cleaned_data.get("city"), cleaned_data.get("fias")
        )
        address_validator()

    class Meta:
        model = Theatre
        fields = (Theatre.name.field.name, Theatre.description.field.name, Theatre.image.field.name)

        labels = {
            Theatre.name.field.name: "?????????????? ???????????????? ????????????",
            Theatre.description.field.name: "?????????????? ???????????????? ????????????",
            Theatre.image.field.name: "???????????????? ???????????????? ????????????",
        }

        widgets = {
            Theatre.name.field.name: widgets.TextInput(attrs={"class": "multi-form-input", "placeholder": "????????????????"}),
            Theatre.description.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "????????????????"}
            ),
        }

    field_order = [Theatre.name.field.name, "address", Theatre.description.field.name]


class EventForm(CreateTroupeMembersForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[Event.theatre.field.name].queryset = Theatre.objects.filter(is_published=True)

    def save(self, commit=True):
        event = ModelForm.save(self, commit=False)
        troupe = CreateTroupeMembersForm.save(self, commit=True)

        event.troupe = troupe
        event.reviews = ReviewGroup.objects.create()

        if commit:
            event.save()
        return event

    class Meta:
        model = Event
        fields = (Event.name.field.name, Event.theatre.field.name, Event.image.field.name, Event.description.field.name)

        labels = {
            Event.name.field.name: "?????????????? ???????????????? ????????????????????",
            Event.theatre.field.name: "???????????????? ??????????",
            Event.image.field.name: "???????????????? ??????????????????????",
            Event.description.field.name: "?????????????? ???????????????? ????????????????????",
        }

        widgets = {
            Event.theatre.field.name: widgets.Select(attrs={"class": "multi-form-input"}),
            Event.name.field.name: widgets.TextInput(attrs={"class": "multi-form-input", "placeholder": "????????????????"}),
            Event.description.field.name: widgets.Textarea(
                attrs={"class": "multi-form-input", "placeholder": "????????????????"}
            ),
        }


class ActorForm(CreateContactsForm):
    def save(self, commit=True):
        actor = ModelForm.save(self, commit=False)
        contacts = CreateContactsForm.save(self, commit=True)

        actor.contacts = contacts

        if commit:
            actor.save()
        return actor

    class Meta:
        model = ActorProfile
        fields = (
            ActorProfile.first_name.field.name,
            ActorProfile.last_name.field.name,
            ActorProfile.birthday.field.name,
            ActorProfile.image.field.name,
            ActorProfile.description.field.name,
        )

        widgets = {
            ActorProfile.first_name.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "??????"}
            ),
            ActorProfile.last_name.field.name: widgets.TextInput(
                attrs={"class": "multi-form-input", "placeholder": "??????????????"}
            ),
            ActorProfile.description.field.name: widgets.Textarea(
                attrs={"class": "multi-form-input", "placeholder": "????????????????"}
            ),
            ActorProfile.birthday.field.name: widgets.DateTimeInput(
                attrs={"class": "multi-form-input", "placeholder": "???????? ????????????????", "type": "date"}
            ),
        }

        labels = {
            ActorProfile.first_name.field.name: "?????????????? ??????",
            ActorProfile.last_name.field.name: "?????????????? ??????????????",
            ActorProfile.description.field.name: "?????????????? ???????????????? ????????????",
            ActorProfile.birthday.field.name: "?????????????? ???????? ????????????????",
            ActorProfile.image.field.name: "?????????????????? ???????? ????????????",
        }
