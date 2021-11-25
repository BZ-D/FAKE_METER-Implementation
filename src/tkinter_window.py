import tkinter.messagebox
from tkinter import *
import tkinter.filedialog as tkFD
from tkinter import ttk
import subprocess
import socket
import requests

# -------------- global variables ---------------

has_appium = False
has_devices = False

api_key = ''
secret_key = ''
access_token = ''
app_name = ''
script_path = ''
base_apk_path = ''
updated_apk_path = ''
base_platform_ver = ''
updated_platform_ver = ''
app_package = ''
app_activity = ''
timer = 0
counter = 0


# -------------------- Functions ---------------------

def check_port_in_use(port, host='127.0.0.1'):
    # check whether a certain port is occupied

    # log
    print('Checking port usage: ' + str(port) + '...')

    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()


def get_appium_state():
    # check whether the port 4723 (default port of Appium) is occupied

    # log
    print('Getting Appium state...')

    APPIUM_DEFAULT_PORT = 4723
    global has_appium
    has_appium = check_port_in_use(APPIUM_DEFAULT_PORT)
    dialog_appium_state()


def dialog_appium_state():
    if has_appium:
        print('Appium active!')
        tkinter.messagebox.showinfo('Appium 状态', 'Appium 已启动！')
    else:
        print('No Appium Server detected!')
        tkinter.messagebox.showinfo('Appium 状态', 'Appium 未启动！')


def check_android_device():
    # check android device connection
    global has_devices

    # log
    print('Checking devices state...')

    out = subprocess.Popen('adb devices',
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8'
                           )
    if 'emulator' in out.communicate()[0]:
        # log
        print('Android Devices detected!')

        has_devices = True
    else:
        # log
        print('No Android Devices detected!')

        has_devices = False

    dialog_device_state()


def dialog_device_state():
    if has_devices:
        tkinter.messagebox.showinfo('Android Devices 状态', 'Android 设备已连接！')
    else:
        tkinter.messagebox.showinfo('Android Devices 状态', '未找到连接的 Android 设备！')


def get_api_key():
    global api_key

    # log
    print('Getting api key...')

    api_key = api_key_input.get()
    return api_key


def get_secret_key():
    global secret_key

    # log
    print('Getting secret key...')

    secret_key = secret_key_input.get()
    return secret_key


def get_access_token():
    # ※ important: get OCR access token of Baidu OCR API
    # should provide api key as well as secret key to get access token
    # if successfully get the token, print it
    # else hint an error happens

    global access_token
    get_api_key()
    get_secret_key()
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'
    host = host + '&client_id=' + api_key
    host = host + '&client_secret=' + secret_key

    # log
    print('Getting access token...')

    response = requests.get(host)

    if response:
        # log
        print('Getting an access token success!')

        access_token = response.json()['access_token']
        print(access_token)
        token_result_hint.config(state='normal')
        token_result_hint.delete(0, "end")
        token_result_hint.insert(0, '获取成功！令牌为: ' + access_token)
        token_result_hint.config(state='readonly')
    else:
        # log
        print('Getting an access token failure!')

        token_result_hint.config(state='normal')
        token_result_hint.delete(0, "end")
        token_result_hint.insert(0, '获取失败！请检查您的 API Key 及 Secret Key.')
        token_result_hint.config(state='readonly')


def get_app_name():
    # get a field

    # log
    print('Getting app name...')

    global app_name
    app_name = app_name_input.get()
    return app_name


def get_script_path():
    # get a field

    # log
    print('Getting script path...')

    global script_path
    script_path = tkFD.askopenfilename()
    script_path_input.config(state='normal')
    script_path_input.delete(0, "end")
    script_path_input.insert(0, script_path)
    script_path_input.config(state='readonly')
    return script_path


def get_base_apk_path():
    # get a field

    # log
    print('Getting base apk size...')

    global base_apk_path
    base_apk_path = tkFD.askopenfilename()
    base_input.config(state='normal')
    base_input.delete(0, "end")
    base_input.insert(0, base_apk_path)
    base_input.config(state='readonly')
    return base_apk_path


def get_updated_apk_path():
    # get a field

    # log
    print('Getting updated apk size...')

    global updated_apk_path
    updated_apk_path = tkFD.askopenfilename()
    updated_input.config(state='normal')
    updated_input.delete(0, "end")
    updated_input.insert(0, updated_apk_path)
    updated_input.config(state='readonly')
    return updated_apk_path


def get_base_platform_ver():
    # get a field

    # log
    print('Getting base platform version...')

    global base_platform_ver
    base_platform_ver = base_platform_choose.get()
    return base_platform_ver


def get_updated_platform_ver():
    # get a field

    # log
    print('Getting updated platform version...')

    global updated_platform_ver
    updated_platform_ver = updated_platform_choose.get()
    return updated_platform_ver


