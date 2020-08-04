from flask import Flask, render_template, request, url_for, redirect, session, flash
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from barbell_warmups import *
from kb_warmups import *
from getters import *

app = Flask(__name__)

app.config['SECRET_KEY'] = '2fc1cdd26003685f749bd3e217824aca'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out')

    return redirect(url_for('/'))


# JJ HELP TODOS
# TODO: expanding to XL messes with formatting
# TODO Padding on L of R big screen column does not respond
# TODO: better dropdowns/navbar ideas
#  TODO: * Get screen orientation to lock in portrait mode
# TODO: login with user database
#

# MDR TODOS
# TODO: Continue to update gifs/vids (ended on kb_warmups.py)
# TODO: Get all links to not be separate buttons but the title or image of the movement
# TODO: ONLY ONE CORE WARMUP IN DROMS
# TODO: Default selected length is "normal". Fix the way its carrying over after submit.
# TODO: need to differentiate olympic lift warmup and strength/squat warmup. If olympic lift is in 'easy' warm up one way, if olympic lift is 'tough' warm up another. If strength movement is combined with oly movement in a WOD...?
# TODO: need an overhead squat category. see barbellwarmups.py 'overhead squat warmup'
# TODO: If forced core exercise, only allow one core exercise in output (line 62 getters.py)


# LONG TERM TODOS:
# TODO: add draggable inputs
# TODO: Create banded section.
# TODO: 1. Create DB category throughout code, 2. fix bug in index.html that doubles-up input (it lookslike
#  I can put in airsquat 2x) 3. create 'equipment' thing. 4. have users log in

