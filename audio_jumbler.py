import sounddevice as sd
import subprocess as sp
import settings
import variables
import random
import numpy
from scipy.interpolate import UnivariateSpline
import threading

env = None

class Track:
    def __init__(self, name, seek_to=False):
        self.name = name
        self.seek_to = seek_to
        self.is_valid_track = False
        
        pipe = sp.Popen([settings.FFMPEG_BIN,"-i", name, "-"], 
                        stdin=sp.PIPE, stdout=sp.PIPE,  stderr=sp.PIPE)
        pipe.stdout.read()
        pipe.terminate()
        infos = pipe.stderr.read().split(b"\r\n")
        for info in infos:
            info = info.strip()
            
            #print (info)
            if info.startswith(b"Duration: "):
                self.timestr = info.replace(b"Duration: ", b"").split(b", ")[0]
            elif info.startswith(b"Stream"):
                
                linedata = info.split(b":")
                
                data = linedata[-1].split(b", ")
                
                #print(linedata)
                #print(data)
                streaheader = linedata[:3]
                
                stream_type = streaheader[-1]
                
                #print(stream_type)
                
                if stream_type.strip().lower() == b"audio":
                    
                    #print(data)
                    self.format = data[0]
                    self.frequency = int(data[1].split(b" ")[0])
                    self.channels = 1
                    if data[2] == b"stereo":
                        self.channels = 2
                    self.bits = data[3]
                    self.rate = data[4]
                    
                    self.is_valid_track = True
        
        if not self.is_valid_track:
            return
        
        self.runtime = self.time_to_sec(self.timestr)
        
        self.frames = int(self.runtime * self.frequency)
        
        self.position = 0
        self.frame = 0
        
        if seek_to:
            self.frame = int(self.frames * (seek_to / self.runtime))
            self.position = self.frame*self.channels*2
        
        #self.open()
        
        #self.data = self._read(self.frames*self.channels*2)
        #self.data = self._read(self.frames*4)
        
        #print(len(self.data), self.frames)
        
        
        #self.close()    
    
    def time_to_sec(self, timebstring):
        h, m, s = timebstring.split(b":")
        
        hours = int(h)
        minutes = int(m)
        seconds = float(s)
        
        time = hours*360.0 + minutes*60.0 + seconds
        return time
    
    def open(self):
        if self.seek_to:
            command = [settings.FFMPEG_BIN,
                        '-ss', str(self.seek_to),
                        '-i', self.name,
                        '-f', 's16le',
                        #'-acodec', 'pcm_s16le',
                        '-ar', str(self.frequency), # ouput will have 44100 Hz
                        '-ac', str(self.channels), # stereo (set to '1' for mono)
                        '-']
        else:
            command = [settings.FFMPEG_BIN,
                        '-i', self.name,
                        '-f', 's16le',
                        #'-acodec', 'pcm_s16le',
                        '-ar', str(self.frequency), # ouput will have 44100 Hz
                        '-ac', str(self.channels), # stereo (set to '1' for mono)
                        '-']
        self.pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=10**8)
        
    def close(self):
        self.pipe.terminate()
    
    def _read(self, length):
        read = self.pipe.stdout.read(length)
        self.position += len(read)
        self.frame +=  len(read)/(self.channels*2) # stereo * bytes (16 bit)
        #print(self.position, self.frame)
        return read
    
    def read(self, length):
        return self._read(length)

#class AudioSequence:
#    
#    def __init__(self, track, chunksize=1000, name="tmp.wav"):
#        self.data = self.transcribe_track(track, chunksize, name)
#        self.fh = open(name, "br")
#        self.position = 0
#        
#    def read(self, length):
#        read = self.fh.read(length)
#        self.position = self.position + len(read)
#        return read
#    
#    def close(self):
#        self.close()
#    
#    def seek(self, position):
#        self.fh.seek(position)
#        self.position = position
#        
#    def transcribe_track(self, track, block=1000, name="tmp.wav"):
#        track.open()
#        with open(name, "bw") as tmph:
#        
#            read = track.read(block)
#            while read:
#                tmph.write(read)
#        
#        track.close()
        
        #end = self.position + length
        #if end >= len(self.data):
        #    end = len(self.data)
        #
        #return self.data[self.position:end]
        
        #return self.pipe.stdout.read(length)

