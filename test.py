import customtkinter
import os, sys
from customtkinter import filedialog as fd
from configparser import ConfigParser
import shutil
from win32com.client import Dispatch
from CTkScrollableDropdown import *
import threading
import pythoncom

Settings = ConfigParser()
AccountList = ConfigParser()
Backup = ConfigParser()
Settings.read('settings.ini')
AccountList.read('accounts.ini')
if os.path.isfile('./backup/accounts.ini'):
    Backup.read('./backup/accounts.ini')
if not os.path.exists('./backup'):
    os.makedirs('./backup')    

regions = [
    'EU',
    'NA',
    'Asia',
    'TW/HK/MO',
]
acc = []
korepi = []

instructions = '1) Click on the "Import Accounts" button to import accounts\nAPP WILL CLOSE AFTER SELECTING INJECTOR/IMPORTING ACCOUNTS\n\n2)Choose your region and account\n3)Click on launch\n\nYOU HAVE TO EXPORT YOUR ACCOUNTS USING KOREPI FIRST!!\n\naccounts.ini file is usually on your korepi folder'
#Creating application window
root = customtkinter.CTk()
        #creating gui
root.geometry('650x350')
root.title('Account Manager')
root.resizable(False, False) 

#Configure grid layout
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2,3), weight=1)
root.grid_rowconfigure((0,1,2), weight=1)

#importing accounts
def select_file():
    file_name = fd.askopenfilename(
    title='Select account file',
    filetypes=[('Initialization files', '*.ini')],
    initialdir='/')
    if file_name == '':
        return print('No file selected')
    shutil.copy(file_name, './accounts.txt')
    if not os.path.isfile('accounts.ini'):
        with open('accounts.ini', 'w') as f:
            print('Created accounts.ini file')
            Settings.read('accounts.ini')
    if not os.path.isfile('settings.ini'):
        with open('settings.ini', 'w') as f:
            print('Created settings.ini file')
            Settings.read('settings.ini')
    try:
        Settings.add_section('Settings')
    except:
        print('Settings section already exists')
    try:
        AccountList.add_section('Accounts')
    except:
        print('Accounts section already exists')
    Settings.set('Settings', 'accounts', file_name)
    with open('settings.ini', 'w') as cfgfile:
        Settings.write(cfgfile)
        print(cfgfile)
    with open('accounts.ini', 'w') as cfgfile2:
        AccountList.write(cfgfile2)
    os.rename('accounts.ini', 'accounts2.txt')
    with open('accounts.txt','r') as firstfile, open('accounts2.txt','a') as secondfile: 
        for line in firstfile: 
                secondfile.write(line)
    try:
        with open('accounts2.txt', 'r') as fr2:
            lines2 = fr2.readlines()
            ptr = 1
            with open('accounts2.txt', 'w') as fw2:
                for line2 in lines2:
                    if ptr != 3:
                        fw2.write(line2)
                    ptr += 1
                print("Deleted")
    except:
        print("Oops! something error")
    os.rename('accounts2.txt', 'accounts.ini')
    os.remove('accounts.txt')
    shutil.copy('accounts.ini', './backup/accounts.ini')
    os.remove('accounts.ini')
    root.destroy()
#open file and save injector location
def select_injector():
    injector_name = fd.askopenfilename(
        title='Select injector file',
        filetypes=[('Executable files', '*.exe')],
        initialdir='/')
    if not os.path.isfile('settings.ini'):
        with open('settings.ini', 'w') as f:
            print('Created settings.ini file')
            Settings.read('settings.ini')
    try:
        Settings.add_section('Settings')
    except:
        print('Injector section already exists')
    Settings.set('Settings', 'Injector', injector_name)
    if injector_name == '':
        print('No file selected')
    with open('settings.ini', 'w') as cfgfile:
        Settings.write(cfgfile)
    for Injector in Settings:
        for key3, value3 in Settings[Injector].items():
            korepi.append(value3)
    print('Injector location: ' + korepi[0])

try:
    for section2 in Backup:
        for key2, value2 in Backup[section2].items():
            acc.append(key2)
    print('Available accounts:' + str(acc))
except:
    print('No accounts.ini file found')
