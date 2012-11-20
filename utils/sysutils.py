import subprocess

def move_file(movefrom, moveto):
    print "moving file %s --> %s" % (movefrom, moveto)
    try:
        subprocess.Popen(['mv %s %s' % (movefrom, moveto)], shell=True)
    except Exception, e:
        print "[ERROR] unable to move file: %s, %s" % (movefrom, moveto)
    return

def delete_file(filepath):
    print "remove file %s" % filepath
    try:
        subprocess.Popen(['rm %s'%imgpath], shell=True)
    except Exception, e:
        print "[ERROR] unable to remove file: %s" % filepath
    return
