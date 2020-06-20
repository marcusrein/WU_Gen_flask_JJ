
from getters import *
from checks import *
from droms import *
# import SlimSelect from SlimSelect
# from fuzzywuzzy import fuzz
from flask import Flask, render_template, request
# from PIL import image

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def first_page():
    from exercises import exercises
    from droms import droms

    exercise_keys = exercises.keys()

    metcon_time = 'metcon_time'
    drom_time = 'drom_time'

    # length_of_x = len(x)
    if request.method == 'POST':
        # intensity = request.form['intensity_form']

        exercise1 = check_exercise_fuzz_80(request.form['exercise1_form'])
        exercise2 = check_exercise_fuzz_80(request.form['exercise2_form'])
        exercise3 = check_exercise_fuzz_80(request.form['exercise3_form'])
        exercise4 = check_exercise_fuzz_80(request.form['exercise4_form'])
        exercise5 = check_exercise_fuzz_80(request.form['exercise5_form'])

        exercise1_toggle = request.form['exercise1_toggle']
        exercise2_toggle = request.form['exercise2_toggle']
        exercise3_toggle = request.form['exercise3_toggle']
        exercise4_toggle = request.form['exercise4_toggle']
        exercise5_toggle = request.form['exercise5_toggle']

        todays_wod = [exercise1, exercise2, exercise3, exercise4, exercise5]
        todays_wod_toggles = [exercise1_toggle, exercise2_toggle,
                              exercise3_toggle, exercise4_toggle, exercise5_toggle]

        metcons_compiled = get_movements_compiled(
            todays_wod, todays_wod_toggles, metcons, metcon_time)
        selected_metcon = metcons_compiled.get('SELECTED MOVEMENTS: ')
        cleaned_metcon_reps = ''.join(str(x) for x in selected_metcon)
        metcon_reps = get_metcon_reps(cleaned_metcon_reps)

        droms_compiled = get_movements_compiled(
            todays_wod, todays_wod_toggles, droms, drom_time)
        selected_droms = droms_compiled.get('SELECTED MOVEMENTS: ')

        img_list = []
        for drom in selected_droms:
            img_test_drom = droms[drom]['img']
            img_list.append(img_test_drom)

        tester_dict = dict(zip(selected_droms, img_list))

        return render_template('index.html', droms_compiled=droms_compiled, selected_metcon=selected_metcon,
                               metcon_reps=metcon_reps, exercise_keys=exercise_keys, selected_droms=selected_droms,
                               tester_dict=tester_dict)

    else:
        print('else block called$$$$$$$$$$$$$$$$$$$$$$')
        return render_template('index.html', exercise_keys=exercise_keys)


if __name__ == '__main__':
    app.run(debug=True)
