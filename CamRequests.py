import requests
from xml.etree import ElementTree


class CamRequests:
    cam_url = 'http://192.168.1.254/'

    EV = {'+2.0': 0, '+1.7': 1, '+1.3': 2, '+1.0': 3, '+0.7': 4, '+0.3': 5, '0.0':  6, '-0.3': 7, '-0.7': 8,
          '-1.0': 9, '-1.3': 10, '-1.7': 11, '-2.0': 12}
    MODE = {'photo': 0, 'video': 1, 'preview': 2}
    VIDEO_RESOLUTION = {'720p60': 0, 'test': 1, '720p30': 2, '480p30': 3}  # wrong
    PHOTO_RESOLUTION = {'14M': 0, '12M': 1, '10M': 2, '8M': 4, '5M': 4, '3M': 5, '2MHD': 6, 'VGA': 7, '1.3M': 8}

    # general
    def send_get(self, command_nr, parameters=[], url=cam_url):
        """the get commandlú"""
        params = [('custom', '1'), ('cmd', command_nr)] + parameters
        r = requests.get(url, params=params)
        return r

    def set_modus(self, modus):
        self.send_get(3001, [('par', str(modus))])

    def ping(self):
        x = self.send_get(2016)
        print(x.text)

    # video functions
    def start_recording(self):
        self.send_get(2001, [('str', '1')])

    def stop_recording(self):
        self.send_get(2001, [('str', '0')])

    def set_video_resolution(self, resolution):
        self.set_modus('video')
        self.send_get(2002, [('par', str(resolution))])

    # photo functions
    def take_photo(self):
        self.set_modus('photo')
        self.send_get(1001)

    def set_photo_resolution(self, resolution):
        self.set_modus('video')
        self.send_get(1002, [('par', str(resolution))])

    def get_number_of_left_captures(self):
        x = self.send_get(1003)
        elementText = ElementTree.fromstring(x.text)
        return elementText.find('./Value').text

    def set_hdr(self, hdr):
        if hdr == 1:
            flag = '1'
        else:
            flag = '0'
        self.send_get(2004, [('par', flag)])

    def set_ev(self, ev):
        self.send_get(2005, [('par', str(ev))])

    def set_motion_detection(self, detect):
        if detect == 1:
            flag = '1'
        else:
            flag = '0'
        return self._get(2006, [('par', flag)])

    def set_audio_capture(self, capture):
        if capture == 1:
            flag = '1'
        else:
            flag = '0'
        return self._get(2007, [('par', flag)])

    def set_timestamp(self, stamp):
        if stamp == 1:
            flag = '1'
        else:
            flag = '0'
        return self._get(2008, [('par', flag)])
