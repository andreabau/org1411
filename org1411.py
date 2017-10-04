import streams
import timers

new_exception(org1411Exception, Exception)

_ser = None
_pwr = None
_wup = None


def _send(cmd):
    _ser.write(cmd + '\r\n')


def _read(timeout=2000):
    t = timers.timer()
    t.start()
    while not _ser.available():
        if t.get() > timeout:
            return "timeout"
    return _ser.readline().strip('\r\n').strip(chr(0))

# send messages to stop continous stream
def _set_freq():
    _send('$PSRF103,02,00,00,01*26')
    _send('$PSRF103,03,00,00,01*27')
    _send('$PSRF103,04,00,00,01*20')
    _send('$PSRF103,00,00,00,01*24')


def get_lla():
    #send request for gga message
    _send('$PSRF103,00,01,00,01*25')
    res = _read()
    return _parse_gga_lla(res)


def _parse_gga_lla(res):
    parts = res.split(',')
    # msg_id      = parts[0]
    # utc_time    = parts[1]
    latitude    = parts[2]
    latitude_d  = parts[3]
    longitude   = parts[4]
    longitude_d = parts[5]
    # pos_fix     = parts[6]
    # n_satell    = parts[7]
    # hdop        = parts[8]
    altitude    = parts[9]
    # alt_units   = parts[10]
    # geoid_sep   = parts[11]
    # geoid_units = parts[12]
    # age_diff_c  = parts[13]
    # diff_ref    = parts[14]

    if len(latitude) > 4:
        lat = int(latitude[:2]) + float(latitude[2:]) / 60
        if latitude_d == 'S':
            lat = -lat

        lon = int(longitude[:3]) + float(longitude[3:]) / 60
        if longitude_d == 'W':
            lon = -lon

        alt = float(altitude)

        return lat, lon, alt
    else:
        return 0


def _pulse():
    digitalWrite(_pwr, HIGH)
    sleep(100)
    digitalWrite(_pwr, LOW)


def init(ser_drv, pwr_pin, wup_pin, rst_pin=None):
    global _pwr, _wup

    _pwr = pwr_pin
    _wup = wup_pin

    if _ser is not None:
        _ser.close()
        _ser = None

    _ser = streams.serial(ser_drv, set_default=False, baud=4800)

    pinMode(_wup, INPUT)
    pinMode(_pwr, OUTPUT)

    _pulse()
    sleep(50)
    while not digitalRead(_wup):
        _pulse()
        sleep(50)

    t = timers.timer()
    t.start()

    while _read() != '$PSRF150,1*3E':
        if t.get() > 2500:
            raise org1411Exception

    _set_freq()
