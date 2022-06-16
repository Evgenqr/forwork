from base.forms import AuthForm


def get_context_data(request):
    context = {
        'login_form': AuthForm()
    }
    return context
