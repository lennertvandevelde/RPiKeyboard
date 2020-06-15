# pylint: skip-file
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import threading
from mingus.core import notes, chords
from mingus.containers import Note
from mingus.midi import fluidsynth, pyfluidsynth
from helpers.klasseknop import Button
from RPi import GPIO
import datetime
import json
import LCD
from subprocess import check_output

ir = [26, 19, 13, 6, 5, 22, 27, 17]
btn2 = 12
touch = 4
sw = 21
dt = 20
clk = 16
scale_number = 1
last_scale_number = 1
clkLastState = 1
dtLastState = 1
scale_name= ""
backtrack_number = 0
volume = 75
Noteid = ''
endpoint = '/api/v1'
duration = ''
current_track = 0
may_rotate = True
leadinstr = 1
backinginstr = 1


fs = pyfluidsynth.Synth(gain=2)
fs.start(driver="alsa")
sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)
fs.program_change(2,1)
fs.program_change(1,1)
fs.program_change(3,123)
fs.program_change(9,48)

lcd = LCD.Lcd(E=23, RS= 24, SDA=12, SCL=25)
ips = check_output(['hostname', '--all-ip-addresses']).decode("utf-8")
ip = ips.split(" ")
print(ip[1])

lcd.clear_display()
LockRotary = threading.Lock()

now_date =''
noten = {}
index_note_in_track = 0
now_time = 0
scalenotes = {}
idnoten_in_scale_midi = {}
place_inKey_notename = {}
interval = 1
touch2 = True
old_time = 0
new_time = 0
loop = False
end = 0
start = 1
playing = False



def backtrack():
    print("staaart")
    global volume
    global loop
    global backtrack_number
    global interval
    global backinginstr
    while True:
        while loop:
            if playing:
                if backtrack_number == 1:
                    print("back")
                    while backtrack_number == 1:
                        fs.program_change(2, backinginstr)
                        fs.noteon(2,idnoten_in_scale_midi['idNote1'], round(volume/1.5))
                        time.sleep(interval*3/4)
                        fs.noteoff(2, idnoten_in_scale_midi['idNote1'])
                        time.sleep(interval/4)
                        fs.noteon(2,idnoten_in_scale_midi['idNote2'], round(volume/1.5)) 
                        time.sleep(interval*3/4)
                        fs.noteoff(2, idnoten_in_scale_midi['idNote2'])
                        time.sleep(interval/4)
                        fs.noteon(2,idnoten_in_scale_midi['idNote3'], round(volume/1.5))
                        time.sleep(interval*3/4)
                        fs.noteoff(2, idnoten_in_scale_midi['idNote3'])
                        time.sleep(interval/4)
                        fs.noteon(2,idnoten_in_scale_midi['idNote4'], round(volume/1.5))
                        time.sleep(interval*3/4)
                        fs.noteoff(2, idnoten_in_scale_midi['idNote4'])
                        time.sleep(interval/4)
                if backtrack_number == 2:
                    fs.program_change(2, backinginstr)
                    fs.noteon(2,idnoten_in_scale_midi['idNote1'] - 12, round(volume/2))
                    while backtrack_number == 2:
                        time.sleep(0.5)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote1'] - 12)
                while backtrack_number == 3:
                    fs.program_change(2, backinginstr)
                    fs.noteon(2,idnoten_in_scale_midi['idNote1'], round(volume/1.5))
                    time.sleep(interval*1/3)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote1'])
                    fs.noteon(2,idnoten_in_scale_midi['idNote1'], round(volume/1.5)) 
                    time.sleep(interval*1/3)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote1'])
                    fs.noteon(2,idnoten_in_scale_midi['idNote1'], round(volume/1.5)) 
                    time.sleep(interval*1/3)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote1'])
                    fs.noteon(2,idnoten_in_scale_midi['idNote5'], round(volume/1.5))
                    time.sleep(interval*1)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote5'])
                if backtrack_number == 4:
                    fs.program_change(2, backinginstr)
                    fs.noteon(2,idnoten_in_scale_midi['idNote1'] - 12, round(volume/2))
                    fs.noteon(2,idnoten_in_scale_midi['idNote3'] - 12, round(volume/2))
                    fs.noteon(2,idnoten_in_scale_midi['idNote5'] - 12, round(volume/2))
                    while backtrack_number == 4:
                        time.sleep(0.5)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote1'] - 12)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote3'] - 12)
                    fs.noteoff(2, idnoten_in_scale_midi['idNote5'] - 12)
                if backtrack_number == 0:
                    fs.system_reset()
                    loop = False
                    
                    
                time.sleep(1)






