from PIL import Image, ImageDraw
from math import ceil, floor, pi, cos, atan, tan
from scipy.interpolate import interp1d
import PySimpleGUI as sg

sg.LOOK_AND_FEEL_TABLE['MaterialDark'] = {
    'BACKGROUND': '#333333', 'TEXT': '#FFFFFF',
    'INPUT': '#424242', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#424242',
    'BUTTON': ('#FFFFFF', '#007ACC'), 'PROGRESS': ('#000000', '#000000'),
    'BORDER': 0, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'
}
sg.ChangeLookAndFeel('MaterialDark')

modes = ('Planetocentric to planetographic', 'Planetographic to planetocentric', 'Lambert to planetocentric')

layout = [
    [sg.Text('Import file', s=20), sg.Input(key='open'), sg.FileBrowse()],
    [sg.Text('Export file name', s=20), sg.InputText('script-result.png', key='save')],
    [sg.Text('Projection mode', s=20), sg.InputCombo(modes, s=30, key='mode')],
    [sg.Text('Oblateness', s=20), sg.InputText('0.06487', key='obl')],
    [sg.HSeparator()],
    [sg.OK(), sg.Cancel(), sg.ProgressBar(100, size=(40, 20), key='progress')]
]

window = sg.Window('Celestial Reprojector', layout)


# window launch

while True:
    event, values = window.read()

    if event in [sg.WIN_CLOSED, 'Cancel']:
        break
    
    elif event == 'OK':
        mode = values['mode']
        obl = float(values['obl'])
        img_old = Image.open(values['open'])
        pix = img_old.load()

        w = img_old.size[0]
        h_old = img_old.size[1]
        if mode == 'Lambert to planetocentric':
            h_new = floor(h_old * pi / 2)
        else:
            h_new = h_old
            
        img_new = Image.new('RGB', (w, h_new), (0, 0, 0))
        draw = ImageDraw.Draw(img_new)

        if mode != 'Lambert to planetocentric':
            n = (1 - obl)**2
            hpi = h_old / pi
            pih = pi / h_old

        for x in range(w):
            line_r = []
            line_g = []
            line_b = []
            for y in range(h_old):
                line_r.append(pix[x, y][0])
                line_g.append(pix[x, y][1])
                line_b.append(pix[x, y][2])
            interp_r = interp1d(range(h_old), line_r, kind='cubic')
            interp_g = interp1d(range(h_old), line_g, kind='cubic')
            interp_b = interp1d(range(h_old), line_b, kind='cubic')
            for y in range(h_new - 1):
                if mode == 'Planetocentric to planetographic':
                    y_old = hpi * (atan(tan(pih * (y + 0.5)) / n)) # planetoCENTRIC to planetoGRAPHIC
                elif mode == 'Planetographic to planetocentric':
                    y_old = hpi * (atan(tan(pih * (y + 0.5)) * n)) # planetoGRAPHIC to planetoCENTRIC
                else:
                    y_old = h_old / 2 * (1 - cos(2 * y / h_old))   # lambert to planetoCENTRIC
                if y_old < 0:
                    y_old += h_old - 1
                if y_old > h_old - 1:
                    y_old = h_old - 1
                r = int(interp_r(y_old))
                g = int(interp_g(y_old))
                b = int(interp_b(y_old))
                draw.point((x, y), (r, g, b))
            window['progress'].update_bar(x / w * 100)
        
        img_new.save(f'{"/".join(values["open"].split("/")[:-1])}/{values["save"]}')

window.close()

