from base.forms import DocumentForm


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
    assert form.fields['category'].widget.attrs["class"] == "form-select"  # Check class attribute of category field widget 
    assert form.fields['departament'].widget.attrs["class"] == "form-select"  # Check class attribute of departament field widget 
    assert form.fields['status'].widget.attrs["class"] == "form-select"  # Check class attribute of status field widget 
    assert form.fields['law'].widget.attrs["class"] == "form-select"  # Check class attribute of law field widget 

     # Test if the fields are required or not  
    #  assert not(form.fields["departament"].required)   # Departament is not required  
    #  assert not(form.fields["status"].required)       # Status is not required  

     # Test if the data is valid or not  

    #  data = {   'title': 'Test title',   'category': 1,   'departament': 2,   'status': 3,   'law': [1,2],   'text': 'Test text',   }

    #  valid_data = DocumentForm(data=data)

    #  assert valid_data.is_valid()