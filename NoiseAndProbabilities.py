# psychometric.py
from __future__ import division
import pandas as pd
from psychopy import core, event, visual, logging, gui, data, sound
import os
import pickle
from datetime import datetime
import array

# That volume does not work, maybe due to the audiodevice library

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store subject info / create GUI
expName = 'NoiseAndProbabilities'
myDlg = gui.Dlg(title="Auditory experiment")
myDlg.addField('Participant:')
myDlg.addField('Age:', 21)
myDlg.addField('Sex:', choices=('female', 'male', 'non-binary'))
myDlg.addField('Condition', choices=('1', '2', '3', '4'))
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    print(ok_data)
else:
    print('user cancelled')

# store values from dialog
expInfo = {
    'Participant': ok_data[0],
    'Age': ok_data[1],
    'Sex': ok_data[2],
    'Condition': ok_data[3]
}

expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName  # you may want to use later for other info

# Save Files
if not os.path.isdir('data'):
    os.makedirs('data')  # if this fails (e.g. permissions) we will get error
filename = 'data' + os.path.sep + '%s_%s' % (expInfo['Participant'],
                                             expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # output to console, not to file


# Here the experiment starts


def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("DEBUG: Clear Screen")


def experiment_update(filename):
    '''
    Create the user update experimence, interface.
    '''

    # Import KA tones
    sndKaPlus8 = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNRplus14.wav', sampleRate=44100, stereo=True)
    sndKaPlus4 = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNRplus10.wav', sampleRate=44100, stereo=True)
    sndKa = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNR0.wav', sampleRate=44100, stereo=True)
    sndKaMinus4 = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNRminus10.wav', sampleRate=44100, stereo=True)
    sndKaMinus8 = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNRminus16.wav', sampleRate=44100, stereo=True)
    sndKaMinus10 = sound.backend_sounddevice.SoundDeviceSound(
        'KaNorm300_SNRminus20.wav', sampleRate=44100, stereo=True)

    # Import TO tones
    sndToPlus8 = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNRplus14.wav', sampleRate=44100, stereo=True)
    sndToPlus4 = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNRplus10.wav', sampleRate=44100, stereo=True)
    sndTo = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNR0.wav', sampleRate=44100, stereo=True)
    sndToMinus4 = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNRminus10.wav', sampleRate=44100, stereo=True)
    sndToMinus8 = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNRminus16.wav', sampleRate=44100, stereo=True)
    sndToMinus10 = sound.backend_sounddevice.SoundDeviceSound(
        'ToNorm300_SNRminus20.wav', sampleRate=44100, stereo=True)

    # Create some text stimuli
    begin_text = 'LEERTASTE DRÜCKEN UM ZU BEGINNEN'
    tone_text = " + "
    text_AB = " KA oder TO? "

    # set up timer durations
    initial_wait = 0.05
    pre_observation = 0.5

    # Trial number / order / counters:

    # Import csv file (now with relative path)
    path = os.path.join(_thisDir, "SeqForPython.csv")
    with open(path) as f:
        df = pd.read_csv(f)

    # If Condition == '1', import different sequences etc.
    if expInfo['Condition'] == '1':
        order = array.array('i', df["seqCond1"])
        intensities = array.array('i', df["intensityCond1"])
        print("Condition 1")
    elif expInfo['Condition'] == '2':
        order = array.array('i', df["seqCond2"])
        intensities = array.array('i', df["intensityCond2"])
        print("Condition 2")
    elif expInfo['Condition'] == '3':
        order = array.array('i', df["seqCond3"])
        intensities = array.array('i', df["intensityCond3"])
        print("Condition 3")
    elif expInfo['Condition'] == '4':
        order = array.array('i', df["seqCond4"])
        intensities = array.array('i', df["intensityCond4"])
        print("Condition 4")

    # Intensities: The closer to one, the more signal
    orderMetric = intensities

    print("DEBUG: orderMetric")
    print(orderMetric)

    no_trials = len(order)
    print(order)

    # Set the screen / visual stuff
    win0 = visual.Window([800, 600], screen=0, monitor='testMonitor',
                         color=(1, 1, 1), fullscr=True, units='pix',
                         allowGUI=True)

    text_stim = visual.TextStim(win0, text=" ", font='Arial', pos=(0, 0),
                                color=(-1, -1, -1), units='pix', height=72)

    # win0.flip()

    text_stim.setText(begin_text)
    text_stim.setHeight(24)
    text_stim.draw()
    win0.flip()

    key = event.waitKeys(keyList=['space'], clearEvents=True)

    # Main experimental loop
    for i in range(0, no_trials):
        # Read the experimental file
        current_exp_data = pd.read_csv(filename + '.csv')
        updated_subID = str(current_exp_data.iloc[-1]['subject'])
        updated_condition = str(current_exp_data.iloc[-1]['condition'])
        updated_sex = str(current_exp_data.iloc[-1]['sex'])
        updated_age = str(current_exp_data.iloc[-1]['age'])
        updated_exp_date = datetime.today().strftime('%y%m%d')
        updated_orderMetricIndex = int(current_exp_data.iloc[-1]['intensity'])

        # Initialize some info
        current_exp_trial = int(current_exp_data.iloc[-1]['trial'])
        current_correctCounter = int(current_exp_data.iloc[-1]['counter'])
        # Update some info
        updated_exp_trial = current_exp_trial + 1
        updated_exp_time = datetime.today().strftime('%H%M%S')

        # Get the index of the direction array
        orderIndex = order[i]
        update_orderIndex = orderIndex

        # Intensity 
        orderMetricIndex = orderMetric[i]
        updated_orderMetricIndex = orderMetricIndex
        print("DEBUG updated_orderMetricIndex")
        print(updated_orderMetricIndex)

        text_stim.setText(" ")  # clear window
        text_stim.draw()  # draw stimulus text onto the window
        win0.flip()

        exp_time = core.getTime()
        current_time = core.getTime() - exp_time

        # Initial wait
        while current_time < initial_wait:
            current_time = core.getTime() - exp_time
            print("DEBUG: Initial Wait")
            core.wait(0.05)

        exp_time = core.getTime()
        current_time = core.getTime() - exp_time

        # Pre Observation
        while current_time < pre_observation:
            current_time = core.getTime() - exp_time
            # print("DEBUG: Pre Observation Time")

        text_stim.setText(tone_text)
        text_stim.setHeight(72)
        text_stim.draw()
        win0.flip()
        pre_timer = core.getTime()  # In order to get stim duration
        pre_rt = core.getTime()  # Maybe you can place elsewhere (on/offset?)
        dev = 1.5  # Devider, so subjects can answer during stimulus pres.

        # Here we actually play the sound / closer to zero - more signal
        # Order index == 0 = Ka /// Order index == 1 = To
        # Devide core.getDuration by 1.5 for early responses (dk if good)
        if orderIndex == 0:
            if orderMetricIndex == -6:
                sndKaMinus10.play()
                core.wait(sndKaMinus10.getDuration()/dev)
            elif orderMetricIndex == -5:
                sndKaMinus8.play()
                core.wait(sndKaMinus8.getDuration()/dev)
            elif orderMetricIndex == -4:
                sndKaMinus4.play()
                core.wait(sndKaMinus4.getDuration()/dev)
            elif orderMetricIndex == -3:
                sndKa.play()
                core.wait(sndKa.getDuration()/dev)
            elif orderMetricIndex == -2:
                sndKaPlus4.play()
                core.wait(sndKaPlus4.getDuration()/dev)
            elif orderMetricIndex == -1:
                sndKaPlus8.play()
                core.wait(sndKaPlus8.getDuration()/dev)
        elif orderIndex == 1:
            if orderMetricIndex == 6:
                sndToMinus10.play()
                core.wait(sndToMinus10.getDuration()/dev)
            elif orderMetricIndex == 5:
                sndToMinus8.play()
                core.wait(sndToMinus8.getDuration()/dev)
            elif orderMetricIndex == 4:
                sndToMinus4.play()
                core.wait(sndToMinus4.getDuration()/dev)
            elif orderMetricIndex == 3:
                sndTo.play()
                core.wait(sndTo.getDuration()/dev)
            elif orderMetricIndex == 2:
                sndToPlus4.play()
                core.wait(sndToPlus4.getDuration()/dev)
            elif orderMetricIndex == 1:
                sndToPlus8.play()
                core.wait(sndToPlus8.getDuration()/dev)

        text_stim.setText(text_AB)
        text_stim.draw()
        win0.flip()
        d_timer = core.getTime() - pre_timer
        print('DEBUG: TimeDiff: %3.5f' % (d_timer))
        # Response - Event
        key = event.waitKeys(keyList=['q', 'f', 'j'], clearEvents=True)
        if 'f' in key:
            if orderIndex == 0:  # Stim was Ka & sub said Ka
                print('DEBUG: Subject correct')
                updated_correct = 1  # Correct or not
                updated_correctCounter = current_correctCounter + 1

            elif orderIndex == 1:  # Stim was To & sub said Ka
                print('DEBUG: Subject incorrect')
                updated_correct = 0
                updated_correctCounter = 0

            text_stim.setText(" ")
            text_stim.draw()
            win0.flip()

            print("DEBUG: Stimulus A is pressed")
            print("DEBUG: Trial Number: %d" % (i))
            updated_response = 0
            i += 1

        if 'j' in key:
            if orderIndex == 1:  # Stim was To & sub said To
                print('DEBUG: Subject correct')
                updated_correct = 1
                updated_correctCounter = current_correctCounter + 1

            elif orderIndex == 0:  # Stim was Ka & sub said To
                print('DEBUG: Subject incorrect')
                updated_correct = 0
                updated_correctCounter = 0

            text_stim.setText(" ")
            text_stim.draw()
            win0.flip()

            print("DEBUG: Stimulus B is pressed")
            print("DEBUG: Trial Number: %d" % (i))
            updated_response = 1
            i += 1

        if 'q' in key:
            break

        rt = core.getTime() - pre_rt  # Get RT (stimulus onset - response)

        updated_output = pd.DataFrame({'subject': [updated_subID],
                                       'sex': [updated_sex],
                                       'age': [updated_age],
                                       'date': [updated_exp_date],
                                       'time': [updated_exp_time],
                                       'condition': [updated_condition],
                                       'reactiontime': [rt],
                                       'trial': [updated_exp_trial],
                                       'intensity': [updated_orderMetricIndex],
                                       'AorB': [update_orderIndex],
                                       'response': [updated_response],
                                       'correct': [updated_correct],
                                       'counter': [updated_correctCounter]})
        with open(filename + '.csv', 'a') as f:  # try without .csv ???
            updated_output.to_csv(f, mode='a', index=False, header=False)
        f.close()
    win0.close


# Write the whole stuff to the csv file
def experiment_file():

    # Get current time
    exp_date = str(datetime.today().strftime('%y%m%d'))
    exp_time = datetime.today().strftime('%H%M%S')

    exp_data = pd.DataFrame({'subject': expInfo['Participant'],
                             'sex': expInfo['Sex'],
                             'age': expInfo['Age'],
                             'date': [exp_date],
                             'time': [exp_time],
                             'condition': expInfo['Condition'],
                             'reactiontime': [-1],
                             'trial': [-1],
                             'intensity': [-1],
                             'AorB': [-1],
                             'response': [1],
                             'correct': [0],
                             'counter': [0]})

    try:
        # Save CSV file
        exp_data.to_csv(filename + ".csv", index=False)
        # Save pickle
        with open(filename + ".pkl", 'wb') as f:
            pickle.dump(exp_data, f, pickle.HIGHEST_PROTOCOL)
            print("DEBUG: Files saved")
        return filename
    except:
        print("DEBUG: Problem saving files")


if __name__ == '__main__':
    clear_output()
    filename = experiment_file()
    experiment_update(filename)
