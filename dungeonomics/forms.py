from allauth.account.forms import LoginForm

# class MyLoginForm(LoginForm):
#     def __init__(self, *args, **kwargs):
#         super(MyLoginForm, self).__init__(*args, **kwargs)
#         self.fields['password'].widget = forms.PasswordInput()

#         if 'remember' in self.fields.keys():
#             del self.fields['remember']

#         helper = FormHelper()
#         helper.form_show_labels = False
#         helper.layout = Layout(
#             Field('login', placeholder = 'Email address'),
#             Field('password', placeholder = 'Password'),
#             FormActions(
#                 Submit('submit', 'Log me in to Cornell Forum', css_class = 'btn-primary')
#             ),
#         )
#         self.helper = helper