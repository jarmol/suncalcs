from Tkinter import *
import datetime, time, math
from time import gmtime, strftime

znt_official = 90.833
d2r = math.pi/180.0
dLT = [0.0, 0.0, 0.0]

def yday(year, month, day):
    print("Date: %d-%d-%d" % (year, month, day))
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    ydN = N1 - (N2 * N3) + day - 30
    return ydN

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
    h=decimhours        # floating hours
    s = 3600*h          # seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

def suncalc(year, month, day, suncalctype, lat1, lot1, localOffset, zenith):
    N = yday(year, month, day)
    print("Zenith %.3f degrees used for %s" % (zenith, suncalctype))

#  2. convert the longitude to hour value and calculate an approximate time
    longitude = lot1
    lngHour = longitude / 15

    if (suncalctype == "SUNRISE"):
        t = N + ((6 - lngHour) / 24)
    else:
        t = N + ((18 - lngHour) / 24)

#  3. calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

#  4. calculate the Sun's true longitude
    L = M + (1.916 * math.sin(d2r*M)) + (0.020 * math.sin(2 * M*d2r)) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
 
    if (L > 360.0):
        L-= 360.0
    elif (L < -360.0):
        L+= 360 

#  5a. calculate the Sun's right ascension
    RA = math.atan(0.91764 * math.tan(d2r*L))

# Correction: added converting RA to degrees / JL 25.12.2014
    RA /= d2r

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
#  Added this JL 25.12.2014
    if (RA > 360.0):
        RA-= 360.0
    elif (RA < -360.0):
        RA+= 360

#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant = (math.floor( L/90)) * 90
    RAquadrant = (math.floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

# 5c. right ascension value needs to be converted into hours
    RA = RA / 15

# 6. calculate the Sun's declination
    sinDec = 0.39782 * math.sin(d2r*L)
    cosDec = math.cos(math.asin(sinDec))
    declin = math.atan(sinDec/cosDec)/d2r
    dLT[2] = declin     # Save declination 

# 7a. calculate the Sun's local hour angle
    latitude = d2r*lat1

    cosH = (math.cos(d2r*zenith) - (sinDec * math.sin(latitude))) / (cosDec * math.cos(latitude))
    if (cosH > 1):
        print "the sun never rises on this location (on the specified date.\n"

    if (cosH < -1):
        print "the sun never sets on this location (on the specified date)\n"

#  7b. finish calculating H and convert into hours   
    H = math.acos(cosH)/d2r # converted to degrees

#  if rising time is desired:
    if (suncalctype == "SUNRISE" ):
        H = 360 - H

        prtx = "Sunrise"
    else:
        prtx = "Sunset" 

#  degrees to hours:
    H = H / 15

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622

#  9. adjust back to UTC
    UT = (T - lngHour) % 24
        
#    print("%s UT %s" % (prtx, human(UT)))

# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset
    if (suncalctype == "SUNRISE"):
        dLT[0] = localT   
    else:
        dLT[1] = localT
 
#    return ("%s local time %s" % (prtx, human(localT)))
    return human(localT)

# end of suncalc()

# Main Begin

root = Tk()
root.geometry("350x300+200+200")
root.title("Suncalculator")

Label(root, text="Latitude", fg="red").place(relx=0, rely=0)		# Latitude
Label(root, text="Longitude, TZ", fg="red").place(relx=0, rely=0.1)	# Longitude & TZ
Label(root, text="Current time", fg="red").place(relx=0, rely=0.2)	# Local time
Label(root, text="Sunrise time", fg="red").place(relx=0, rely=0.3)	# Sunrise time official
Label(root, text="Sunset time", fg="red").place(relx=0, rely=0.4)	# Sunset time
Label(root, text="Daylength", fg="red").place(relx=0, rely=0.5)		# Daylength
Label(root, text="Noon time", fg="red").place(relx=0, rely=0.6)		# Noontime
Label(root, text="Sun elevation", fg="red").place(relx=0, rely=0.7)	# Noontime

now = datetime.datetime.now()
nyear = now.year
nmonth = now.month
nday = now.day

latitude = 60.18; longitude = 24.93; tzone = 2.0

content = StringVar()
content.set("%.2f" % latitude)
e1 = Entry(root, textvariable=content).place(relx=0.3, rely=0)

content2 = StringVar()
content2.set("%.2f" % longitude)
e2 = Entry(root, textvariable=content2).place(relx=0.3, rely=0.1)

content3 = StringVar()
content3.set("%.1f" % tzone)
e3 = Entry(root, textvariable=content3).place(relx=0.75, rely=0.1, relwidth=0.2)

content4 = StringVar()
s4 = time.strftime("%d.%m.%Y %T", time.localtime())
content4.set(s4)
e4 = Entry(root, textvariable=content4).place(relx=0.3, rely=0.2)

content5 = StringVar()
s5 = suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_official)
content5.set(s5)
e5 = Entry(root, textvariable=content5).place(relx=0.3, rely=0.3)

content6 = StringVar()
s6 = suncalc(nyear, nmonth, nday, "SUNSET", latitude, longitude, tzone, znt_official)
content6.set(s6)
e6 = Entry(root, textvariable=content6).place(relx=0.3, rely=0.4)

# daylength, noontime and elevation
deltas = (dLT[1] - dLT[0])
#print dLT[0], dLT[1], human(deltas)
isnoont = dLT[0] + 0.5*deltas
iselevation = ("%.2f deg" % (90 - latitude + dLT[2]))

content7 = StringVar()
content7.set(human(deltas))
e7 = Entry(root, textvariable=content7).place(relx=0.3, rely=0.5)

content8 = StringVar()
content8.set(human(isnoont))
e8 = Entry(root, textvariable=content8).place(relx=0.3, rely=0.6)

content9 = StringVar()
content9.set(iselevation)
e9 = Entry(root, textvariable=content9).place(relx=0.3, rely=0.7)

#button1 = Button(root, text="C -> F", command=yday(nyear, nmonth, nday)).pack(side=BOTTOM)

root.mainloop()