def get_app_package():
    # get a field

    # log
    print('Getting app package...')

    global app_package
    app_package = app_package_input.get()
    return app_package


def get_app_activity():
    # get a field

    # log
    print('Getting app activity...')

    global app_activity
    app_activity = app_activity_input.get()
    return app_activity


def run():
    # what to do after press on the "run" button

    global app_name
    global app_package
    global app_activity
    global base_platform_ver
    global updated_platform_ver
    app_name = get_app_name()
    app_package = get_app_package()
    app_activity = get_app_activity()
    base_platform_ver = get_base_platform_ver()
    updated_platform_ver = get_updated_platform_ver()

    prepare_works_done = [
        has_appium,
        has_devices,
        len(api_key) > 0,
        len(secret_key) > 0,
        len(access_token) > 0,
        len(app_name) > 0,
        len(script_path) > 0,
        len(base_apk_path) > 0,
        len(updated_apk_path) > 0,
        len(base_platform_ver) > 0,
        len(updated_platform_ver) > 0,
        len(app_package) > 0,
        len(app_activity) > 0
    ]

    for i in range(len(prepare_works_done)):
        if not prepare_works_done[i]:
            print('The missing item index: ' + str(i))
            tkinter.messagebox.showinfo('无法运行', '请完善所有信息后再运行！')
            return

    prohibit_run_again()
    counting()
    timing()


def timing():
    # used as a timer to record running time
    global timer
    timer += 1
    running_timer.config(text=str(timer))
    print('Fake METER has run for ' + str(timer) + ' seconds.')
    running_timer.after(1000, timing)


def counting():
    # simulate the process counter
    global counter
    if counter == 0:
        hint_text.set('运行中')
        counter += 1
    elif counter == 1:
        hint_text.set('运行中 =')
        counter += 1
    elif counter == 2:
        hint_text.set('运行中 ==')
        counter += 1
    elif counter == 3:
        hint_text.set('运行中 ===')
        counter = 0

    running_hint.after(1000, counting)


def start():
    # start of window
    global window
    window.mainloop()


def prohibit_run_again():
    # avoid press on the "run" button for more than one time
    run_btn.config(state=DISABLED)


# ------------ TkInter Window Area -------------

window = Tk()

# title of window
window.title('METER-Play')
# size of window 'width x height'
window.geometry('600x800')
# avoid change window size
window.resizable(0, 0)

# banner
banner = Label(window,
               text='FAKE-METER-Implementation Play',
               bg='#2C9AE9',
               fg='#FEFEFE',
               font=('Arial', 12),
               width=15,
               height=2
               )
banner.pack(fill=X)

# frame
body = Frame(window)
body.pack(side=LEFT,
          anchor=W,
          fill=BOTH,
          expand=YES)

# check Appium hint
check_appium_hint = Label(body,
                          text='1. 检查 Appium 运行状态',
                          font=('Arial', 10),
                          width=25,
                          height=2,
                          anchor=W)
check_appium_hint.place(x=40, y=40)

# check Appium button
check_appium_btn = Button(body,
                          text='检查',
                          width=10,
                          command=get_appium_state
                          )
check_appium_btn.place(x=250, y=40)

# check Android device hint
check_device_hint = Label(body,
                          text='2. 检查 Android 设备状态',
                          font=('Arial', 10),
                          width=25,
                          height=2,
                          anchor=W)
check_device_hint.place(x=40, y=80)

# check Android device button
check_device_btn = Button(body,
                          text='检查',
                          width=10,
                          command=check_android_device
                          )
check_device_btn.place(x=250, y=80)

# get Baidu OCR Access Token hint
ocr_token_hint = Label(body,
                       text='3. 获取百度 OCR 访问令牌',
                       font=('Arial', 10),
                       width=25,
                       height=2,
                       anchor=W)
ocr_token_hint.place(x=40, y=120)

# input API Key hint
api_key_hint = Label(body,
                     text='API Key: ',
                     font=('Arial', 10),
                     width=25,
                     height=2,
                     anchor=W)
api_key_hint.place(x=40, y=160)

# input API Key text field
api_key_input = Entry(body,
                      font=('Arial', 10),
                      width=40,
                      justify='center'
                      )
api_key_input.place(x=150, y=167)

# input Secret Key hint
secret_key_hint = Label(body,
                        text='Secret Key: ',
                        font=('Arial', 10),
                        width=25,
                        height=2,
                        anchor=W)
secret_key_hint.place(x=40, y=200)

# input API Key text field
secret_key_input = Entry(body,
                         font=('Arial', 10),
                         width=40,
                         justify='center'
                         )
secret_key_input.place(x=150, y=207)

# get Access Token button
get_token_btn = Button(body,
                       text='获取',
                       width=10,
                       command=get_access_token
                       )