def rotate():
    global clkLastState
    while True:
        if may_rotate:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                clkLastState = clkState
                print("rotate")
                fs.system_reset()
                fs.program_select(0, sfid, 0, 0)
                global backtrack_number
                backtrack_number = 0
                
                global dtLastState
                global scale_number
                
                time.sleep(0.002) 



                if (clkState == 1) and (dtState == 0) : 
                    print("->")
                    if scale_number != 8:
                        scale_number += 1
                        keycheck()
                    else:
                        scale_number = 1
                        keycheck()
                    print(scale_number)

                    while dtState == 0:
                        dtState = GPIO.input(dt)
    
                    while dtState == 1:
                        dtState = GPIO.input(dt)

                elif (clkState == 1) and (dtState == 1): 
                    print("<-")
                    if scale_number != 1:
                        scale_number -= 1
                        keycheck()
                    else:
                        scale_number = 8
                        keycheck()
                    print(scale_number)
                    while clkState == 1:
                        clkState = GPIO.input(clk)


def keycheck():
    global place_inKey_notename
    global last_scale_number
    global idnoten_in_scale_midi
    global scale_number
    global scalenotes
    global leadinstr
    global backinginstr
    last_scale_number = scale_number
    print(scale_number)
    idnoten_in_scale_midi = DataRepository.read_noten_by_keyid(scale_number)
    print(idnoten_in_scale_midi)
    i = -2
    for idnoot in idnoten_in_scale_midi:
        if i == -2:
            scale_name = idnoten_in_scale_midi[idnoot]
            i += 1
        elif i == -1:
            leadinstr = idnoten_in_scale_midi['Leadinst']
            i+= 1
        elif i == 0:
            backinginstr = idnoten_in_scale_midi['Backinst']
            i+= 1
        else:
            place_inKey_notename[i] = DataRepository.read_notename_by_id(idnoten_in_scale_midi[idnoot])['NoteName']
            scalenotes[idnoten_in_scale_midi[idnoot]] = DataRepository.read_notename_by_id(idnoten_in_scale_midi[idnoot])['NoteName']
            i += 1
    socketio.emit('B2F_noten_in_scale', place_inKey_notename)
    print(place_inKey_notename)
    print(scale_name)
    lcd.clear_display()
    lcd.write_message(scale_name)




