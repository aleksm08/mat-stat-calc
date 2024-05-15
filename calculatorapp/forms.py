from django import forms
import numpy as np

class AlgoritmForm(forms.Form):
    delta_xi_A = forms.CharField(label='Delta Xi A', widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}))
    ni_A = forms.CharField(label='Ni A', widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}))
    delta_xi_B = forms.CharField(label='Delta Xi B', widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}))
    mi_B = forms.CharField(label='Mi B', widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}))

    def clean_delta_xi_A(self):
        delta_xi_A = self.cleaned_data['delta_xi_A']
        try:
            delta_xi_A = np.array([float(x) for x in delta_xi_A.split(',')])
        except ValueError:
            raise forms.ValidationError('Введите числа, разделенные запятыми')
        return delta_xi_A

    def clean_ni_A(self):
        ni_A = self.cleaned_data['ni_A']
        try:
            ni_A = np.array([int(x) for x in ni_A.split(',')])
        except ValueError:
            raise forms.ValidationError('Введите целые числа, разделенные запятыми')
        return ni_A

    def clean_delta_xi_B(self):
        delta_xi_B = self.cleaned_data['delta_xi_B']
        try:
            delta_xi_B = np.array([float(x) for x in delta_xi_B.split(',')])
        except ValueError:
            raise forms.ValidationError('Введите числа, разделенные запятыми')
        return delta_xi_B

    def clean_mi_B(self):
        mi_B = self.cleaned_data['mi_B']
        try:
            mi_B = np.array([int(x) for x in mi_B.split(',')])
        except ValueError:
            raise forms.ValidationError('Введите целые числа, разделенные запятыми')
        return mi_B
