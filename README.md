org1411
=======

Zerynth library for ORG1411 GPS module
---------------------------------------

This module contains the [Zerynth](https://www.zerynth.com/) driver for OriginGPS Nano Hornet ORG1411 GPS module ([product page](https://www.origingps.com/products/hornet-org-1411/)).

Example:
    
    import org1411 as gps
    import streams
    
    streams.serial()
    try:
    
        # init gps module
        drv_gps = SERIAL2
        pwr_gps = D6
        wup_gps = D0
        gps.init(drv_gps, pwr_gps, wup_gps)
        
        while True:
            # retrieve global position
            res = gps.get_lla()
            
            if res != 0:
                lat, lon, alt = res
                print("latitude = %+10.6f" % lat)
                print("longitude = %+011.6f" % lon)
                print("altitude = %.1f" % alt)
            print("- - - - - - - - -")
            sleep(2000)
    except Exception as e:
        print(e)

