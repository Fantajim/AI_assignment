import PySimpleGUI as sg
import keras
import os
import time
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')



models_list = []
fig = plt.gcf()

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def fill_model(name):
    model = keras.models.load_model(f"{os.getcwd()}/{name}")
    print("loaded")
    with open(f"{os.getcwd()}/{name}/model_history.txt") as file:
        history = json.load(file)
        print(f"accuracy: {history['accuracy']}")

    model_acc.Update(history['accuracy'][-1])
    model_val_acc.Update(history['val_accuracy'][-1])
    model_loss.Update(history['loss'][-1])
    model_val_loss.Update(history['val_loss'][-1])

    plt.plot(history['accuracy'])
    plt.plot(history['val_accuracy'])
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('Model overview')
    plt.ylabel('Percentage')
    plt.xlabel('Epochs')
    plt.legend(['accuracy', 'val_accuracy', 'loss', 'val_loss'], loc='upper left')

    figure = draw_figure(window["-PLOT-"].TKCanvas, fig)

def find_model():
    global models_list
    dir_list = os.listdir(os.getcwd())
    for dirs in dir_list:
        if "model" in dirs:
            models_list.append(dirs)
    return sg.Listbox(values=models_list, size=(100, 10), select_mode="LISTBOX_SELECT_MODE_SINGLE", auto_size_text=True, enable_events=True, key="-MODELS-")

model_listbox = find_model()
model_acc = sg.T("-", size=(20,1))
model_val_acc = sg.T("-", size=(20,1))
model_loss = sg.T("-", size=(20,1))
model_val_loss = sg.T("-", size=(20,1))
model_plot = sg.Canvas(key="-PLOT-")
visible = "model"



model_col = sg.Column([[sg.Text("Models found:")],
                       [model_listbox],
                       [sg.T("Accuracy: "), model_acc],
                       [sg.T("Validation accuracy: "), model_val_acc],
                       [sg.T("Loss: "), model_loss],
                       [sg.T("Validation loss: "), model_val_loss],
                       [model_plot]],
                        key='-COL-MODEL-')


train_col = sg.Column([[sg.Text("Train", size=(10, 1))]], visible=False, key='-COL-TRAIN-')

test_col = sg.Column([[sg.Text("Test", size=(10, 1))]], visible=False, key='-COL-TEST-')

layout = [[sg.Button("Model", border_width=5, size=(10, 1)),
           sg.Button("Train", border_width=5, size=(10, 1)),
           sg.Button("Test", border_width=5, size=(10, 1))],
          [model_col, train_col, test_col] ]

window = sg.Window("AI assignment", layout, size=(800, 800))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Model":
        find_model()
        window['-COL-MODEL-'].update(visible=True)
        window['-COL-TRAIN-'].update(visible=False)
        window['-COL-TEST-'].update(visible=False)
        visible = "model"
    if event == "Train":
        window['-COL-MODEL-'].update(visible=False)
        window['-COL-TRAIN-'].update(visible=True)
        window['-COL-TEST-'].update(visible=False)
        visible="train"
    if event == "Test":
        window['-COL-MODEL-'].update(visible=False)
        window['-COL-TRAIN-'].update(visible=False)
        window['-COL-TEST-'].update(visible=True)
        visible="test"
    if model_listbox and visible == "model":
        print(f"{values['-MODELS-'][0]}")
        fill_model(values["-MODELS-"][0])
window.close()
