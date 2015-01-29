import datetime, time, math
from time import gmtime, strftime
from datetime import date

znt_official = 90.833

rad  = lambda x: math.pi*x/180.0
cosd = lambda x: math.cos(rad(x))
sind = lambda x: math.sin(rad(x))
tand = lambda x: math.tan(rad(x))
degr = lambda x: 180.0*x/math.pi

def chif(cval, yval, nval):
    if (cval):
        rval = yval
    else:
        rval = nval

    return rval

class Location(object):

# Geographic locations

    def __init__(self, city, latitude, longitude, timezone): 
        self.Cityname = city 
        self.Latitude = latitude 
        self.Longitude = longitude
        self.Timezone = timezone

    def getname(self): 
        return self.Cityname

    def getlatitude(self): 
        return self.Latitude

    def getlongitude(self): 
        return self.Longitude

    def gettimezone(self):
        return self.Timezone

    def printrecord(self):
        cityx = self.Cityname
        latx  = self.Latitude
        lonx  = self.Longitude
        tzx   = self.Timezone

        suflat = chif(latx < 0.0, 'S', 'N')
        suflon = chif(lonx < 0.0, 'W', 'E')
        pretz  = chif(tzx  < 0.0, '', '+')
        print("%s latitude %s %s longitude %s %s timezone UTC%s%d\n" % (cityx, abs(latx), suflat, abs(lonx), suflon, pretz, tzx))            

class Dates(object):

    def __init__(self, year, month, day):
        self.Year = year
        self.Month = month
        self.Day = day 

    def yday(self):
        N1 = math.floor(275*self.Month/9)
        N2 = math.floor((self.Month + 9)/12)
        N3 = (1 + math.floor((self.Year - 4*math.floor(self.Year/4) + 2)/3))
        ydN = N1 - (N2 * N3) + self.Day - 30
        return ydN

    def getdate(self):
        return ("%d.%d.%d" % (self.Day, self.Month, self.Year))

class Solar(object):

# Solar calculations
# Note, shortened list of arguments as the object argument p of class Location is used
    def __init__(self, daynr, p, whichway="SUNRISE", zenith=znt_official):
        self.Daynr = daynr
        self.Latitude =  p.Latitude
        self.Longitude = p.Longitude
        self.Whichway  = whichway
        self.Zenith    = zenith
        self.Timezone =  p.Timezone
        self.Declination = 0.0
        self.RiseLT = 24.0
        self.SetLT  = 0.0

    def getsolar(self):
        print("%s at daynr %d for zenith %.2f\n" % (self.Whichway, self.Daynr, self.Zenith))

#  2. convert the longitude to hour value and calculate an approximate time
    def suncalc(self):
        lngHour = self.Longitude/15.0 

        cond1 =(self.Whichway == "SUNRISE")
        t1 = self.Daynr + (6.0 - lngHour)/24.0
        t2 = t1 + 0.5
        t =  chif(cond1, t1, t2)

#  3. calculate the Sun's mean anomaly
        M = 0.9856*t - 3.289

#  4. calculate the Sun's true longitude
        L = M + (1.916*sind(M)) + 0.020*sind(2*M) + 282.634

#  NOTE: L needs to be adjusted into the range [-360,360]
 
        if (L > 360.0):
            L-= 360.0
        elif (L < -360.0):
            L+= 360.0 

#  5a. calculate the Sun's right ascension
        RA = math.atan(0.91764*tand(L))
        RA = degr(RA)

#  NOTE: RA needs to be adjusted into the range [-360,360]
        if (RA > 360.0):
            RA-= 360.0
        elif (RA < -360.0):
            RA+= 360.0

#  5b. right ascension value needs to be in the same quadrant as L
        Lquadrant  = (math.floor(L/90.0))*90.0
        RAquadrant = (math.floor(RA/90.0))*90.0
        RA = RA + (Lquadrant - RAquadrant)

# 5c. right ascension degrees needs to be converted into hours
        RA = RA/15.0

# 6. calculate the Sun's declination
        sinDec = 0.39782*sind(L)
        cosDec = math.cos(math.asin(sinDec))
        declin = degr(math.atan(sinDec/cosDec))
        self.Declination = declin     # Save declination

# 7a. calculate the Sun's local hour angle

        cosH = (cosd(self.Zenith) - (sinDec*sind(self.Latitude)))/(cosDec*cosd(self.Latitude))
        if (cosH > 1):
            cosH = 1.0    # errors prohibited
            print "the sun never rises on this location!\n"

        if (cosH < -1):
            cosH = -1.0     # this will prevent error
            print "Sun will not set!"

#  7b. finish calculating H and convert into hours   
        H = degr(math.acos(cosH)) # converted to degrees

#  if rising time is desired:
        if (self.Whichway == "SUNRISE" ):
            H = 360 - H

            prtx = "Sunrise"
        else:
            prtx = "Sunset" 

#  degrees to hours:
        H = H/15.0

#  8. calculate local mean time of rising/setting
        T = H + RA - (0.06571*t) - 6.622

#  9. adjust back to UTC
        UT = (T - lngHour) % 24
        
# 10. convert UT value to local time zone of latitude/longitude
        localT = UT + self.Timezone

        if (self.Whichway == "SUNRISE"):
            self.RiseLT = localT
        else:
            self.SetLT = localT

# If no sunrise it will give for sunrise and sunset the same times at noon plus daylength 0
        if ((H > 23.999) or (H < 0.001)):
            self.SetLT = self.RiseLT
            localT = self.RiseLT
 
        return human(localT)

# end of suncalc()

def human(decimhours):
# This function converts floating hours to formatted time hh:mm:ss
# Not embedded to any object
    h=decimhours        # floating hours
    s = 3600*h          # seconds
    ts = time.strftime('%H:%M:%S', time.gmtime(s))
    return ts

#def daylen(d1, d2):
#    dlhs = d2 - d1
#    return human(dlhs)

def daylen(pt1, pt2):
    d1 = pt1.RiseLT
    d2 = pt2.SetLT
    dlhs = d2 - d1
    return human(dlhs)

def noonts(pt1, pt2):
    d1 = pt1.RiseLT
    d2 = pt2.SetLT
    tnoon = human(d1 + 0.5*(d2 - d1))
    return tnoon 

def delivery(ps1, ps2):
    s1 = ps1.suncalc()
    s2 = ps2.suncalc()

    delta = daylen(ps1, ps2)
    tnoon = noonts(ps1, ps2)

    print ("Sunrise:   %s" % s1)
    print ("Sunset:    %s" % s2)
    print ("Noon time: %s" % tnoon)
    print ("Daylength: %s\n---------\n" % delta)