#Getting injector location on boot
try:
    for Injector in Settings:
        for key3, value3 in Settings[Injector].items():
            korepi.append(value3)
    if korepi[0] == '':
        print('No injector file found')
        select_injector()
    else:
        print('Injector location: ' + korepi[0])
except:
    print('No Injector file found')
    print('Please select injector file')
    try:
        try:
            select_injector()
        except:
            print('skipped')
    except:
        print('Injector location: ' + korepi[0])

def select_injector2():
    injector_name = fd.askopenfilename(
        title='Select injector file',
        filetypes=[('Executable files', '*.exe')],
        initialdir='/')
    if injector_name == '':
        return
    if not os.path.isfile('settings.ini'):
        with open('settings.ini', 'w') as f:
            print('Created settings.ini file')
            Settings.read('settings.ini')
    try:
        Settings.add_section('Settings')
    except:
        print('Injector section already exists')
    Settings.set('Settings', 'Injector', injector_name)
    if injector_name == '':
        print('No file selected')
    with open('settings.ini', 'w') as cfgfile:
        Settings.write(cfgfile)
    for Injector in Settings:
        for key3, value3 in Settings[Injector].items():
            korepi.append(value3)
    print('Injector location: ' + korepi[0])
    root.destroy()

def thread_injector():
    threading.Thread(target=launch).start()
accs = []
regs = []
def choose_account(choice):
    acc.append(choice)
def choose_region(choice):
    regs.append(choice)
def launch():
    acco = accSel.get()
    reg = regSel.get()
    if acco == 'Select Account':
        return
    if reg == 'Select Region':
        return
    if reg == 'EU':
        reg = 'eu'
    if reg == 'NA':
        reg = 'usa'
    if reg == 'Asia':
        reg = 'asia'
    if reg == 'TW/HK/MO':
        reg = 'thm'
    fileis = sys.argv[0]
    filepathname = os.path.dirname(fileis)
    finalpath = os.path.abspath(filepathname)
    path = r'./backup/launch.lnk'
    targetInjector = korepi[0]
    injector_dir = os.path.dirname(korepi[0])
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = targetInjector
    shortcut.WorkingDirectory = injector_dir
    shortcut.save()    
    SelAccSelReg = '%s/backup/launch.lnk -account \"%s\" -region \"%s\"' % (finalpath, acco, reg)
    os.system(SelAccSelReg)

sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
ImpInjector = customtkinter.CTkButton(sidebar_frame, text='Change Injector', command=lambda: select_injector2())
ImpInjector.grid(row=8, column=0, padx=20, pady=(10,10))
regSel = customtkinter.StringVar(root)
regSel.set('0')
Region = customtkinter.CTkOptionMenu(sidebar_frame, values=regions, command=choose_region, variable=regSel)
Region.grid(row=2, column=0, padx=20, pady=(10,10))
CTkScrollableDropdown(Region, values=regions)
accSel = customtkinter.StringVar(root)
accSel.set('0')
Account = customtkinter.CTkOptionMenu(sidebar_frame, values=acc, command=choose_account, variable=accSel)
Account.grid(row=4, column=0, padx=20, pady=(10,10))
CTkScrollableDropdown(Account, values=acc)
ImpAcc = customtkinter.CTkButton(sidebar_frame, text='Import Accounts', command=lambda: select_file())
ImpAcc.grid(row=7, column=0, padx=20, pady=(10,10))
AccountLabel = customtkinter.CTkLabel(sidebar_frame, text='Select Account')
AccountLabel.grid(row=3, column=0, padx=20, pady=(10,10))
RegionLabel = customtkinter.CTkLabel(sidebar_frame, text='Select Region')
RegionLabel.grid(row=1, column=0, padx=20, pady=(10,10))
space = customtkinter.CTkLabel(sidebar_frame, text='')
space.grid(row=6, column=0, padx=20, pady=(10,10))
LaunchButton = customtkinter.CTkButton(root, text='Launch', command=lambda: thread_injector())
LaunchButton.grid(row=2, column=1, padx=20, pady=(20,20))
textbox = customtkinter.CTkLabel(root, width=250, text=instructions)
textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
Account.set("Select Account")
Region.set("Select Region")

try:
    os.remove('accounts.ini')
except:
    print('')

root.mainloop()