def _callback(indata, outdata, frames, time, status):
    global env
    
    if env.pause:
        for i in range(env.track.channels):
            outdata[:,i] = numpy.zeros(frames)
        return
        
    if not env.start:
        env.start = time.currentTime
    
    #print (time.currentTime)
    if not env.last_time:
        env.last_time = time.currentTime
        
    can_do_event = True
    if env.last_event_time:
        can_do_event = time.currentTime - env.last_event_time >= env.wait_after_event
    
    if can_do_event:
        if env.last_time and not env.glitch_start:
            if random.random() < env.glitch_chance*(time.currentTime - env.last_time):
                env.glitch_start = time.currentTime
                print(str(time.currentTime-env.start) + ": glitch")
                env.last_event_time = time.currentTime
                
        if env.current_pitch == env.target_pitch and random.random() < env.pitch_change_chance*(time.currentTime - env.last_time):
            env.target_pitch = random.uniform(env.pitch_min, env.pitch_max)
            print(str(time.currentTime-env.start) + ": pitch change to " + str(env.target_pitch))
            env.last_event_time = time.currentTime
        
    if env.glitch_start and time.currentTime - env.glitch_start < env.glitch_duration:
        for i in range(env.track.channels):
            outdata[:,i] = numpy.zeros(frames)
        return
    else:
        env.glitch_start = None
        
    if env.current_pitch != env.target_pitch:
        increment = env.target_pitch - env.current_pitch
        sign = numpy.sign(increment)
        increment = abs(increment)
        max_pitch_increment = env.pitch_max_change_speed * (time.currentTime - env.last_time)
        if increment > max_pitch_increment:
            increment = max_pitch_increment
        env.current_pitch += increment * sign
        print (increment, sign, env.current_pitch)
        env.last_event_time = time.currentTime
        env.ui.invalidate_data()
    
    #if settings.DO_SEEK:
    #    while env.track.frame < settings.SEEK_TO:
    #        frames_left = int(settings.SEEK_TO - env.track.frame)
    #        
    #       toread = frames_left*4
    #        if toread > 1280000:
    #            toread = 1280000
    #        read = env.track.read(toread)
    #        print (frames_left, len(read))
    #        env.current_frame = env.track.frame
    #        #import time as ttime
    #        #ttime.sleep(1)
    #        
    #        if read == 0:
    #            break
    
    env.current_frame = int(frames*env.current_pitch) + env.current_frame
    env.ui.invalidate_data()
    
    toread = int(frames*env.current_pitch)*env.track.channels*2 # 2 channels and 2 bytes per entry
    raw_audio = env.track.read(toread)
    read = len(raw_audio)
    #print (raw_audio)
    audio_array = numpy.fromstring(raw_audio, dtype="int16")
    
    audio_array = audio_array.reshape((len(audio_array)/env.track.channels,env.track.channels))
    
    #channel_0 = numpy.arange(0, frames, 2)
    #channel_1 = numpy.arange(0, frames, 2)
    #channel_0_new = numpy.arange(frames)       # Where you want to interpolate
    #channel_1_new = numpy.arange(frames)       # Where you want to interpolate
    
    #print(str(frames), str(toread), str(len(channel_0)), str(len(channel_0_new)))
    
    ch_list = [audio_array[:,i] for i in range(env.track.channels)]
    #ch0 = audio_array[:,0]
    #ch1 = audio_array[:,1]
    
    old_idx_list = [numpy.arange(0,len(ch_list[i])) for i in range(env.track.channels)]
    
    #old_indices = numpy.arange(0,len(ch0))
    new_length = frames
    
    new_idx_list = [numpy.linspace(0,len(ch_list[i])-1,new_length) for i in range(env.track.channels)]
    
    #new_indices = numpy.linspace(0,len(ch0)-1,new_length)
    
    splice_list = [UnivariateSpline(old_idx_list[i],ch_list[i],k=1,s=0) for i in range(env.track.channels)]
    
    #spl0 = UnivariateSpline(old_indices,ch0,k=1,s=0)
    #spl1 = UnivariateSpline(old_indices,ch1,k=1,s=0)
    
    #ch_arrays = [splice_list[i](new_idx_list[i]) for i in range(env.track.channels)]
    
    #ch0_array = spl0(new_indices)
    #ch1_array = spl1(new_indices)

    for i in range(env.track.channels):
        outdata[:,i] = splice_list[i](new_idx_list[i])
    
    #outdata[:,0] = ch0_array
    #outdata[:,1] = ch1_array

    #print(max(ch0_array))
    
    env.last_time = time.currentTime
    
    if read < toread:
        print ("track end")
        raise sd.CallbackStop()
    
    #channel_0_new = numpy.interp(channel_0_new, channel_0, audio_array[:,0])
    #channel_1_new = numpy.interp(channel_1_new, channel_1, audio_array[:,1]) 
    
    #outdata[:,0] = channel_0_new
    #outdata[:,1] = channel_1_new
    
