from timeit import default_timer as timer
from collections import defaultdict,OrderedDict
from datetime import datetime
from subprocess import Popen, PIPE
import time,sys,traceback

class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        #in python3 you can omit the args to super
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

def run_bash_old(cmd):
    p = Popen(cmd, stdout=PIPE, shell=True)
    (output, err) = p.communicate()
    if not err is None:
        print("could not run bash command")
    return output

def run_bash(cmd):
    process = Popen(cmd, stdout=PIPE,shell=True)
    ## But do not wait till netstat finish, start displaying output immediately ##
    string = ''
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            string += out
            if out=='\n':                
                sys.stdout.write(string)
                sys.stdout.flush()
                string = ''

def splitter(df, chunkSize = 2000):
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        yield df[i*chunkSize:(i+1)*chunkSize]

def ChTimeForm(time_str,_from,_to):
    return datetime.strftime(datetime.strptime(time_str,_from),_to)[:-3]

def pretty_time(sec):
    if sec/3600>=1:
        time = sec/3600.0;unit = '[h]'
    elif sec/60>=1:
        time = sec/60.0;unit = '[min]'
    elif sec/60<1:
        time = sec;unit = '[sec]'
    return '%.2f %s'%(time,unit)

class Timer(object):
    def __init__(self, arg=1):
        self.arg = arg
    def __call__(self,f):        
        def inner(*args, **kwargs):
            start = timer()
            f(*args, **kwargs)            
            print('elapsed %s'%pretty_time(timer() - start))
        return inner
    
class Logger_out(object):
    def __init__(self,stream,mode,filename="Default.log"):
        self.terminal = stream
        self.log = open(filename,mode)
    def write(self, message):
        if message.strip():
            self.terminal.write(str(datetime.now())+" "+message+"\n")
            self.log.write(str(datetime.now())+" "+message+"\n")
            self.log.flush()
    def flush(self):
        pass

class Logger_err(object):
    def __init__(self,stream,mode,filename="Default.log"):
        self.terminal = stream
        self.log = open(filename,mode)
    def write(self, message):
        antet = ''
        if message.strip():
            if 'Traceback' in message:
                antet = str(datetime.now())+ " "
            self.terminal.write(antet+message.strip("\n")+"\n")
            self.log.write(antet + message.strip("\n")+"\n")
            self.log.flush()
    def flush(self):
        pass

class Log(object):
    def __init__(self,filename="Default.log"):
        self.arg = filename
    def __call__(self,f):
        def inner(*args, **kwargs):
            orig_stdout = sys.stdout
            orig_stderr = sys.stderr
            sys.stdout = Logger_out(sys.stdout,"a",self.arg)
            sys.stderr = Logger_err(sys.stderr,"a",self.arg)
            f(*args, **kwargs)
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr
        return inner
            
class Wait_bar(object):
    def __init__(self,iterations = 0,percent=.1,increment =1):
        self.laps = []
        self.cnt = 0
        self.ref = timer()
        self.iter = iterations
        self.incr = increment
        self.global_ref = timer()        
        self.often = int(iterations*percent)
        if self.often == 0:
            self.often = 1

    def display(self):
        self.cnt+=self.incr
        if self.cnt%self.often==0:
            est_left_time = (self.iter - self.cnt)*(timer()-self.ref)/float(self.often)
            passed = pretty_time(timer()-self.global_ref)
            print('%.2f%% done, estimated left time: %s, passed: %s'%((100*self.cnt)/float(self.iter),pretty_time(est_left_time),passed))
            self.laps.append((timer(),est_left_time))
            self.ref = timer()

class Retry(object):
    def __init__(self, sleep=0.5,iters=2,func=None):
        self.max = iters
        self.excep = ''
        self.pause = sleep
        self.func = func
    def __call__(self,f):        
        def inner(*args, **kwargs):
            cnt=0
            while True:
                if cnt>self.max:                    
                    raise Exception('maximum execution times reached')
                if cnt>0:
                    traceback.print_exc(file=sys.stderr)
                    print('error %s occured, sleeping %d [sec]...'%(str(self.excep),self.pause))
                    time.sleep(self.pause)
                try:
                    if cnt==0:
                        f(*args, **kwargs)
                    else:
                        f(self.func(*args, **kwargs))
                except Exception as er:
                    self.excep = str(er)
                    cnt+=1
                    continue
                break
        return inner


if __name__=="__main__":
    ######################################--Testing--######################################
    def inside(var):
        print("this func is runnning when an error is triggerd")
        return 3


    @Retry()
    def test(fff):
        int(fff)


    ######################################--Testing--######################################
    def test2():
        wb = Wait_bar(100,.001)
        for i in range(100):
            pass
            time.sleep(1)
            wb.display()


    ######################################--Testing--######################################
    @Log(filename="log.log")
    def test3():
        print "starting1..."
        print "starting2..."
        raise ValueError("eroare")

    test2()
    