def setup():
    global now_date
    global scalenotes
    global now_time
    global idnoten_in_scale_midi
    global clkLastState
    print(setup)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in ir:
        GPIO.setup(i, GPIO.IN,GPIO.PUD_UP)
        GPIO.add_event_detect(i,GPIO.FALLING, infra ,bouncetime=200)
    GPIO.setup(touch, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(touch, GPIO.RISING, touched, bouncetime=50)
    GPIO.setup(clk, GPIO.IN)
    clkLastState = GPIO.input(clk)
    GPIO.setup(dt, GPIO.IN)
    GPIO.setup(sw, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(sw, GPIO.FALLING, backtrack_button, bouncetime=400)
    print(pyfluidsynth.api_version)
    now_date = datetime.datetime.now()
    now_date = now_date.strftime("%Y-%m-%d %H:%M:%S")
    now_time = time.time()
    print(now_time)


def backtrack_button(sw):
    if playing:
        global backtrack_number
        global loop
        print("druk")
        
        if backtrack_number != 4:
            backtrack_number += 1
        else:
            backtrack_number = 0
        if backtrack_number == 1:
            loop = True
        print(backtrack_number)

    
    

def touched(touch):
    if playing:
        print("touch")
        global interval
        global old_time
        global new_time
        new_time = time.time()
        if new_time - old_time < 1.5:
            interval = new_time - old_time
        old_time = new_time
        print(interval)
    else:
        lcd.clear_display()
        lcd.write_message((ip[1]))

def infra(i):
    print(playing)
    if playing:
        global start
        global end
        global idNote
        global noten
        global index_note_in_track
        global idnoten_in_scale_midi
        global fs
        global leadinstr
        start = time.time()
        if i == 17:
            idNotenew = 'idNote1'
        elif i == 27:
            idNotenew = 'idNote2'
        elif i == 22:
            idNotenew = 'idNote3'
        elif i == 5:
            idNotenew = 'idNote4'
        elif i == 6:
            idNotenew = 'idNote5'
        elif i == 13:
            idNotenew = 'idNote6'
        elif i == 19:
            idNotenew = 'idNote7'
        elif i == 26:
            idNotenew = 'idNote8'
        if start - end > 0.1 or idNotenew != idNote:
            
            dur = round(start-end, 2)
            index_note_in_track += 1
            noten[f"{index_note_in_track}"] = dict(noteduration = dur, idNotes = 1)
            idNote = idNotenew

            print("pressed")
            start = time.time()
            fs.program_change(1,leadinstr)
            fs.noteon(1,idnoten_in_scale_midi[idNote], volume)
            socketio.emit('B2F_note_on', {'Noot': scalenotes[idnoten_in_scale_midi[idNote]]})
            bol = True
            while bol:
                time.sleep(0.1)
                if  GPIO.input(i) == GPIO.HIGH:
                    bol = False
            fs.noteoff(1,idnoten_in_scale_midi[idNote])
            end = time.time()
            dur = round(end-start, 2)
            print(dur)
            index_note_in_track += 1
            print(dur)
            if dur>0.1:
                noten[f"{index_note_in_track}"] = dict(noteduration = dur, idNotes = idnoten_in_scale_midi[idNote])
            print(noten)
            socketio.emit('B2F_note_off')
        



def knop2(btn2):
    print("pressed2")
    global now_time
    global now_date
    global noten
    for notje in noten:
        print(noten[notje]["noteduration"])
    if len(noten)>0:
        new_now_time = time.time()
        sesId = DataRepository.add_new_playsession(new_now_time-now_time, now, 1, f'00:00:0{round(interval)}', noten)
    noten = {}
    now_date = datetime.datetime.now()
    now_date = now_date.strftime("%Y-%m-%d %H:%M:%S")
    now_time = time.time()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."
@app.route(endpoint +'/tracks', methods=['GET'])
def show_saved():
    print("a")
    global playing
    playing = False
    print(json.dumps(DataRepository.get_all_tracks(), default=str))
    return json.dumps(DataRepository.get_all_tracks(), default=str), 200
@app.route(endpoint + '/tracks/remove/<sessionId>', methods=['DELETE'])
def delete(sessionId):
    print(sessionId)
    data = DataRepository.delete_track(sessionId)
    print(data)
    if data > 0:
        return jsonify(status="success", row_count=data), 201
    else:
        return jsonify(status="no update", row_count=data), 201
# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    global current_track
    current_track = DataRepository.get_current_track_id()['curtra']
    print(current_track)

@socketio.on('F2B_play_test')
def play_test():
    print("ontvangen")
    vel2 = 100
    vel1 = 50
    vel3 = 70
    base = 1.2
    fs.program_change(2, 42)
    fs.program_change(3, 42)
    fs.noteon(2, Note('G-3'), vel2)
    time.sleep(base)
    fs.noteoff(2,Note('G-3'))
    fs.noteon(2,Note('C-3'), vel2)
    time.sleep(base)
    fs.noteoff(2,Note('C-3'))
    fs.noteon(2,Note('Eb-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('Eb-3'))
    fs.noteon(2,Note('F-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('F-3'))
    fs.noteon(2,Note('G-3'), vel2)
    time.sleep(base*2/3)
    fs.noteoff(2,Note('G-3'))
    fs.noteon(2,Note('C-3'), vel2)
    time.sleep(base*2/3)
    fs.noteoff(2,Note('C-3'))
    fs.noteon(2,Note('Eb-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('Eb-3'))
    fs.noteon(2,Note('F-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('F-3'))
    fs.noteon(2,Note('D-3'), vel2)
    time.sleep(base*2+base*2/3)
    fs.noteoff(2,Note('D-3'))
    time.sleep(base/3)
    fs.noteon(2,Note('F-3'), vel2)
    time.sleep(base)
    fs.noteoff(2,Note('F-3'))
    fs.noteon(2,Note('Bb-2'), vel2)
    time.sleep(base)
    fs.noteoff(2,Note('Bb-2'))
    fs.noteon(2,Note('Eb-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('Eb-3'))
    fs.noteon(2,Note('D-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('D-3'))
    fs.noteon(2,Note('F-3'), vel2)
    time.sleep(base*2/3)
    fs.noteoff(2,Note('F-3'))
    fs.noteon(2,Note('Bb-2'), vel2)
    time.sleep(base)
    fs.noteoff(2,Note('Bb-2'))
    fs.noteon(2,Note('Eb-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('Eb-3'))
    fs.noteon(2,Note('D-3'), vel2)
    time.sleep(base/6)
    fs.noteoff(2,Note('D-3'))
    fs.noteon(2,Note('C-3'), vel2)
    time.sleep(base*3)
    fs.noteoff(2,Note('C-3'))



    # while True:
    #     fs.noteon(2, 48, 60)
    #     fs.noteon(2,52,60)
    #     time.sleep(1)
    #     fs.noteoff(2,52)
    #     time.sleep(1)
    #     print(GPIO.input(ir1))

    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    # status = DataRepository.read_status_lampen()
    # socketio.emit('B2F_status_lampen', {'lampen': status})
@socketio.on('F2BCheck')
def check():
    return 0
@socketio.on('F2B_volume_changed')
def change_volume(pvolume):
    global volume
    volume = int(pvolume['volume'])
    print(volume)

@socketio.on("F2B_start")
def start():
    global playing
    global end
    global may_rotate
    print("play")
    may_rotate = False
    playing = True
    end = time.time()

@socketio.on("F2B_pause")
def pause():
    global playing
    playing = False
@socketio.on("F2B_stop")
def stop():
    global playing
    global noten
    global may_rotate
    global backtrack_number
    backtrack_number = 0
    may_rotate = True
    playing = False
    noten = {}
    print(noten)
@socketio.on("F2B_save")
def save(json):
    print("pressed2")
    global now_time
    global now_date
    global noten
    for notje in noten:
        print(noten[notje]["noteduration"])
    if len(noten)>0:
        new_now_time = time.time()
        now_date = datetime.datetime.now()
        now_date = now_date.strftime("%Y-%m-%d %H:%M:%S")
        print(json)
        sesId = DataRepository.add_new_playsession(json['trackName'], duration, now_date, scale_number, interval, noten)
    noten = {}

@socketio.on("F2B_duration")
def durationf(json):
    global duration
    duration = json['duration']
    print(duration)
@socketio.on("F2B_play_track")
def playtrack(json):
    print("AA")
    print(json['track'])
    global leadinstr
    leadinstr = DataRepository.get_lead_by_id(json['track'])['Leadinst']
    result = DataRepository.get_played_notes(json['track'])
    fs.program_change(1, leadinstr)
    for noot in result:
        if noot != 1:
            fs.noteon(1, noot['idNotes'], 100)
            time.sleep(noot['noteduration'])
            fs.noteoff(1, noot['idNotes'])
        else:
            time.sleep(noot['noteduration'])

@socketio.on('F2B_play')
def play():
    global playing
    global idnoten_in_scale_midi
    global place_inKey_notename
    global scale_name
    global current_track
    global may_rotate
    may_rotate = True
    idnoten_in_scale_midi = DataRepository.read_noten_by_keyid(scale_number)
    print(idnoten_in_scale_midi)
    i = -2
    for idnoot in idnoten_in_scale_midi:
        if i == -2:
            scale_name = idnoten_in_scale_midi[idnoot]
            i += 1
        elif i == -1:
            leadinstr = idnoten_in_scale_midi['Leadinst']
            i+= 1
        elif i == 0:
            backinginstr = idnoten_in_scale_midi['Backinst']
            i+= 1
        else:
            place_inKey_notename[i] = DataRepository.read_notename_by_id(idnoten_in_scale_midi[idnoot])['NoteName']
            scalenotes[idnoten_in_scale_midi[idnoot]] = DataRepository.read_notename_by_id(idnoten_in_scale_midi[idnoot])['NoteName']
            i  += 1
    
    socketio.emit('B2F_noten_in_scale1', place_inKey_notename)
    socketio.emit('B2F_current_track', {'current': current_track}, broadcast=False)
    print(place_inKey_notename)
    print(scale_name)
@socketio.on('F2B_saved')
def saved():
    global playing
    playing = False
@socketio.on('F2B_saving')
def saving():
    global playing
    playing = False
    btt = round(1/interval, 2)
    socketio.emit("B2F_track_info", {'key': scale_name, 'btt': btt, 'time': duration})
    socketio.emit('B2F_current_track', {'current': current_track})
    


setup()

backthread = threading.Thread(target = backtrack, daemon=True)
backthread.start()
rotatethread = threading.Thread(target= rotate, daemon=True)
rotatethread.start()


if __name__ == '__main__':
    print("start")
    socketio.run(app, debug=False, host='0.0.0.0')
    print("start")

