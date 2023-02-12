# -*- coding:utf-8 -*-
from base.forms import DocumentForm
import pytest


@pytest.mark.django_db
def test_document_form():
    form = DocumentForm()
    # Test form fields
    assert form.fields['title'].label == "Заголовок:"
    assert form.fields['title'].max_length == 250
    assert form.fields['category'].label == "Категория:"
    assert form.fields['departament'].label == "Отдел:"
    assert form.fields['status'].label == "Статус:"
    assert form.fields['law'].label == "Закон:"
    assert form.fields['text'].label == "Текст:"
    assert form.fields['tags'].label == "Теги:"

    # Test field attributes
    # Check class attribute of category field widget
    assert form.fields['category'].widget.attrs["class"] == "form-select"
    # Check class attribute of departament field widget
    assert form.fields['departament'].widget.attrs["class"] == "form-select"
    # Check class attribute of status field widget
    assert form.fields['status'].widget.attrs["class"] == "form-select"
    # Check class attribute of law field widget
    assert form.fields['law'].widget.attrs["class"] == "form-select"

    # Test if the fields are required or not
    assert not (form.fields["departament"].required)
    assert not (form.fields["status"].required)
    assert not (form.fields["law"].required)
    assert form.fields["title"].required
    assert form.fields["category"].required


# Test if the data is valid or not
@pytest.mark.parametrize(
    'title, category, departament, law, status, text, tags',
    [(
        'Test title', 'ca 1', 'dep 2', 'law 3', 'stat 4', 'text', 'tags'
    )]
    # ['Test title, cat 1, dep 2, law 3,  statt 4, text, tags']
)
def valid_test(title, category, departament, law, status, text, tags):
    form = DocumentForm(data={
        'title': title,
        'category': category,
        'law': law,
        'departament': departament,
        'status': status,
        'text': text,
        'tags': tags
    }
    )
    assert form.is_valid()
