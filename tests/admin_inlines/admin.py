from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models

from .models import (
    Author, BinaryTree, CapoFamiglia, Chapter, Child, Child1, Child2, Child3,
    ChildModel1, ChildModel2, Class, Consigliere, Course, CourseProxy,
    CourseProxy1, CourseProxy2, EditablePKBook, ExtraTerrestrial, Fashionista,
    FootNote, Holder, Holder2, Holder3, Holder4, Holder5, Inner, Inner2,
    Inner3, Inner4Stacked, Inner4Tabular, Inner5Stacked, Inner5Tabular,
    NonAutoPKBook, NonAutoPKBookChild, Novel, NovelReadonlyChapter, OutfitItem,
    Parent1, Parent2, Parent3, ParentModelWithCustomPk, Person, Poll, Profile,
    ProfileCollection, Question, ReadOnlyInline, ShoppingWeakness, Sighting,
    SomeChildModel, SomeParentModel, SottoCapo, Teacher, Title,
    TitleCollection,
)

site = admin.AdminSite(name="admin")


class BookInline(admin.TabularInline):
    model = Author.books.through


class NonAutoPKBookTabularInline(admin.TabularInline):
    model = NonAutoPKBook
    classes = ('collapse',)


class NonAutoPKBookChildTabularInline(admin.TabularInline):
    model = NonAutoPKBookChild
    classes = ('collapse',)


class NonAutoPKBookStackedInline(admin.StackedInline):
    model = NonAutoPKBook
    classes = ('collapse',)


class EditablePKBookTabularInline(admin.TabularInline):
    model = EditablePKBook


class EditablePKBookStackedInline(admin.StackedInline):
    model = EditablePKBook


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline, NonAutoPKBookTabularInline, NonAutoPKBookStackedInline,
        EditablePKBookTabularInline, EditablePKBookStackedInline,
        NonAutoPKBookChildTabularInline,
    ]


class InnerInline(admin.StackedInline):
    model = Inner
    can_delete = False
    readonly_fields = ('readonly',)  # For bug #13174 tests.


class HolderAdmin(admin.ModelAdmin):

    class Media:
        js = ('my_awesome_admin_scripts.js',)


class ReadOnlyInlineInline(admin.TabularInline):
    model = ReadOnlyInline
    readonly_fields = ['name']


class InnerInline2(admin.StackedInline):
    model = Inner2

    class Media:
        js = ('my_awesome_inline_scripts.js',)


class InnerInline2Tabular(admin.TabularInline):
    model = Inner2


class CustomNumberWidget(forms.NumberInput):
    class Media:
        js = ('custom_number.js',)


class InnerInline3(admin.StackedInline):
    model = Inner3
    formfield_overrides = {
        models.IntegerField: {'widget': CustomNumberWidget},
    }

    class Media:
        js = ('my_awesome_inline_scripts.js',)


class TitleForm(forms.ModelForm):
    title1 = forms.CharField(max_length=100)

    def clean(self):
        cleaned_data = self.cleaned_data
        title1 = cleaned_data.get("title1")
        title2 = cleaned_data.get("title2")
        if title1 != title2:
            raise ValidationError("The two titles must be the same")
        return cleaned_data


class TitleInline(admin.TabularInline):
    model = Title
    form = TitleForm
    extra = 1


class Inner4StackedInline(admin.StackedInline):
    model = Inner4Stacked
    show_change_link = True


class Inner4TabularInline(admin.TabularInline):
    model = Inner4Tabular
    show_change_link = True


class Holder4Admin(admin.ModelAdmin):
    inlines = [Inner4StackedInline, Inner4TabularInline]


class Inner5StackedInline(admin.StackedInline):
    model = Inner5Stacked
    classes = ('collapse',)


class Inner5TabularInline(admin.TabularInline):
    model = Inner5Tabular
    classes = ('collapse',)


class Holder5Admin(admin.ModelAdmin):
    inlines = [Inner5StackedInline, Inner5TabularInline]


class InlineWeakness(admin.TabularInline):
    model = ShoppingWeakness
    extra = 1


class WeaknessForm(forms.ModelForm):
    extra_field = forms.CharField()

    class Meta:
        model = ShoppingWeakness
        fields = '__all__'


class WeaknessInlineCustomForm(admin.TabularInline):
    model = ShoppingWeakness
    form = WeaknessForm


class FootNoteForm(forms.ModelForm):
    extra_field = forms.CharField()

    class Meta:
        model = FootNote
        fields = '__all__'


class FootNoteNonEditableInlineCustomForm(admin.TabularInline):
    model = FootNote
    form = FootNoteForm

    def has_change_permission(self, request, obj=None):
        return False


class QuestionInline(admin.TabularInline):
    model = Question
    readonly_fields = ['call_me']

    def call_me(self, obj):
        return 'Callable in QuestionInline'


class PollAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

    def call_me(self, obj):
        return 'Callable in PollAdmin'


class ChapterInline(admin.TabularInline):
    model = Chapter
    readonly_fields = ['call_me']

    def call_me(self, obj):
        return 'Callable in ChapterInline'


class NovelAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


class ReadOnlyChapterInline(admin.TabularInline):
    model = Chapter

    def has_change_permission(self, request, obj=None):
        return False


class NovelReadonlyChapterAdmin(admin.ModelAdmin):
    inlines = [ReadOnlyChapterInline]