get_token_btn.place(x=250, y=240)

# result of getting ocr access token
token_result_hint = Entry(body,
                          text='',
                          font=('Arial', 10),
                          state='readonly',
                          width=60
                          )
token_result_hint.place(x=30, y=280)

# input APP name hint
app_name_hint = Label(body,
                      text='4. APP 名称: ',
                      font=('Arial', 10),
                      width=25,
                      height=2,
                      anchor=W)
app_name_hint.place(x=40, y=320)

# input APP name field
app_name_input = Entry(body,
                       font=('Arial', 10),
                       width=40,
                       justify='center'
                       )
app_name_input.place(x=150, y=327)

# input test script path hint
script_path_hint = Label(body,
                         text='5. 测试脚本路径: ',
                         font=('Arial', 10),
                         width=25,
                         height=2,
                         anchor=W)
script_path_hint.place(x=40, y=360)

# input test script path field
script_path_input = Entry(body,
                          font=('Arial', 10),
                          width=30,
                          state='readonly',
                          justify='center'
                          )
script_path_input.place(x=180, y=367)

# input test script path choose
script_path_choose = Button(body,
                            text='选择',
                            width=10,
                            command=get_script_path)
script_path_choose.place(x=480, y=360)

# base version apk path hint
base_hint = Label(body,
                  text='6. 基准版本 APK 路径: ',
                  font=('Arial', 10),
                  width=25,
                  height=2,
                  anchor=W)
base_hint.place(x=40, y=400)

# base version apk path field
base_input = Entry(body,
                   font=('Arial', 10),
                   width=25,
                   state='readonly',
                   justify='center'
                   )
base_input.place(x=230, y=407)

# base version apk path choose
base_choose = Button(body,
                     text='选择',
                     width=10,
                     command=get_base_apk_path)
base_choose.place(x=480, y=400)

# updated version apk path hint
updated_hint = Label(body,
                     text='7. 升级版本 APK 路径: ',
                     font=('Arial', 10),
                     width=25,
                     height=2,
                     anchor=W)
updated_hint.place(x=40, y=440)

# updated version apk path field
updated_input = Entry(body,
                      font=('Arial', 10),
                      width=25,
                      state='readonly',
                      justify='center'
                      )
updated_input.place(x=230, y=447)

# updated version apk path choose
updated_choose = Button(body,
                        text='选择',
                        width=10,
                        command=get_updated_apk_path)
updated_choose.place(x=480, y=440)

# base platform version hint
base_platform_hint = Label(body,
                           text='8. 基准平台版本: ',
                           font=('Arial', 10),
                           width=25,
                           height=2,
                           anchor=W)
base_platform_hint.place(x=40, y=480)

# base platform version choose
base_platform_choose = ttk.Combobox(body, width=5, state='readonly')
base_platform_choose['value'] = ('7.0', '8.0', '9.0', '10.0', '11.0')
base_platform_choose.place(x=180, y=487)

# updated platform version hint
updated_platform_hint = Label(body,
                              text='9. 升级平台版本: ',
                              font=('Arial', 10),
                              width=25,
                              height=2,
                              anchor=W)
updated_platform_hint.place(x=40, y=520)

# updated platform version choose
updated_platform_choose = ttk.Combobox(body, width=5, state='readonly')
updated_platform_choose['value'] = ('7.0', '8.0', '9.0', '10.0', '11.0')
updated_platform_choose.place(x=180, y=527)

# input App_Package hint
app_package_hint = Label(body,
                         text='10. App Package: ',
                         font=('Arial', 10),
                         width=25,
                         height=2,
                         anchor=W)
app_package_hint.place(x=40, y=560)

# input APP package field
app_package_input = Entry(body,
                          font=('Arial', 10),
                          width=40,
                          justify='center'
                          )
app_package_input.place(x=180, y=567)

# input App_Activity hint
app_activity_hint = Label(body,
                          text='11. App Activity: ',
                          font=('Arial', 10),
                          width=25,
                          height=2,
                          anchor=W)
app_activity_hint.place(x=40, y=600)

# input APP Activity field
app_activity_input = Entry(body,
                           font=('Arial', 10),
                           width=40,
                           justify='center'
                           )
app_activity_input.place(x=180, y=607)

# run METER button
run_btn = Button(body,
                       text='运行',
                       width=10,
                       command=run
                       )
run_btn.place(x=250, y=650)

# running hint
hint_text = StringVar('')
running_hint = Label(body,
                     textvariable=hint_text,
                     width=10,
                     font=('Arial', 10),
                     anchor=W
                     )
running_hint.place(x=180, y=710)

# running timer
running_timer = Label(body,
                      text='',
                      width=10,
                      font=('Arial', 10)
                      )
running_timer.place(x=300, y=710)

start()
