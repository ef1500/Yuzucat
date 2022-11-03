# client/server API - Client Side
# objectives -> Run Commands From the Command Line
#            -> Execute Script
import os
import uuid
import shlex
import subprocess

def run_command(cmd):
    # Run a command in a shell and then return the output of the terminal
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                            shell=True, universal_newlines=True)
    stdout, stderr = proc.communicate()
    out = stdout if stdout else stderr
    return out

def run_script(script, dir=os.curdir):
    # Execute a script
    scriptname = str(uuid.uuid4().hex) + '.py'
    args = shlex.split(f"python3 {dir}{scriptname}")
    with open(dir+scriptname, mode='w+', encoding='utf-8') as tempscript:
        tempscript.write(script)
        tempscript.close()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                            shell=True, universal_newlines=True)
    stdout, stderr = proc.communicate()
    out = stdout if stdout else stderr
    os.remove(dir+scriptname)
    return out

def run_script_from_file(file, dir=os.curdir):
    # Execute a script from aa file
    script = open(file, encoding='utf-8').read()
    scriptname = str(uuid.uuid4().hex) + '.py'
    args = shlex.split(f"python3 {dir}{scriptname}")
    with open(dir+scriptname, mode='w+', encoding='utf-8') as tempscript:
        tempscript.write(script)
        tempscript.close()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                            shell=True, universal_newlines=True)
    stdout, stderr = proc.communicate()
    out = stdout if stdout else stderr
    os.remove(dir+scriptname)
    return out