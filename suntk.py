from Tkinter import *
import datetime, time, math
import tkMessageBox
from time import gmtime, strftime
from datetime import date

znt_official = 90.833
dLT = [0.0, 0.0, 0.0]

rad  = lambda x: math.pi*x/180.0
cosd = lambda x: math.cos(rad(x))
sind = lambda x: math.sin(rad(x))
tand = lambda x: math.tan(rad(x))
degr = lambda x: 180.0*x/math.pi

def yday(year, month, day):
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
    L = M + (1.916 * sind(M)) + 0.020*sind(2*M) + 282.634

#  NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
 
    if (L > 360.0):
        L-= 360.0
    elif (L < -360.0):
        L+= 360 

#  5a. calculate the Sun's right ascension
    RA = math.atan(0.91764 * tand(L))

# Correction: added converting RA to degrees / JL 25.12.2014
    RA = degr(RA)

#  NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
#  Added this JL 25.12.2014
    if (RA > 360.0):
        RA-= 360.0
    elif (RA < -360.0):
        RA+= 360

#  5b. right ascension value needs to be in the same quadrant as L
    Lquadrant  = (math.floor(L/90)) * 90
    RAquadrant = (math.floor(RA/90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

# 5c. right ascension degrees needs to be converted into hours
    RA = RA/15

# 6. calculate the Sun's declination
    sinDec = 0.39782 * sind(L)
    cosDec = math.cos(math.asin(sinDec))
    declin = degr(math.atan(sinDec/cosDec))
    dLT[2] = declin     # Save declination 

# 7a. calculate the Sun's local hour angle
#    latitude = lat1

    cosH = (cosd(zenith) - (sinDec*sind(lat1)))/(cosDec*cosd(lat1))
    if (cosH > 1):
        cosH = 1.0    # errors prohibited
        tkMessageBox.showinfo( "Alert", "Sun will not rise!")
        print "the sun never rises on this location (on the specified date)\n"

    if (cosH < -1):
        cosH = -1.0	# this will prevent error
        tkMessageBox.showinfo( "Alert", "Sun will not set!")

#  7b. finish calculating H and convert into hours   
    H = degr(math.acos(cosH)) # converted to degrees

#  if rising time is desired:
    if (suncalctype == "SUNRISE" ):
        H = 360 - H

        prtx = "Sunrise"
    else:
        prtx = "Sunset" 

#  degrees to hours:
    H = H/15

#  8. calculate local mean time of rising/setting
    T = H + RA - (0.06571*t) - 6.622

#  9. adjust back to UTC
    UT = (T - lngHour) % 24
        
# 10. convert UT value to local time zone of latitude/longitude
    localT = UT + localOffset

    if (suncalctype == "SUNRISE"):
        dLT[0] = localT   
    else:
        dLT[1] = localT

# If no sunrise it will give for sunrise and sunset the same times at noon plus daylength 0
    if ((H > 23.999) or (H < 0.001)):
        dLT[1] = dLT[0]
        localT = dLT[0]
 
    return human(localT)

# end of suncalc()


def ButtonClicked():
    s1 = E1.get()
    s2 = E2.get()
    s3 = E3.get()

    s10 = content10.get()
    nyear = int(s10)

    s11 = content11.get()
    nmonth = int(s11)

    s12 = content12.get()
    nday = int(s12)
    
    latitude  = float(s1)
    longitude = float(s2)
    tzone     = float(s3)

    s4 = ("%d-%d-%d" % (nyear, nmonth, nday))
    content4.set(s4)

    s5 = suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_official)
    content5.set(s5)

    s6 = suncalc(nyear, nmonth, nday, "SUNSET", latitude, longitude, tzone, znt_official)
    content6.set(s6)

# daylength, noontime and elevation
    deltas = (dLT[1] - dLT[0])
    content7.set(human(deltas))
    isnoont = (dLT[0] + 0.5*deltas)
    content8.set(human(isnoont))
    iselevation = ("%.2f deg" % (90 - latitude + dLT[2]))
    content9.set(iselevation)


# Main Begin
root = Tk()

root.geometry("350x300+200+200")
root.title("Suncalculator")

Label(root, text="Latitude", fg="red").grid(row=0, column=0)		# Latitude
Label(root, text="Longitude, TZ", fg="red").grid(row=1, column=0)	# Longitude & TZ
Label(root, text="Current date", fg="red").grid(row=2, column=0)	# current date
Label(root, text="Sunrise time", fg="red").grid(row=3, column=0)	# Sunrise time official
Label(root, text="Sunset time ", fg="red").grid(row=4, column=0)	# Sunset time
Label(root, text="Daylength   ", fg="red").grid(row=5, column=0)	# Daylength
Label(root, text="Noon time   ", fg="red").grid(row=6, column=0)	# Noontime
Label(root, text="Sun elevation", fg="red").grid(row=7, column=0)	# Sun elevation
Label(root, text="Calculation date", fg="red").grid(row=8, column=0)	# Calculation date

now = datetime.datetime.now()
nyear = now.year
nmonth = now.month
nday = now.day

latitude = 60.18; longitude = 24.93; tzone = 2.0

content = StringVar()
content.set("%.2f" % latitude)
E1 = Entry(root, textvariable=content, width=10)
E1.grid(row=0, column=1)

content2 = StringVar()
content2.set("%.2f" % longitude)
E2 = Entry(root, textvariable=content2, width=10)
E2.grid(row=1, column=1)

content3 = StringVar()
content3.set("%.1f" % tzone)
E3 = Entry(root, textvariable=content3, width=5)
E3.grid(row=1, column=2)

content4 = StringVar()
nyt = date.today()
s4 = nyt.isoformat()
content4.set(s4)
E4 = Entry(root, textvariable=content4, width=10)
E4.grid(row=2, column=1)

content5 = StringVar()
s5 = suncalc(nyear, nmonth, nday, "SUNRISE", latitude, longitude, tzone, znt_official)
content5.set(s5)
e5 = Entry(root, textvariable=content5, width=10)
e5.grid(row=3, column=1)

content6 = StringVar()
s6 = suncalc(nyear, nmonth, nday, "SUNSET", latitude, longitude, tzone, znt_official)
content6.set(s6)
e6 = Entry(root, textvariable=content6, width=10)
e6.grid(row=4, column=1)

# daylength, noontime and elevation
deltas = (dLT[1] - dLT[0])
isnoont = dLT[0] + 0.5*deltas
iselevation = ("%.2f deg" % (90 - latitude + dLT[2]))

content7 = StringVar()
e7 = Entry(root, textvariable=content7, width=10)
e7.grid(row=5, column=1)

content8 = StringVar()
e8 = Entry(root, textvariable=content8, width=10)
e8.grid(row=6, column=1)

content9 = StringVar()
e9 = Entry(root, textvariable=content9, width=10)
e9.grid(row=7, column=1)

content10 = StringVar()
s10 = ("%d" % nyear)
content10.set(s10)
e10 = Entry(root, textvariable=content10, width=6)
e10.grid(row=8, column=1)

content11 = StringVar()
s11 = ("%d" % nmonth)
content11.set(s11)
e11 = Entry(root, textvariable=content11, width=4)
e11.grid(row=8, column=2)

content12 = StringVar()
s12 = ("%d" % nday)
content12.set(s12)
e12 = Entry(root, textvariable=content12, width=4)
e12.grid(row=8, column=3)

button1 = Button(root, text="Calculate", command=ButtonClicked)
button1.grid(row=10, column=1)

root.mainloop()