class ConsigliereInline(admin.TabularInline):
    model = Consigliere


class SottoCapoInline(admin.TabularInline):
    model = SottoCapo


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


# admin for #18433
class ChildModel1Inline(admin.TabularInline):
    model = ChildModel1


class ChildModel2Inline(admin.StackedInline):
    model = ChildModel2


# admin for #19425 and #18388
class BinaryTreeAdmin(admin.TabularInline):
    model = BinaryTree

    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            return extra - obj.binarytree_set.count()
        return extra

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 3
        if obj:
            return max_num - obj.binarytree_set.count()
        return max_num


# admin for #19524
class SightingInline(admin.TabularInline):
    model = Sighting


# admin and form for #18263
class SomeChildModelForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = SomeChildModel
        widgets = {
            'position': forms.HiddenInput,
        }
        labels = {'readonly_field': 'Label from ModelForm.Meta'}
        help_texts = {'readonly_field': 'Help text from ModelForm.Meta'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'new label'


class SomeChildModelInline(admin.TabularInline):
    model = SomeChildModel
    form = SomeChildModelForm
    readonly_fields = ('readonly_field',)


class StudentInline(admin.StackedInline):
    model = Child
    extra = 1
    fieldsets = [
        ('Name', {'fields': ('name',), 'classes': ('collapse',)}),
    ]


class TeacherAdmin(admin.ModelAdmin):
    inlines = [StudentInline]


class AuthorTabularInline(admin.TabularInline):
    model = Author


class FashonistaStackedInline(admin.StackedInline):
    model = Fashionista


# Admin for #30231
class ClassStackedHorizontal(admin.StackedInline):
    model = Class
    extra = 1
    filter_horizontal = ['person']


class ClassAdminStackedHorizontal(admin.ModelAdmin):
    inlines = [ClassStackedHorizontal]


class ClassTabularHorizontal(admin.TabularInline):
    model = Class
    extra = 1
    filter_horizontal = ['person']


class ClassAdminTabularHorizontal(admin.ModelAdmin):
    inlines = [ClassTabularHorizontal]


class ClassTabularVertical(admin.TabularInline):
    model = Class
    extra = 1
    filter_vertical = ['person']


class ClassAdminTabularVertical(admin.ModelAdmin):
    inlines = [ClassTabularVertical]


class ClassStackedVertical(admin.StackedInline):
    model = Class
    extra = 1
    filter_vertical = ['person']


class ClassAdminStackedVertical(admin.ModelAdmin):
    inlines = [ClassStackedVertical]


# admin and form for #31867
class Child1Form(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Child1
        widgets = {
            'position': forms.HiddenInput,
        }

    def _post_clean(self):
        super()._post_clean()
        if self.instance is not None and self.instance.position == 1:
            self.add_error(None, ValidationError("A non-field error"))


class Child1Inline(admin.TabularInline):
    model = Child1
    form = Child1Form


class Child2Form(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Child2
        widgets = {
            'position': forms.HiddenInput,
        }


class Child2Inline(admin.StackedInline):
    model = Child2
    form = Child2Form
    fields = (("name", "position"), )


class Child3Form(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Child3
        widgets = {
            'position': forms.HiddenInput,
        }


class Child3Inline(admin.StackedInline):
    model = Child3
    form = Child3Form
    fields = ("name", "position")


site.register(TitleCollection, inlines=[TitleInline])
# Test bug #12561 and #12778
# only ModelAdmin media
site.register(Holder, HolderAdmin, inlines=[InnerInline])
# ModelAdmin and Inline media
site.register(Holder2, HolderAdmin, inlines=[InnerInline2, InnerInline2Tabular])
# only Inline media
site.register(Holder3, inlines=[InnerInline3])

site.register(Poll, PollAdmin)
site.register(Novel, NovelAdmin)
site.register(NovelReadonlyChapter, NovelReadonlyChapterAdmin)
site.register(Fashionista, inlines=[InlineWeakness])
site.register(Holder4, Holder4Admin)
site.register(Holder5, Holder5Admin)
site.register(Author, AuthorAdmin)
site.register(CapoFamiglia, inlines=[ConsigliereInline, SottoCapoInline, ReadOnlyInlineInline])
site.register(ProfileCollection, inlines=[ProfileInline])
site.register(ParentModelWithCustomPk, inlines=[ChildModel1Inline, ChildModel2Inline])
site.register(BinaryTree, inlines=[BinaryTreeAdmin])
site.register(ExtraTerrestrial, inlines=[SightingInline])
site.register(SomeParentModel, inlines=[SomeChildModelInline])
site.register([Question, Inner4Stacked, Inner4Tabular])
site.register(Teacher, TeacherAdmin)
site.register(Chapter, inlines=[FootNoteNonEditableInlineCustomForm])
site.register(OutfitItem, inlines=[WeaknessInlineCustomForm])
site.register(Person, inlines=[AuthorTabularInline, FashonistaStackedInline])
site.register(Course, ClassAdminStackedHorizontal)
site.register(CourseProxy, ClassAdminStackedVertical)
site.register(CourseProxy1, ClassAdminTabularVertical)
site.register(CourseProxy2, ClassAdminTabularHorizontal)
site.register(Parent1, inlines=[Child1Inline])
site.register(Parent2, inlines=[Child2Inline])
site.register(Parent3, inlines=[Child3Inline])
