import serial
import subprocess
from subprocess import CalledProcessError
import os

class LPCLink2(object):

    def __init__(self, base_path='/usr/local/lpcxpresso/lpcxpresso/bin/'):
        self.base_path = base_path
        self.dfu_boot()

    def dfu_boot(self):
        dfu_flags = ['dfu-util', '-d', '0x1FC9:0x000C', '-c', '0', '-t', '2048', '-R']
        dfu_flags.extend(['-D', self.base_path+'LPC432x_CMSIS_DAP_V5_173.bin.hdr'])
        try:
            output = subprocess.run(dfu_flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except CalledProcessError:
            pass

    def program(self, filename, load_base=0, target_board='LPC1768', debug=False):
        redlink_flags = [self.base_path+'crt_emu_cm_redlink', '-p'+target_board, '-load-base='+str(load_base) ]

        if debug:
            redlink_flags.extend(['-g'])

        redlink_flags.extend(['-flash-load-exec='+filename])

        try:
            output = subprocess.run(redlink_flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except CalledProcessError:
            raise

        return True if output.returncode == 0 else False
