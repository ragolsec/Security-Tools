# This script asks from user the title of the window user wants to terminate.
# It then finds out the correct process IDs and terminates the process.
# Depending on the program it may terminate all of the instances or only the latest one.
# Uses Windows API for all the heavy lifting. 


import ctypes


k_handle = ctypes.WinDLL("Kernel32.dll")
u_handle = ctypes.WinDLL("User32.dll")



lpClassName = None
lpWindowName = ctypes.c_char_p(input("Enter Window Name to Kill: ").encode())


#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-findwindowa

hWnd = u_handle.FindWindowA(lpClassName, lpWindowName) 

if hWnd == 0:
	print("Error Code: {0} - Could Not Grab the Handle for the Window.".format(k_handle.GetLastError()))
else:
	print("Handle for the Window was created!")



# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid

lpdwProcessId = ctypes.c_ulong()
response = u_handle.GetWindowThreadProcessId(hWnd, ctypes.byref(lpdwProcessId))

if response == 0:
	print("Error Code: {0} - Could Not Grab PID".format(k_handle.GetLastError()))
	exit(1)
else:
	print("Got the PID!")



#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
dwDesiredAccess = PROCESS_ALL_ACCESS
bInheritHandle = False

hProc = k_handle.OpenProcess(dwDesiredAccess, bInheritHandle, lpdwProcessId) 

if hProc == 0:
	print("Error Code: {0} - Could not get the handle for the process.".format(k_handle.GetLastError()))
	exit(1)
else:
	print("Got the handle for the process!")
	


#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess

terminated = k_handle.TerminateProcess(hProc, 0)

if terminated == 0:
	print("Error Code: {0} - Could not terminate the process.".format(k_handle.GetLastError()))
	exit(1)
else:
	print("Process terminated!")



