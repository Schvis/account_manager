### Author: Schvis ###
### Testing and debugging: rekiihype & crossxzone
### Importing needed libraries ###
import customtkinter
import os, sys
from customtkinter import filedialog as fd
from configparser import ConfigParser
import shutil
from win32com.client import Dispatch
from CTkScrollableDropdown import *
import threading
import pythoncom
import time

### Setting and reading settings and account file information ###
Settings = ConfigParser()
AccountList = ConfigParser()
Backup = ConfigParser()
LastUsed = ConfigParser()
Settings.read('settings.ini')
AccountList.read('accounts.ini')
LastUsed.read('last_used.ini')
### Creating .ini files if they don't exist ###
if os.path.isfile('./backup/accounts.ini'):
    Backup.read('./backup/accounts.ini')
if not os.path.exists('./backup'):
    os.makedirs('./backup')    
if not os.path.isfile('last_used.ini'):
        with open('last_used.ini', 'w') as f:
            print('Created last_used.ini file')
            LastUsed.read('last_used.ini')
try:
    LastUsed.add_section('Used')
    with open('last_used.ini', 'w') as f:
        LastUsed.write(f)
except:
    print('')
### Arrays to keep track of selected accounts ###
regions = [
    'EU',
    'NA',
    'Asia',
    'TW/HK/MO',
]
acc = []
korepi = []
usedaccs = []
instructions = '1) Click on the "Import Accounts" button to import accounts\nAPP WILL RELOAD AFTER SELECING INJECTOR/ACCOUNT!\n\n2)Choose your region and account\n3)Click on launch\n\nYOU HAVE TO EXPORT YOUR ACCOUNTS USING KOREPI FIRST!!\n\naccounts.ini file is usually on your korepi folder'
### Creating GUI ###
root = customtkinter.CTk()
root.geometry('650x350')
root.title('Account Manager')
root.resizable(False, False) 
### Configuring grid layout ###
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2,3), weight=1)
root.grid_rowconfigure((0,1,2), weight=1)
### Function to import accounts from accounts.ini file ###
def select_file():
    file_name = fd.askopenfilename(
    title='Select account file',
    filetypes=[('Initialization files', '*.ini')],
    initialdir='/')
    if file_name == '':
        return print('No file selected')
    shutil.copy(file_name, './accounts.txt')
    ### Creating .ini files if it was deleted ###
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
        AccountList.add_section('Accounts')
    except:
        print('Settings/Account section already exists')
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
    ### Deleting bugged line on file, cuz i don't know how to fix it. ###
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
    os.rename('accounts2.txt', 'accounts3.ini')
    os.remove('accounts.txt')
    shutil.copy('accounts3.ini', './backup/accounts.ini')
    os.remove('accounts3.ini')
    threading.Thread(target=reopen).start()
    root.destroy()
### Function to select injecter on boot if not already selected ###
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
        for InjectorKey, InjectorValue in Settings[Injector].items():
            korepi.append(InjectorValue)
    print('Injector location: ' + korepi[0])
### Getting saved account files on boot ###
try:
    for section2 in Backup:
        for AccountKey, AccountValue in Backup[section2].items():
            acc.append(AccountKey)
    print('Available accounts:' + str(acc))
except:
    print('No accounts.ini file found')
### Checking if account was already selected from last use ###
try:
    for Used in LastUsed:
        for UsedAcc, UsedValue in LastUsed[Used].items():
            usedaccs.append(UsedValue)
    print('Last used account: ' + usedaccs[0])
    print('Last used region: ' + usedaccs[1])
except:
    print('No used accounts found')
    print('No used regions found')
### Getting injector location on boot ###
try:
    for Injector in Settings:
        for InjectorKey, InjectorValue in Settings[Injector].items():
            korepi.append(InjectorValue)
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
### Function to change injector file if path was changed/updated ###
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
    threading.Thread(target=reopen).start()
    root.destroy()
### Function to reload the launcher without needing to open it manually again ###
def reopen():
    fileis = sys.argv[0]
    time.sleep(1)
    os.system(os.path.realpath(fileis))
### Threading so app doesn't freeze on launch ###
def thread_injector():
    threading.Thread(target=launch).start()
### Funcion to launch selected account and region, and saving it for the next use ###
def launch():
    acco = accSel.get()
    reg = regSel.get()
    LastUsed.set('Used', 'SelectedAcc', acco)
    LastUsed.set('Used', 'SelectedReg', reg)
    with open ('last_used.ini', 'w') as last:
        LastUsed.write(last)
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
    pythoncom.CoInitialize()
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = targetInjector
    shortcut.WorkingDirectory = injector_dir
    shortcut.save()    
    SelAccSelReg = r'%s/backup/launch.lnk -account \"%s\" -region \"%s\"' % (finalpath, acco, reg)
    print('Selected account: %s Region: %s' % (acco, reg))
    print(r'%s' % SelAccSelReg)
    os.system(r'%s' % SelAccSelReg)
### Adding all the widgets to the main window ###
sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
ImpInjector = customtkinter.CTkButton(sidebar_frame, text='Change Injector', command=lambda: select_injector2())
ImpInjector.grid(row=8, column=0, padx=20, pady=(10,10))
regSel = customtkinter.StringVar(root)
regSel.set('0')
Region = customtkinter.CTkOptionMenu(sidebar_frame, values=regions, variable=regSel)
Region.grid(row=2, column=0, padx=20, pady=(10,10))
CTkScrollableDropdown(Region, values=regions)
accSel = customtkinter.StringVar(root)
accSel.set('0')
Account = customtkinter.CTkOptionMenu(sidebar_frame, values=acc, variable=accSel)
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
### Setting default values for account and region ###
try:
    if (usedaccs[0] == ''):
        Account.set("Select Account")
    else:
        Account.set(usedaccs[0])
    if (usedaccs[1] == ''):
        Region.set("Select Region")
    else:
        Region.set(usedaccs[1])
except:
    print('Failed to retrieve last_used.ini file')
    Region.set("Select Region")
    Account.set("Select Account")
### Deleting accounts3.ini if it exists to prevent bugs ###
try:
    os.remove('accounts3.ini')
except:
    print('')
### Keeping the window open until the user closes it ###
root.mainloop()

