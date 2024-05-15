from django.shortcuts import render
from io import BytesIO
import base64
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .forms import AlgoritmForm
    
def algoritm(request):
    if request.method == 'POST':
        form = AlgoritmForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            delta_xi_A = np.array(form.cleaned_data['delta_xi_A'])
            ni_A = np.array(form.cleaned_data['ni_A'])
            delta_xi_B = np.array(form.cleaned_data['delta_xi_B'])
            mi_B = np.array(form.cleaned_data['mi_B'])

            # Вычисляем характеристики для завода A
            Fn_A, F0_A, mean_A, std_A, KC_A, df_A = process_plant_data(delta_xi_A, ni_A)

            # Вычисляем характеристики для завода B
            Fn_B, F0_B, mean_B, std_B, KC_B, df_B = process_plant_data(delta_xi_B, mi_B)

            plot_url1, plot_url2 = create_plots(delta_xi_A, Fn_A, F0_A, delta_xi_B, Fn_B, F0_B)

            alpha = 0.05  # Уровень значимости
            critical_value = 1.358  # Табличное значение КС для α = 0.05

            
            context = {
                'form': form,
                'df_A': df_A.to_html(),
                'df_B': df_B.to_html(),
                'KC_A': KC_A,
                'KC_B': KC_B,
                'plot_url1': plot_url1,
                'plot_url2': plot_url2,
                'critical_value': critical_value,
                'alpha': alpha,
            }
            
            return render(request, 'algoritm.html', context)
    else:
        form = AlgoritmForm()
    return render(request, 'algoritm.html', {'form': form})

def process_plant_data(delta_xi, ni):
    Fn = np.cumsum(ni) / np.sum(ni)
    Fn_new = np.insert(Fn, 0, 0)
    Fn_new_2 = np.delete(Fn_new, -1)

    mean = np.sum(delta_xi * ni) / np.sum(ni)
    std = np.sqrt(np.sum(ni * (delta_xi - mean)**2) / np.sum(ni))

    F0 = norm.cdf((delta_xi - mean) / std)

    KC = np.sqrt(np.sum(ni)) * np.max(np.abs(Fn_new_2 - F0))

    data = {
        'Delta_Xi': delta_xi,
        'Ni': ni,
        'Ni/N': ni / np.sum(ni),
        'Fn': Fn_new_2,
        'F0': F0,
    }
    df = pd.DataFrame(data)

    return Fn_new_2, F0, mean, std, KC, df

def create_plots(delta_xi_A, Fn_A, F0_A, delta_xi_B, Fn_B, F0_B):
    # Создаем буферы для хранения графиков в виде изображений
    buffer1 = BytesIO()
    buffer2 = BytesIO()

    # Создаем графики
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(delta_xi_A, Fn_A, label='Fn (Plant A)')
    ax1.plot(delta_xi_A, F0_A, label='F0 (Plant A)')
    ax1.legend()
    ax1.set_title('Empirical Distribution Function and Normal Distribution for Plant A')
    ax1.set_xlabel('Delta_Xi')
    ax1.set_ylabel('Fn, F0')
    ax1.grid(True)
    fig1.savefig(buffer1, format='png')

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(delta_xi_B, Fn_B, label='Fn (Plant B)')
    ax2.plot(delta_xi_B, F0_B, label='F0 (Plant B)')
    ax2.legend()
    ax2.set_title('Empirical Distribution Function and Normal Distribution for Plant B')
    ax2.set_xlabel('Delta_Xi')
    ax2.set_ylabel('Fn, F0')
    ax2.grid(True)
    fig2.savefig(buffer2, format='png')

    buffer1 = BytesIO()
    buffer2 = BytesIO()
    fig1.savefig(buffer1, format='png')
    fig2.savefig(buffer2, format='png')

    # Кодирование буферов в base64 для отображения на веб-странице
    buffer1.seek(0)
    plot_url1 = base64.b64encode(buffer1.getvalue()).decode('utf-8')

    buffer2.seek(0)
    plot_url2 = base64.b64encode(buffer2.getvalue()).decode('utf-8')

    return plot_url1, plot_url2
