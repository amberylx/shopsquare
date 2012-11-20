import subprocess

def move_file(movefrom, moveto):
    print "moving file %s --> %s" % (movefrom, moveto)
    subprocess.Popen(['mv %s %s' % (movefrom, moveto)], shell=True)
    return

def delete_file(filepath):
    print "remove file %s" % filepath
    subprocess.Popen(['rm %s'%imgpath], shell=True)
    return
