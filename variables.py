import settings

class TrackEnv():
    def __init__(self, jumbler, track):
        self.jumbler = jumbler
        self.track = track
        
        self.events = []
        
        self.start = None
        self.last_time = None
        
        self.glitch_start = None
        self.glitch_chance = settings.GLITCH_CHANCE
        self.glitch_duration = settings.GLITCH_DURATION
        
        self.current_pitch = settings.PITCH_START
        self.target_pitch = settings.PITCH_START
        self.pitch_change_chance = settings.PITCH_CHANGE_CHANCE
        
        self.pitch_min = settings.PITCH_MIN
        self.pitch_max = settings.PITCH_MAX
        self.pitch_max_change_speed = settings.PITCH_CHANGE_SPEED
        self.pause = False
        
        self.wait_after_event = settings.MIN_WAIT_AFTER_EVENT
        self.last_event_time = None
        
        self.current_frame = 0
        self.total_frames = 0