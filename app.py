from flask import Flask, request, render_template, Markup
import pandas as pd
import requests
from zipfile import ZipFile
import os

def updateData():
    URL = "https://openpowerlifting.gitlab.io/opl-csv/files/openipf-latest.zip"
    response = requests.get(URL)
    open("openipf.zip", "wb").write(response.content)
    with ZipFile('openipf.zip', 'r') as zipObj:
        zipObj.extractall()

def findCsv():
    for folder in os.listdir(os.getcwd()):
        if folder.startswith("openipf-"):
            tfolder = folder
            break
    os.chdir(tfolder)
    for file in os.listdir(os.getcwd()):
        if file.startswith("openipf-"):
            tfile = file
    return tfile

updateData()
file = findCsv()

# df = pd.read_csv('openipf-2022-06-08-1cd7e89a.csv')
df = pd.read_csv(file)
df = df[
    ['Name', 'Age', 'Sex', 'Equipment', 'BodyweightKg', 'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg']]

app = Flask(__name__)


def find_score(sex, max_bodyweight):
    res = df.loc[df['Equipment'] == 'Raw'].loc[df['Sex'] == sex].loc[df['BodyweightKg'] <= max_bodyweight]
    max_total = res['TotalKg'].max()
    id_max_total = res['TotalKg'].idxmax()
    squat = res['Best3SquatKg'].get(id_max_total)
    bench = res['Best3BenchKg'].get(id_max_total)
    deadlift = res['Best3DeadliftKg'].get(id_max_total)
    name = res['Name'].get(id_max_total)
    age = res['Age'].get(id_max_total)
    return squat, bench, deadlift, max_total, name, age


def calc_plates(weight):
    if weight < 20:
        return -1
    weight -= 20  # barbell weight
    side_weight = weight / 2  # one side weight
    side_weight -= 2.5  # collars weight
    plates = {}
    plates['25'] = side_weight // 25
    side_weight -= plates['25'] * 25
    plates['20'] = side_weight // 20
    side_weight -= plates['20'] * 20
    plates['15'] = side_weight // 15
    side_weight -= plates['15'] * 15
    plates['10'] = side_weight // 10
    side_weight -= plates['10'] * 10
    plates['5'] = side_weight // 5
    side_weight -= plates['5'] * 5
    plates['2.5'] = side_weight // 2.5
    side_weight -= plates['2.5'] * 2.5
    plates['2.0'] = side_weight // 2
    side_weight -= plates['2.0'] * 2
    plates['1.5'] = side_weight // 1.5
    side_weight -= plates['1.5'] * 1.5
    plates['1.0'] = side_weight // 1
    side_weight -= plates['1.0'] * 1
    plates['0.5'] = side_weight // 0.5
    side_weight -= plates['0.5'] * 0.5
    plates['0.25'] = side_weight // 0.25
    side_weight -= plates['0.25'] * 0.25
    return plates


def generate_svg(weight):
    plates = calc_plates(weight)
    svg = '''<svg width="200px" height="500px">
             <rect id="bar" width="10" height="83" x="95" y="0"></rect>
             <rect id="bar" width="14" height="6" x="93" y="83"></rect>
             <rect id="bar" width="6" height="262" x="97" y="89"></rect>
             <rect id="bar" width="14" height="6" x="93" y="351"></rect>
             <rect id="bar" width="10" height="83" x="95" y="357"></rect>
             '''
    y1 = 77
    y2 = 357
    for kgs in plates:
        plates_num = plates[kgs]
        if float(kgs) == 25:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate25" width="90" height="5" x="55" y="''' + str(y1) + '''"></rect>
                <rect class="plate25" width="90" height="5" x="55" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 20:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate20" width="90" height="5" x="55" y="''' + str(y1) + '''"></rect>
                <rect class="plate20" width="90" height="5" x="55" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 15:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate15" width="80" height="5" x="60" y="''' + str(y1) + '''"></rect>
                <rect class="plate15" width="80" height="5" x="60" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 10:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate10" width="70" height="5" x="65" y="''' + str(y1) + '''"></rect>
                <rect class="plate10" width="70" height="5" x="65" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 5:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate5" width="50" height="5" x="75" y="''' + str(y1) + '''"></rect>
                <rect class="plate5" width="50" height="5" x="75" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 2.5:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate25" width="40" height="5" x="80" y="''' + str(y1) + '''"></rect>
                <rect class="plate25" width="40" height="5" x="80" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 1.5:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate15" width="30" height="5" x="85" y="''' + str(y1) + '''"></rect>
                <rect class="plate15" width="30" height="5" x="85" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 1.0:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate10" width="26" height="5" x="87" y="''' + str(y1) + '''"></rect>
                <rect class="plate10" width="26" height="5" x="87" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 0.5:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate5" width="20" height="5" x="90" y="''' + str(y1) + '''"></rect>
                <rect class="plate5" width="20" height="5" x="90" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
        elif float(kgs) == 0.25:
            for i in range(int(plates_num)):
                svg += '''
                <rect class="plate025" width="16" height="5" x="92" y="''' + str(y1) + '''"></rect>
                <rect class="plate025" width="16" height="5" x="92" y="''' + str(y2) + '''"></rect>'''
                y1 -= 6
                y2 += 6
    y1 -= 4
    svg += '''
                <rect class="collar" width="20" height="9" x="90" y="''' + str(y1) + '''"></rect>
                <rect class="collar" width="20" height="9" x="90" y="''' + str(y2) + '''"></rect></svg>'''
    return svg


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        sex = request.form['sex']
        bodyweight = request.form['bodyweight']
        sq, bench, dl, total, name, age = find_score(sex, float(bodyweight))
        sqpl = calc_plates(sq)
        bppl = calc_plates(bench)
        dlpl = calc_plates(dl)
        svgsq = generate_svg(sq)
        svgbp = generate_svg(bench)
        svgdl = generate_svg(dl)
        return render_template("index.html", squat=sq, bench=bench, deadlift=dl, total=total, name=name, age=age,
                               sqpl=sqpl, bppl=bppl, dlpl=dlpl, svgsq=Markup(svgsq), svgbp=Markup(svgbp), svgdl=Markup(svgdl))


if __name__ == "__main__":
    app.run()
