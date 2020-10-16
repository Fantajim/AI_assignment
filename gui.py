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


"""import PySimpleGUI as sg

BG_COLOR = '#1B1B26'
INPUT_BG_COLOR = '#2C2C37'
BUTTON_BG_COLOR = BG_COLOR
TEXT_COLOR = '#FCFDFF'

def the_gui():
    sg.theme_background_color(BG_COLOR)
    sg.theme_element_background_color(BG_COLOR)
    sg.theme_input_background_color(INPUT_BG_COLOR)
    sg.theme_input_text_color(TEXT_COLOR)
    sg.theme_text_color(TEXT_COLOR)
    sg.theme_button_color((TEXT_COLOR,BUTTON_BG_COLOR))
    sg.set_options(text_element_background_color=BG_COLOR)
    sg.set_options(border_width=0)

    # --------------------- User defined elements ---------------------
    # It would have been better to render the buttons with the red line
    # rather than trying to line up the red line images. Space varies depending on OX
    def top_button(text, image_key, set_as_default=False):
        col = [[sg.Button(text, size=(10,1), font='Helvetica 13 bold', button_color=(TEXT_COLOR, BG_COLOR))],
               [sg.T('    ', font='Helvetica 13 bold', pad=(0,0)),sg.Image(data=red_line if set_as_default else blank_line, key=image_key, pad=(0,0))]]
        return sg.Column(col, pad=(0,0))

    # --------------------- BEGIN GUI DEFINITION ---------------------
    # This is the first of 4 Columns. It holds all the stuff to show when
    # the "Tasks" button is selected on top. Each button will have an column
    # When a new top-button is selected, the previous Column is made invisible
    task_col = sg.Column([[sg.Text('3 Tasks', size=(10,1), font='Helvetica 15 bold', key='-OUT-TASKS-'), sg.In(' '*20 + 'Search', size=(28,1), key='-SEARCH-', font='Helvetica 13'), sg.B(image_data=plus_button, key='-PLUS-')],
                          [sg.T('  Store    Product    Size   Profile    Proxies     Status', font='Any 10', text_color='#505063')],
                          [sg.T(size=(1,4))],
                           ],
                         key='-COL-TASKS-')

    bottom_buttons_col = sg.Column([[sg.T(background_color=INPUT_BG_COLOR, font='Any 4')],      # some padding at top and bottom of box
                                     [sg.B(image_data=green_button, key='-GREEN-', button_color=(INPUT_BG_COLOR,INPUT_BG_COLOR)),
                                     sg.B(image_data=yellow_button, key='-YELLOW-', button_color=(INPUT_BG_COLOR,INPUT_BG_COLOR)),
                                     sg.B(image_data=red_button, key='-RED-', button_color=(INPUT_BG_COLOR,INPUT_BG_COLOR))],
                                    [sg.T(background_color=INPUT_BG_COLOR, font='Any 4' )],],
                                   background_color=INPUT_BG_COLOR, pad=(0,10))

    layout = [
                [top_button('Tasks', '-L1-', True), top_button('Profiles', '-L2-'), top_button('Proxies', '-L3-'), top_button('History', '-L4-')],
                [sg.T()],
                [task_col], # Add the other main window columns here
                [bottom_buttons_col, sg.T(' '*90),sg.Button(image_data=captcha_button, key='-CAPTCHA-')]  ]

    window = sg.Window('Shopify Mockup', layout, use_default_focus=False, no_titlebar=True)

    top_button_selected = 1
    while True:             # Event Loop
        event, values = window.read()
        print(event, values)
        if event in (None, '-RED-'):
            break
        if event == 'Tasks':
            window['-COL-TASKS-'].update(visible=True)
            window[f'-L{top_button_selected}-'].update(data=blank_line)
            top_button_selected = 1
        elif event == 'Profiles':
            window['-COL-TASKS-'].update(visible=False)
            window[f'-L{top_button_selected}-'].update(data=blank_line)
            top_button_selected = 2
        elif event == 'Proxies':
            window['-COL-TASKS-'].update(visible=False)
            window[f'-L{top_button_selected}-'].update(data=blank_line)
            top_button_selected = 3
        elif event == 'History':
            window['-COL-TASKS-'].update(visible=False)
            window[f'-L{top_button_selected}-'].update(data=blank_line)
            top_button_selected = 4
        # indicate which button is currently selected
        window[f'-L{top_button_selected}-'].update(data=red_line)

    window.close()

if __name__ == '__main__':
    blank_line = b'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAGCAMAAABwz6mBAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALMw9IgAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAFUlEQVQoU2P4TyMwajAcDDWD//8HAKuCDg94rot1AAAAAElFTkSuQmCC'
    captcha_button = b'iVBORw0KGgoAAAANSUhEUgAAAHMAAAArCAMAAAB8QEdOAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAABYWGRQUHBYXHBcYHBgZGxkaHhcXIRkZIRoaIBwbIRwcIRwdIh4eIB0eIx0dJR4eJh8fKR8gJSAfJSAfJyAgIiAhJSAgJiIiJCEiJiQkJiAgKCEhKyIiKCIiKiIiLCMkKCQjKSQkKSQkKiYmKCUmKiQkLCQkLiYnLCYmLicoLCgnLSgnLygoKigpLSkoLioqLCkqLiwtLyYmMCgoMCgoMioqMCoqMioqNCssMCwrMSwrMywsMSwsMi4uMC0uMiwsNCwsNi4vNC4uNi4uOC8wNDAvNDAvNzAwMjAwNTAwNjIyNDEyNjQ0NjAwODAwOjIyODIyOjIyPDM0ODQzODQzOzQ1OTQ0OjY2ODU2OzQ0PDQ0PjY2PDY2Pjc4PTg3PTg3Pzg4Ojg4PTk4Pjk6Pzw8PjY2QDg4QDg4Qjo6QDo6Qjo6RDs8QDw7QDw8QTw9Qj4+QD0+Qj09RTw8Rj4+RD4+RkFBQ0FCRUNERkJBSUJCSkNESEZGS0VGTEpKTkhIUEtMUUxLUExNUU5PVE9QVFBRVVFRWVNUWVVWWlVVXVhYWlhZXVhYYFxcZF9gZGBfZGFiZmZmamxsbmtscW1uc21udHFydnJzeHJyenN0eXR1eXV1fXh5fXx8fnh4gH59gn+AhIGChYOEiIWGiYqKkoyNkoyMlJCQkpKRl5GSl5OUmZeXn5mYnZubo5yboZ2eoqGipKKiqqOkqaurrampsaytsq6utbCxtrO0uLS1ura2vre4vLi4urm6vby8vru8wby7wb2+wsHBxsXGysTEzMbHzMbGzsnKzcvM0czL0M3N0c7P1M7O1s/Q0s/Q1NDP1dDQ0tHS1tPU1tTU2tbX2dbX29fW3NfY3NnZ29nZ3dvc3tzd39ra4dra5Nzb4N3d4t3d5d/g4uHi5+Pk5uHh6ebn6efo7Onp6+jp7ezs7unp8err8Ovr8+vs8O3u8ezs9O/w9PDw8vDx9vP09vT09vLz+PP0+PTz+PX2+vb3/Pf4/fn5/vv8//z7//7+/gAAAFDaIzYAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAG1UlEQVRYR72YDXgbZR3Ai+IUmF1FoBtZk7qapAkb2fXey13W3u4ud1lZd1566bauSTuRDrqVjoIMqw46GHaWMRXUgc5PwPmt42N8jO91aGGPDhUUC0MUdUYmAeLQshv/8H+Ta7KSdGzPQ/jlefrk7t78f/e+9977/7+tyOTxst4ywbJely2hTDidHsLzapmQZZknHtuUd3p4OXupPNDgKmpzrpzTR3j7annhc33NOqmyjN3Mw/vyTlZRNEQpPwI7O+f0UiM9IeQulBU265wtRPG7QMmdLiOaJuBLU4Eji53MKt8TJ3a0YrYStaX2+fIicK5MhUuLCvg4UYl/5Umfdx86mN5MBU7afA9lMffhJU+wJ+IxYwrr4qKKVxNwMFguyrGXe12Xc7kpLggaMYjHaCamQYxmH2lsVrxK1MtiHwQXl4iyXDbo0Qga/niSU5bFHLWdem2939/qUhIXxTQtmqDCGLo5VolpnFfgOLxhTmg2zl9G5vJzlzUajc09shyLYWtN4Lwa3i0XW23HLXAMZ5ipjazrqGcSKMEVWvgIK3B415rR45DJh0yDR+grLp/haSTn9zpmOJY1qsYZhgub4eRIsALemcJ90I5b4BhOXQ+HGH9knQ9/fFEiqiVWX0y7Ks8w+bhJujzoo0sXUc1lvMPXOLfLjHtI89zPrY7iaHBKIoF3yCYupu/gZI7h9Le0+v1t0vtVwyBOp8fHO2d4VFMlXWJNXUhk3KFImPGHxKDYfk710qXB9kDLokBLZ+AUucqjYnYiPhLvIlUOnx23QAmnrRTDp9d36OGOVYbB+9TeuNMR/7TqJIYRnsMs193+C+oi7RLTFJFqFoita8Xq4McW1H1S/OjaFucVvUQ2cdANnpim2mPHLWA7ffS52NhKsTPYEq7s/8lTL/3mBz3vc5jxb9z/2LdIlRza/ewfn37oluEP7Bp95g979/5+31B194//lH7ql2uq1z35aPfSmg2P7exVZfKl/b/eWuXgPcVZA8dAVUs7A62hU67eA6/vB7hnEyHyToCfmXJ81gvw3N8B/jY8+k+AQ4fG/3vJ4AgkXwBrb/upAN0L2nvhpa4qR3ynBXfEiYE5+e3YTr6gzDulVr1+u/XMmtot+2BrDRM5/KqV7A7Pak3CZ88c+C3cNn9hwxhsbmhY9PPxsQtahv8CX2kat7rn6OvhxZVMsC+VOvx6/8ppYd0OW+AYzrbpYeaAtUNqn/O1n36xb+XW9K7RN24W+5h0amgJsyN9O7Ow6VnYLDVNH/v/ju7ASTd+7yb3m3DNWnEIDp6+puUm695HrBuquzum22EL2E4hP4UKcygSqQmm4Wr38tMWu89l3CPw5Zth5GTdDy9+/YZvHoBbgpI4BtdLTd0WXD9v3oULP37e2Rb8G8CCA5I+7QHYtg1G3LpfL1o+7Tl0tHNCWqfXdx6EVf3u5W2VfdLy/8ElA6nx9SH/AUhj3D3BYFjcj05xEQ722Z+49KRPzVwBqYcfvGt3KqlXDkFK6ng5vb5yWvuJOFsrO1oPjm+qZpoGb/yCdCuk7h4B6/uhy96wfvHD727owldQ3g9bZHHxv2Djinlnbv7q5pkAKxoWDsJ426zb0skRbP5tJhI6EWebJNXeCfescV85CtuYkdSRIzAOu88SX/nP5309zhnxCee0hw49+OFLB34H31liwfyZ53XAmC6NQvpI6lXYo0snNrb91aGhJIzctw/GVl0G0Fc7ZyAJw9JfYZMQpclWU56HLYq8aBBe+/OPUtbTSxpeG//M/HkbIR0ZsJLXRPThl63BSv9xOPO5zAySNt+1/7AOw6+uCmyHu+v0lYF9sC3yCiQwT2mYxahTkztPGxrDmfPElUsDb4IkLd6YTrZvh13ucHXwcbi1PzCVc1KSy+drgVeMWOd1Vxk+XDPy2K3yqLjGXXHdBmJfLsJuVoBWBkJ2vS0BvRiNYS4TtFhxepiA1hhKIlY6RCloAWRO7aS1CqZmmoOnjMlqCY1lucLDeSeok0NnyV/QwoVasVDiuOIaw4YmS9rEPjw+2EyFd2ongkocXftkETF2NhfFWsQ+fEeoitZgpZy2UChRRU0iW/1PPQxF4MgptNZ0FmccOVvt5KBbuKOn7iR41cC6wD44DnBPKBMnOkvM9Ik4BgplLFByR8UQ3ueRTZXWR8dF1unAvYODN1GR2w2Xi1yhqBLZ4B3ZfRl5D3aeWSv10h0oOl04CeiMsR90GaCFPzVoysT+M+OyfWWz4nueneJRjiqzzgyW6tmaP9eiHNhWL7XlnBkXXY3K58Tg2RUtp7Sd1IrbHrvJuw4NLBT+LzXhxAEu49DiDGInjJnMW4afJfH6bdHpAAAAAElFTkSuQmCC'
    green_button = b'iVBORw0KGgoAAAANSUhEUgAAABMAAAAWCAMAAAAVQ1dNAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAABR4Rh91SB15Rhp5TSV3RyZ8SyV6Ux6HTCaDTiqHWyyDWCiKUSuTViiXVSicWzODXD2BXDCaWjKbYzyZYDKjYTGjaDelaDGoZDmrbzyqazumcj+wcD25cTnCdD3BdTTUcjLeeDrcdT3feDPgbTLiczLjdzPlczDkdjbkdTfldjTmdjXndzPkeDHneTbmeTXmejblfDblfjTnfzXudzHpejHofDfofDTofTXseDnldTnkdzrmdjjmdz/gdj7idT3jdz3mcz3ldjzkdzzmdTvhfTrjfDnifTrjfjrkeTrleznkfjrnfj7heD3ieTzjej3kejzmeT/odT7pdzroeTjoezzoeDzufkCAZUaJZk2SdVSPeUWrakKpcUmkeE23d0DJd0bLfEjCdUrNf0DddEXce0TefkXff0jdd0/cfk3ffUHic0DidUPkckDkc0Pmc0LkdEPldkLmdULmdkDjekHjfEPleEDoeTbmgTvlgjjngDzkgjzsgEi7glu6gl29j26+m0fOgkvEgUrMhk3Lgk3KhkzMgUzOhEzKiELYgUnQgUrTg0jWgkvWhU/ShE3VgE3VgU3UhU3XiUjbgEvagkrag0jfgkjehUjciE/YiFLGiVHLglLJh1LOhlDNi1LNjFfOjFjLhlzMhFnMi1PRh1TUgVbVjlXagVLZjFnTilLckVfbkFvalUPjg0PhhEPghUHihEPihULkgUDmgkDlhkPkh0PnhELmhUXhgEXggkTigUXjhETihUXjhkfih0Tkgkbkg0TkhETiiUfki0HrgUvig0jmh0/gg0zgiFDmjFvjj1LmkFjjkFrokmLGlGfDkGbPl2rCmGPYkmbZnmbgkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACXBECsAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABQ0lEQVQoU2P4H8X+Hw0w/K+vlWSGcqCA4f+FNcviRVihXDBg+L94Us+VRTE8UD4IMPxfMn1H5vKlSRIcUBGQ2MSDR1Iyso5PleeDCgHFul31ywtzSrbtS5ThgonNdNdQcQzW0q0+sWKeGCNErHGLQZiLlbae0brp6zvl+MFizVsNA52sdEyNN6xVqzmQIMoGFOs45O3nYK1vVrFxk6VJwOSVdYIgMQ9fe2dbi6o9u1TVladcOh/J8L91n5tdtr2Nuc/OaQrHzs6NFQDqbdnrn5Od5xLqlT7lzOomYbAdbbutC3Lzg0I8UycskGaBuCV5v7VLUXFZaVr/Qm6QCEisa7tauKbS0VOzhSAiILH2w5WKm0/2SXFCRUBis1bNON0rywvlgwDD/3OX588Rh/IggOF/w8U4JigHChj+R0dAmVDw/z8AkbkcWUjJmvYAAAAASUVORK5CYII='
    plus_button = b'iVBORw0KGgoAAAANSUhEUgAAABoAAAAYCAMAAADTXB33AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAAsbGAUpHQ01Kgo9KhUlIhEjLREqLxkpKB4qKhwtKR4sMBwsORI2KBE2LhY1LRA4LRkwJh00JBsxLh4xLR00Lhs+KBw9LBY3MBk2NB4yOx46MSAfJSEdKjMdLDgfMiM0GSM7GSEnJyAjKiMjLSMmKyUkLSAtJiIpLSIsLSUpLSUuKyglLS4kLCkoLiosKSgtLi4sLyIlMSUjMCYmMCAqMSMpNSYqMScrNCYuMSUtNCQtOCkmMSklNC0nMSkpMioqNCktMikuNS0qMS0qNS0tMSwsNSktOC4uOC0vPCI0JCQ4LSc8LSAxMSEwNSA0MiYwMSUzNCU1MSY2NCEyOiA1OiYwOSc1PiM6MiM5NiA+NCY4MiY7NiU9NyA/OSkxNCk1Ni4yMy4wNCgyOSk2PS8yOS43Pio5My05Oi45PzMnJzUmKzEqLjgpJjUjMzEqMjErNTAuMTEuNjUpMzQvMzYvNzQsODspNzksOz81KTEwNTY5MjU7Ny01QDE6RAJRMQ9XMhtNKh1DNhdZPh5VPg5kJQlmNxVhMCJCNyVANyRCOCZJMyZOMydOOSdOPClAOi9MNihKPC1JPS1NPiVXJCFZKCVUMi9YOCxdPTJAMDRAMjBEOTFSPzhRNDRpOxVeQQ1/QRltSy1ARylFSC9fRy9ZSzFQSDJcRiZiSSBtTS5qSCRxQzNlQDZjTzthVDB6STp2UkJrXURvXEh2XB+KOiicVTSGRDWMVTiIUz6QXzqdbjWgXDKzVjyyXjSlZzK6Zj2+azfDYj3LdzvbbTHXczjYdC/ibTXmdDvrfj/pfD/wfkWaVlGMXEGNZ0uObUKbZUWbbkqQa0mSdFaJaFCTcFeZfUGiXUSpZ0C6cUjDckDVd0PbdkXadkPeeUXff1LBf0HsejjPgD/eimWwkUrKjU/XjUnfhk3YhUvcj03UklbLh1rPi1jEkFvOlV7JlV3NlVPXg1TYhVvZhVvcgkfjgErnjlDngFHljVfhlmbKlmrDl2zLk2DQmGnWk3PelgAAAEiibAcAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAACNElEQVQoU2P4Dwc5/3Ny8p311KDc/1ApHR0958JCQ9eiqiJnG6gkRMquqCop0UDJwMBAz965oMgELAiWcnbWU9UMCg6Kjg4KcHR2cXOxV4FIqdmUudhb+opKd3R1xgbHu7kVubmB5Bj+q9gDWfEZkfxNSzeuW9YfHOBW5ACWY/iv5uDhoaEVwMW74tLjq5smiXBqxms5eLiZ/GcwcbB3CkuTKakWa3vy8v2GCT7egjFWDvYODiYM9g727qYpWjWzpi14+OjpjjU93eIRlg5AYMLg4OaQapIQtXzG+q2Hnj3fvX31qjnpjm4g2xgcPBw8Uv1bzu68fuDWl3v7b+y7sHk20JUgKTcPh6QMgYVvXn+8e/L4iSNfX7y9Mjnew83DwwEkFR/MvPLn30+3Hxw7dfT7jz/nJiZAdbnZO1mJ9F0+c3rP4cPf9l47f3FtbLwbyK8gKTcPJ+2ZClO2HLzzedvUxl5pXyc3V5CUmpubg6eDblalYuvND//mzfUK4vZztAcCNYb/9m5O1u5l2bkK7fdf/Z4+Uz0hNNwCZB5QSs3enUcqRVNfqGHXu19LJklKsrNZuXm42YNC3sQ6RCqUOymdZX59M5Ow5OJFde4ebg6Q+DJ3t0o2Ly7lkOCL43TiNpWVBcuApZT1NDJc5fJsMv2SyypcPCoqXOyBomCp/1ysQUly8i511kZ5eTr2hUWQxAGW4mTkTCqvsDWrNaqocEt01gHLQKQgwNjIwQGWmv7///8fAJ7/NhA3zMv/AAAAAElFTkSuQmCC'
    red_button = b'iVBORw0KGgoAAAANSUhEUgAAABYAAAAVCAMAAAB1/u6nAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAF0jPF0mO18lPWEYM2EbNWAcM2AfN2QZN2cbNWQeNmEdOWAdPGYaOGQdO2oTNWoVNmwXOGgcNmwZN2gbO2keOmkePG0YOGwdOm4ePXAKL3MKMnMPNXAXNXIXNnIXOHAaPXEcOXIdOnIfOXUZOXcZPXYcOHYdPXwTO3oZPHocPnofPn0ZPWEjOGEhPGQiPWQkPGkgO2ohPGwiO2wgPG0hP2wkPHAgO3YgPXUZQH8bQWwmQGwrQ4cOO4QQNYMWPYAXP4UXPIEdP4UaPYYdPooTO4sVPZMPN5YYPoMdQocfRIsWQYkbQIocQ4geRI0YQo8bQo4aRJsOQpAQQJEUQJUXQpYWRpIZQpUbQpYeRJMbSJIfSpgUQp0VQ5wXRpkaQ5gbRZ4ZRoAhQYUiQYwjS5UhRqQPRqsMRKYSRKEYRqEZSaYeTqsTRqgURK0XR6kSSakVSa0VSK8ZR6sbTKwYSq8bTb0MQ7IQQrAURLAWTLEaT7oTR7oVTb0VSb0VTrkcT70ZTr4ZUaIgTq8gTKYgUqogUakkU6klVLMgVLcjV7MkWbQkWbkjU7ojWMIOS8ENTMUPTMQSTs8TTcUSUMUXVMYeWc0XVMgbUcodVc0ZVMsdWM4aWdcMTNIOUNsPVtYQTdIWU9AWVdQSVdUUU9QVWNAaVdAdVdcaVNMZWNYZW9kSU9sSVtoWVd4RUt0VWN8ZVtsaWdgfWdwaWd8eYcEgUscjWMggW8siWc8gW9MhX9YgXdUjYeMHUeIIVOMMUOoOVu0KVOwPVOgOWO8OWuMRVeMRWOUQWOcWWuQZWOQdXugRV+gWV+4TV+oSWusUWeoVXOwQWO4VWegaWukYXOoYX/IKVfYJVvYMV/ENWPMMWvAOWPMPWvANXPYJWPUNWPYPX/8GVvoHWf8CWv8EWP8EWv4GWP8HW/8FXfoIVfwKVvkKWfkMWfkOXf4JWf4KXP0NXPERWvASXfQQW/YWX/kQX/4QXOEeYukXYO0bYv8OYvYSYfUUYPIYYuIjZucgYQAAAAr+GkYAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABy0lEQVQoU2P4zyjCL2D0HwG4OFn+/2f4Lx6dnRUgBxX7r5ycmuonDhR26N69ojFRTRckKOSYN2Pp9jat/wx6Udu+H76yI17W4P9/E5/CVZ9vnewECouFzb7/5OefhlAvdRXf0gX33r293KH+n4HPdsqv589frdlaHBdTMvPc2yfv1zWZAs2WKZh3992z/f8WTp648Pint2/P1ngyA4W57dPn/npz9cP5Y8fO3rv76sK0GF6QA///18ycef7NtVsf7l17+/XD4gwnoBBImCmpZNG9t6/fv3384OqccjdDqPB/s5i+A+/evn379MW+MndFkAhY2Dx2woF3D54+fXtvbbWHEkxYIrxm9Q2g2pf3Lq6f3uwMCiCgsGho3bqPt699vX7w9KUTa5bl+IuBhPUDJx96/+7ehSPzJy0/ceb66z393jxAYavKY++ePzy1obaiaMvGcw+ePNmbb/mfgTdoyZfnb87P7Il0cY6o3/T60fM3U7z/MwimLbpz88euXDsLM2PthJojb96drXNjY+AInvp386wSVxXW///Z5UNqVn7b2aoDNFujpbcqzlHRBuTc/8KB2V3tKaJAYTFVaSl1a7AgEOhJKkhy//8PAMoKLCsLw4FtAAAAAElFTkSuQmCC'
    red_line = b'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAGCAMAAABwz6mBAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAKMXRqQRR6QfTqwUR6oYR6oYSakZSrEYTrkSSroVTb0WTLsdUK4hVbohWbojWMcPT8IUT8cRTsUTT8QXT8kRT8gWTsISUMMTUcATUsAXUMUTUcYXUMQbUsgRUcgWUMgVVs0TVMwUUM4VUc8WUs8XU88XVc8UWMoYVssYWdEVUtMVU9AWU9EUWNAdV9UYVtcYW9oTVtgXWt4cW90cXdoiXusJU+0LVe0NVu0MWOITV+QSW+QXWuYeX+sRW+gSWOoSWekWW+oUXO0QWe8RWu0QW+8RXO4QXfUKV/EOWfANXPAPXfMPXvcMWfQNW/YNXvoHV/8CWP8DWf0EWP8FWv8HWf4GWv4JWf8JWvwJW/0KWv8LW/4MXPwOXPAQWfERWvMWXPQRWfQSWgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK5kYR8AAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAqklEQVQoU2P4zySprquooKGmAwEq5AEtbW0dHVVVVR1lJXlZHtb//xl4Na19/P283eI8KQZxzs5xnuYuDlbGpiL/GfiMvMKCAoMDoigEEVA6PMrDzN5Wn42B38A9MiQ4NCqGchAbCySiY3wtHG312RmYpQzt4xOTEpydXSmDDnYOds6ucZbOTjYmepz/Gf7/Z+GWERMTExaWpghKCAKhsJyogJA4Fwfj//8Ar/aGF89us74AAAAASUVORK5CYII='
    yellow_button = b'iVBORw0KGgoAAAANSUhEUgAAABIAAAASCAMAAABhEH5lAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAALWfL7+lN7esQrinS72mSbirQrmqQ7+oSr2nUsGmPcGlQcOnRMCnSsKnU8OmVsOmWMGnWsGoUcGpU8OqWsSjYMSnY8GoZs2sae/WPvfOJvbPKvrOJfjPKfzMKv/PK/PON/PPPfLOP//HNf/HP/rPM/vMNv3KMf7LMv3KM//LNv/NMP3MMf/MM/7OMP/NNf7ON/jLOvrJPvrOOf/LOf/IPP/LPP/KPf/KPv/MOv/MO//MPP/MPv7OPP/PPf3PPv/OP/PSL/bRK/DYLv/RL//SLfPWMPPVNfHWNPLWNfLWN/fTNPfTN/XVNPXUNfXUN/PUPPPUPvbSOfXSPPbSPvfTP/XUOfDYMPnTNP/RMP3RMv/SMP7SM//RNvrROfnRO/nSOfrQPPnRPv3QOfzQO9nAWe/MTOnPVu3OUezOUunOXe3MWO3QRu/URe/TTu7US+7UTO3ZRufRWe/SVO7WUu/RWfXHTfXLQfXLRfXMQPbJSPXPSP3HQP7GQf/FR//HR//ESP/GSf/GSv/HS//HTPvLQ/nPRfrOR//KQP/KQv/JRP/JRf/IR//KRP/KRf/LRv/LR/7NQP/MQv/MQ/zOQPzOQv/MRP3MRf7ORP/ORfzOR/rOSfrOS/nOTv/JSP/ISf/JS/zLSP/KSfzLSv/JTv7LTP3LTvzNSfzNS/PPVPfOWvfOXPbOXf/GUP/GUv/FVP/GVP/HVvrLVfnNUPrMUv/IUP7KUP/LUf7IVP7JV/3KV/vLXfjNXP/IXv3LXPPSRfDWQ/bRQvbQRPbQRfbQR/bWR/TSSvbVSvHZQ/nQQPnQRPjUSPrWTvzQS/PQUPPRU/DTU/LQVPLTVPXTVffTWOTMaubMa+zFYO/Hb+/KYO/PYu/Ia+DOfOfRbu3TZO7SbvPFZ/bJbPTNbvrKY/jMYfPMcfPTZPLUYvfQZ/TRafbVavLRcgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN+7z/YAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAABYUlEQVQoUwFWAan+AP8LCgUEAwYIDQYHCQ4MAgH//wBlz8bQdHHIx8sZwNPUzMVtcv8A6ngxeSFBQi4rGhsxMiYlUtAUAOihPJeUXEQvLR8uNyQjJ2PTEADhuKC4t5mTn5+Jj7GvgH2FrBUA4K6CuLijoq2tfqS9vbWep6wYAOSijaadw8qlpZqcurmilcnRDwC8ljuHxFFQyoZUwbOzlV9SbhIAqpEwyVFIV09WSErDw19LSG8SAKuRMGJTV0NOTkZJwsJgS05wEwDjkDuYwU9NX2FMU5uolF9TcxEA44w4kJdfXpKSP5W2to09YtERAL6KNYyQPDyMgY6isK+LO2TODgC7jTQ4ODo2f4GKi4SDiDuUqQ8A181jW0VZMJKWQDkqKCwze9oWAOtmIB0cHil8fZg+XVpYVdLfFwD/db9STGKHtLJ2enciImxn1f8A/9ZqaWhr2dvY5eLp5ufe3dz/ZdGaljRkmtwAAAAASUVORK5CYII='
    the_gui()
"""
