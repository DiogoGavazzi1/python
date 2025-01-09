from PySimpleGUI import PySimpleGUI as sg

# Layout
sg.theme('Reddit')
layout = [
    [sg.Text('Utilizador'), sg.Input(key='User')],
    [sg.Text('Password'), sg.Input(key='Password', password_char='*')],
    [sg.Checkbox('Guardar Login?')],
    [sg.Button('Entrar')]
]

# Janela
janela = sg.Window('Tela de Login', layout)

# Ler Evento
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Entrar':
        if valores['User'] == 'Diogo' and valores['Password'] == '1234':
            print('Bem vindo burro do caralho')
            
        else:
            print('Tens alguma coisa errada seu burro da merda')