@app.route('/', methods=['GET', 'POST'])
def first_page():
    from exercises import exercises_dict
    from droms import droms_dict

    alphabetical_exercises_dict = OrderedDict(sorted(exercises_dict.items(), key=lambda x: x[0]))
    exercise_keys = alphabetical_exercises_dict.keys()

    metcon_time = 'metcon_time'
    drom_time = 'drom_time'

    warmup_duration_selection = ''

    if request.method == 'POST':
        # INPUT
        easy_exercises = request.form.getlist('easy_exercises_form')
        easy_exercises = [easy_exercise.lower() for easy_exercise in easy_exercises]
        tough_exercises = request.form.getlist('tough_exercises_form')
        tough_exercises = [tough_exercise.lower() for tough_exercise in tough_exercises]
        # breakpoint()
        warmup_duration_selection = request.form['option']
        warmup_duration_short = 'on' if warmup_duration_selection == 'short' else False
        warmup_duration_long = 'on' if warmup_duration_selection == 'long' else False

        # TODAYSWOD

        todays_wod = easy_exercises + tough_exercises
        error_message = check_no_input_todays_wod(todays_wod)

        # METCON SELECTION

        metcon_warmup = {}

        metcons_compiled = get_movements_compiled(
            todays_wod, tough_exercises, metcons, metcon_time)
        selected_metcon = metcons_compiled.get('SELECTED MOVEMENTS: ')
        metcon_reps = get_reps(selected_metcon, tough_exercises, metcons)
        metcon_images = get_images_for_display(selected_metcon, metcons)
        for idx, item in enumerate(selected_metcon):
            metcon_warmup[selected_metcon[idx]] = {'img': (metcon_images[idx]),
                                                   'reps': (metcon_reps[idx])}

        # DROM SELECTION
        drom_warmup = get_droms_compiled(todays_wod, tough_exercises, drom_time, selected_metcon, warmup_duration_short,
                                         warmup_duration_long)
        print_for_debug = get_movements_compiled(todays_wod, tough_exercises, droms_dict, drom_time)
        # KEY CODING TO COMBINE MULTIPLE LISTS INTO A SINGLE DICTIONARY  #
        drom_final_dict = {}

        drom_img_list = get_images_for_display(drom_warmup[0], droms_dict)
        drom_reps = get_reps(drom_warmup[0], tough_exercises, droms_dict)
        drom_url = get_url_for_display(drom_warmup[0], droms_dict)
        drom_counter = ['1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ', '10. ', '11. ', '12. ']

        for idx, item in enumerate(drom_img_list):
            drom_final_dict[drom_warmup[0][idx]] = {'img': (drom_img_list[idx]),
                                                    'reps': (drom_reps[idx]),
                                                    'url': (drom_url[idx]),
                                                    'counter': (drom_counter[idx])
                                                    }
        what_droms_warms_up_list = get_why_drom_selected_dict(drom_final_dict, todays_wod)
        drom_final_dict = add_why_drom_selected_to_drom_final_dict(drom_final_dict, what_droms_warms_up_list)

        # GYMNASTICS SELECTION
        tough_gymnastics_movements_from_todays_wod = get_which_movements_are_tough_gymnastics_movements(todays_wod)
        tough_gymnastics_warmups = get_gymnastics_warmup(todays_wod)

        gymnastics_final_dict = {}

        for k, v in gymnastics_warmups.items():
            for tough_gymnastics_movement in tough_gymnastics_warmups:
                if tough_gymnastics_movement == k:
                    gymnastics_final_dict[k] = v

        # KB SELECTION
        kb_warmup = {}

        kb_movements_from_todays_wod = get_which_movements_are_kb_movements(todays_wod)
        kb_warmup_movements_list = get_kettlebell_warmup(todays_wod)
        kb_warmup_img_list = get_images_for_display(kb_warmup_movements_list, kb_warmups_dict)
        kb_warmup_url_list = get_url_for_display(kb_warmup_movements_list, kb_warmups_dict)
        kb_warmup_reps_list = get_reps(kb_warmup_movements_list, tough_exercises, kb_warmups_dict)
        for idx, item in enumerate(kb_warmup_movements_list):
            kb_warmup[kb_warmup_movements_list[idx]] = {'img': (kb_warmup_img_list[idx]),
                                                        'url': (kb_warmup_url_list[idx]),
                                                        'reps': (kb_warmup_reps_list[idx]),
                                                        }

        # BARBELL SELECTION
        barbell_warmup = {}

        barbell_movements_from_todays_wod = get_which_movements_are_barbell_movements(todays_wod)
        barbell_warmup_movements_list = get_barbell_warmup_movements(todays_wod)
        barbell_warmup_text_list = get_text_for_display(barbell_warmup_movements_list, barbell_warmups_dict)
        barbell_warmup_img_list = get_images_for_display(barbell_warmup_movements_list, barbell_warmups_dict)
        barbell_warmup_url_list = get_url_for_display(barbell_warmup_movements_list, barbell_warmups_dict)
        barbell_warmup_reps_list = get_reps(barbell_warmup_movements_list, tough_exercises, barbell_warmups_dict)
        for idx, item in enumerate(barbell_warmup_movements_list):
            barbell_warmup[barbell_warmup_movements_list[idx]] = {'img': (barbell_warmup_img_list[idx]),
                                                                  'url': (barbell_warmup_url_list[idx]),
                                                                  'text': (barbell_warmup_text_list[idx]),
                                                                  'reps': (barbell_warmup_reps_list[idx])
                                                                  }
        est_time_for_display = get_est_times_for_display(metcon_warmup, drom_warmup[0], gymnastics_final_dict,
                                                         kb_warmup, barbell_warmup)[0]
        est_time_for_display_plus5 = get_est_times_for_display(metcon_warmup, drom_warmup[0], gymnastics_final_dict,
                                                               kb_warmup, barbell_warmup)[1]

        return render_template('index.html', drom_warmup=drom_warmup, metcon_warmup=metcon_warmup,
                               exercise_keys=exercise_keys,
                               barbell_warmup=barbell_warmup,
                               barbell_movements_from_todays_wod=
                               barbell_movements_from_todays_wod,
                               kb_movements_from_todays_wod=kb_movements_from_todays_wod,
                               kb_warmup=kb_warmup, tough_gymnastics_movements_from_todays_wod=
                               tough_gymnastics_movements_from_todays_wod,
                               easy_exercises=easy_exercises, tough_exercises=tough_exercises,
                               gymnastics_final_dict=gymnastics_final_dict, drom_final_dict=drom_final_dict,
                               todays_wod=todays_wod, est_time_for_display=est_time_for_display,
                               est_time_for_display_plus5=est_time_for_display_plus5,
                               error_message=error_message, warmup_duration_selection=warmup_duration_selection,
                               print_for_debug=print_for_debug
                               )

    else:
        print('else block called$$$$$$$$$$$$$$$$$$$$$$')
        return render_template('index.html', exercise_keys=exercise_keys,
                               warmup_duration_selection=warmup_duration_selection)


if __name__ == '__main__':
    app.run(debug=True)