def _callback_finish():
    global env
        
class AudioJumbler():
    def __init__(self):
        global env
        self.env = env
        self.playing = False
        self.lock = threading.Lock()
        self.at = 0
        self.restart = False
        self.reset_variables = False
        
    def enter_critical(self):
        self.lock.acquire()
    
    def leave_critical(self):
        self.lock.release()
    
    def run(self, getfiles, idx=0, ui = None):
        global env
        self.ui = ui
        
        if self.playing:
            self.stop()
            
        while self.playing:
            pass
        
        self.terminate = False
        self.playing = True
        self.env = env
        self.calllist = getfiles
        self.at = idx
        files = getfiles()
        while not self.terminate:
            self.enter_critical()
            if self.at >= len(files):
                self.at = 0
            
            print("playing track "+ str(self.at) + ": " + files[self.at])
            
            if settings.DO_SEEK:
                settings.DO_SEEK = False
                t = Track(files[self.at], settings.SEEK_TO)
            else:
                t = Track(files[self.at])
            
            #if not env:
            
            if t.is_valid_track:
                
                if env and not self.reset_variables:
                    pitch = env.target_pitch 
                elif not env:
                    pitch = settings.PITCH_START      
                
                env = variables.TrackEnv(self, t)
                
                if not self.reset_variables:
                    env.current_pitch = pitch
                    env.target_pitch = pitch
                    self.reset_variables = False
                #else:
                #    self.reset_variables = False
                    
                env.ui = ui
                env.current_frame = 0
                env.total_frames = t.frames
                self.env = env
                
                #audioseq = AudioSequence(t)
                
                t.open()
                self.leave_critical()
                ui.invalidate_data()
                self.stream = sd.Stream(samplerate=int(t.frequency), channels=t.channels, dtype="int16", callback=_callback, finished_callback=_callback_finish)
                self.stream.start()
                
                t.pipe.stderr.readlines()
                
                t.close()    
                self.stream.stop()
                
                print("\tdone")
            else:
                self.leave_critical()
                print("\terror creating pipe, file type seems to not be supported")
            
            #print(1)
            files = getfiles()
            
            #print(2)
            self.enter_critical()
            
            #print(3)
            if not self.restart:
                self.at += 1
                self.reset_variables = True
            else:
                self.reset_variables = False
            self.restart = False
            
            #print(4)
            self.leave_critical()
            print("next")
        
        self.playing = False
        
    def seek(self):
        self.enter_critical()
        self.restart = True
        self.leave_critical()
        env.track.close()
    
    def stop(self):
        global env
        self.terminate = True
        print("stopping playback and closing stream")
        if self.playing:
            self.enter_critical()
            self.at = len(self.calllist())
            self.leave_critical()
            if env:
                env.track.close()
        
    def go_to(self, to):
        global env
        print("changing track to index: " + str(to))
        self.enter_critical()
        self.at = to-1
        self.leave_critical()
        if env:
            env.track.close()