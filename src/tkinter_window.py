import tkinter.messagebox
from tkinter import *
import tkinter.filedialog as tkFD
from tkinter import ttk
import subprocess
import socket


has_appium = False
has_devices = False
has_access_token = False
has_app_name = False
has_script_path = False
has_base_apk_path = False
has_updated_apk_path = False
has_base_platform_ver = False
has_updated_platform_ver = False
has_app_package = False
has_app_activity = False

PREPARE_WORKS_DONE = [
    has_appium,
    has_devices,
    has_access_token,
    has_app_name,
    has_script_path,
    has_base_apk_path,
    has_updated_apk_path,
    has_base_platform_ver,
    has_updated_platform_ver,
    has_app_package,
    has_app_activity
]


def check_port_in_use(port, host='127.0.0.1'):
    # check whether a certain port is occupied
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
    APPIUM_DEFAULT_PORT = 4723
    global has_appium
    has_appium = check_port_in_use(APPIUM_DEFAULT_PORT)
    return has_appium


def dialog_appium_state():
    if has_appium:
        tkinter.messagebox.showinfo('Appium 状态', 'Appium 已启动！')
    else:
        tkinter.messagebox.showinfo('Appium 状态', 'Appium 未启动！')


def check_android_device():
    # check android device connection
    global has_devices
    out = subprocess.Popen('adb devices',
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8'
                           )
    if 'emulator' in out.communicate()[0]:
        has_devices = True
        return True

    return False


def dialog_device_state():
    if has_devices:
        tkinter.messagebox.showinfo('Android Devices 状态', 'Android 设备已连接！')
    else:
        tkinter.messagebox.showinfo('Android Devices 状态', '未找到连接的 Android 设备！')


def get_meter_window():
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
                              command=dialog_appium_state
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
                              command=dialog_device_state
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
                           width=10)
    get_token_btn.place(x=250, y=240)

    # result of getting ocr access token
    # fail
    token_fail_hint = Label(body,
                            text='获取失败，错误码：',
                            font=('Arial', 10),
                            width=25,
                            height=2,
                            anchor=W)
    token_fail_hint.place(x=200, y=280)

    # success
    secret_key_hint = Label(body,
                            text='Access Token: ',
                            font=('Arial', 10),
                            width=25,
                            height=2,
                            anchor=W)
    # secret_key_hint.place(x=200, y=280)

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
                                command=tkFD.askopenfilename)
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
                         command=tkFD.askopenfilename)
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
                            command=tkFD.askopenfilename)
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
    get_token_btn = Button(body,
                           text='运行',
                           width=10)
    get_token_btn.place(x=250, y=680)

    return window


if __name__ == '__main__':
    m_window = get_meter_window()
    m_window.mainloop()

