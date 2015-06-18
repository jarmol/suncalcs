#!/usr/bin/swift
import Foundation
// http://swiftstub.com/61178276/
let pi: Double = 3.1415926535897931
let fs = " %.5f " // output format decimals

// convert degrees to radians
func rad(x: Double) -> Double {
    return pi*x/180.0
}
// convert radians to degrees
func degr(x: Double) -> Double {
    return 180.0*x/pi
} 

// degree based trigonometric functions
func cosd(x: Double) -> Double {
    return cos(rad(x))
}
func sind(x: Double) -> Double {
    return sin(rad(x))
}

func tand(x: Double) -> Double {
    return tan(rad(x))
}

func atand(x: Double) -> Double {
    return degr(atan(x))
}

   func yday(Year: Int, Month: Int, Day: Int) ->Int {
               let N1 = Int(275*Month/9)
        let N2 = Int((Month + 9)/12)
        let N3 = (1 + Int((Year - 4*Int(Year/4) + 2)/3))
        let ydN = N1 - (N2 * N3) + Day - 30
        return ydN
   }

func dechrtohrmns(dechr: Double) -> String {
  let totalSeconds = Int(3600*dechr)
  let seconds = totalSeconds % 60
  let minutes = (totalSeconds / 60) % 60
  let hours = totalSeconds / 3600
  let c = String(format: "%02d:%02d:%02d", hours, minutes, seconds)
  return c
}

   
// Get current date and time
    let date = NSDate() 
    let calendar = NSCalendar.currentCalendar()

    let components = calendar.components(.CalendarUnitYear
    | .CalendarUnitMonth
    | .CalendarUnitDay
    | .CalendarUnitHour
    | .CalendarUnitMinute
    | .CalendarUnitSecond, fromDate: date)

    let hour = components.hour
    let minutes = components.minute
    let seconds = components.second
    var day = components.day
    var month = components.month
    let year = components.year
// Test: works until vernal equinox on 21 March
//  month = 3 ; day = 21   
    let daynr = yday(year, month, day)

//  Local current time
    println(String(format: "%02d.%02d.%4d ( day nr %3d ) %02d:%02d:%02d", day, month, year, daynr, hour, minutes, seconds))

class Location {

// Geographic locations
    let cityName: String
    let latitude: Double
    let longitude: Double
    let timeZone: Double
    
    init(cityName: String, latitude: Double, longitude: Double, timeZone: Double) { 
        self.cityName = cityName
        self.latitude = latitude 
        self.longitude = longitude
        self.timeZone = timeZone
    }
}
// Create location examples
let p1 = Location(cityName:"Helsinki", latitude:60.18, longitude:24.93, timeZone:2.0)
let p2 = Location(cityName:"Oulu", latitude:65.02, longitude:25.47, timeZone:2.0)
let p3 = Location(cityName:"Vancouver B.C.", latitude:49.217, longitude:-123.1, timeZone:-8.0)

class Solar {
// Solar calculations

    var dayNr: Int
    var Latitude: Double
    var Longitude: Double
    var Zenith: Double
    var Declination: Double
    var Timezone: Double
    var Whichway: String
    var p: Location

// Note, shortened list of arguments as the object argument p of class Location is used
    init(daynr: Int, p: Location, whichway: String, zenith: Double) {
        self.dayNr = daynr
        self.p = p
        self.Latitude =  p.latitude
        self.Longitude = p.longitude
        self.Whichway  = whichway
        self.Zenith    = zenith
        self.Timezone =  p.timeZone
        self.Declination = 0.0
    }

func doCalc() -> (UT: Double, localTime: Double) {
     if (self.Whichway == "SUNRISE") {
       println("\(p.cityName) Latitude \(Latitude), longitude \(Longitude), time zone \(Timezone)")  
    //   println("Day number \(dayNr)")
    }
// 2. convert longitude degrees to hours
//  and calculate an approximate times t1 and t2
    let lngHour = Longitude/15.0
    let t1 = Double(dayNr) + (6.0 - lngHour)/24.0
    let t2 = t1 + 0.5
    var t = t2
    
    if (self.Whichway == "SUNRISE") {
        t = t1
       }
//  3. calculate the Sun's mean anomaly
    let M = 0.9856*t - 3.289

// 4. calculate the Sun's true longitude
    var L = M + (1.916*sind(M)) + 0.020*sind(2*M) + 282.634

//  NOTE: L needs to be adjusted into the range [-360,360]
        if (L > 360.0) {L -= 360.0 }
        else if (L < -360.0) {L += 360.0 }

//  5a. calculate the Sun's right ascension
        var RA = atan(0.91764*tand(L))
        RA = degr(RA)
//  NOTE: RA needs to be adjusted into the range [-360,360]
        if (RA > 360.0) {
            RA -= 360.0 }
        else if (RA < -360.0) {
            RA += 360.0 }
//   5b. RA value needs to be in the same quadrant as L
        let Lquadrant  = (floor(L/90.0))*90.0
        let RAquadrant = (floor(RA/90.0))*90.0
        RA = RA + (Lquadrant - RAquadrant)
// 5c. right ascension degrees needs to be converted into hours
        RA = RA/15.0
        
// 6. calculate the Sun's declination
        var sinDec = 0.39782*sind(L)
        var cosDec = cos(asin(sinDec))
        var declin = degr(atan(sinDec/cosDec))
        Declination = declin     // Save declination

// 7a. calculate the Sun's local hour angle
	var sinH, cosH: Double
        cosH = (cosd(self.Zenith) - (sinDec*sind(self.Latitude)))/(cosDec*cosd(self.Latitude))
	sinH = sqrt(1.0 - cosH*cosH)

        if (cosH > 1) {
            cosH = 1.0    // errors prohibited
            println ("the sun never rises on this location!")
        }

        if (cosH < -1) {
            cosH = -1.0     // this will prevent error
            println ("Sun will not set!")
	}


//  7b. finish calculating H and convert into hours   
        var H = degr(acos(cosH)) // converted to degrees
//	var H = degr(asin(sinH))
	var prtx = "???"

//  if rising time is desired:
        if (self.Whichway == "SUNRISE" ) {
            H = 360.0 - H
            prtx = "Sunrise"
	}
        else { prtx = "Sunset" } 

//  degrees to hours:
        H = H/15.0

//  8. calculate local mean time of rising/setting
     let T = H + RA - (0.06571*t) - 6.622

//  9. adjust back to UTC
     var UT = (T - lngHour)
     if (UT < 0.0) { UT += 24.0 } // correct negative times since March equinox
     UT = UT % 24
 
     var localTime = UT + self.Timezone
     localTime = localTime % 24
     if localTime < 0 {localTime += 24}

//     println("UT = \(dechrtohrmns(UT))")
     println("Local " + prtx + " = \(dechrtohrmns(localTime))")
     return (UT, localTime)
    }
}   

func showMore(lt1: Double, lt2: Double, decl1: Double, decl2: Double, p: Location) {
    var noonTime = 0.5*(lt1 + lt2)
    var dayLength = lt2 - lt1
    if (lt2 < lt1) {
       dayLength += 24
       noonTime += 12 
    }

    var mdecl = 0.5*(decl1 + decl2)
    var maxelev = 90 - p.latitude + mdecl
    println("Noon time: \(dechrtohrmns(noonTime))")
    println(String(format: "Maxim sun elevation: %.2f", maxelev))
    println("Day length: \(dechrtohrmns(dayLength))")
    println(String(format: "Average sun declination: " + fs + "\n", mdecl))

}

let znt_official = 90.833 // Zenit for sunrise or sunset
var LT1, LT2, decl1, decl2, mdecl: Double

// Test of functions
var helsun = Solar(daynr:daynr, p:p1, whichway:"SUNRISE", zenith:znt_official)
var UL1 = helsun.doCalc()
LT1 = UL1.localTime
decl1 = helsun.Declination

helsun = Solar(daynr:daynr, p:p1, whichway:"SUNSET", zenith:znt_official)
var UL2 = helsun.doCalc()
LT2 = UL2.localTime

decl2 = helsun.Declination
showMore(LT1, LT2, decl1, decl2, p1)

var oulsun = Solar(daynr:daynr, p:p2, whichway:"SUNRISE", zenith:znt_official)
UL1 = oulsun.doCalc()
LT1 = UL1.localTime

decl1 = oulsun.Declination

oulsun = Solar(daynr:daynr, p:p2, whichway:"SUNSET", zenith:znt_official)
UL2 = oulsun.doCalc()
LT2 = UL2.localTime

decl2 = oulsun.Declination
showMore(LT1, LT2, decl1, decl2, p2)

var vancsun = Solar(daynr:daynr, p:p3, whichway:"SUNRISE", zenith:znt_official)
UL1 = vancsun.doCalc()
LT1 = UL1.localTime
decl1 = vancsun.Declination

vancsun = Solar(daynr:daynr, p:p3, whichway:"SUNSET", zenith:znt_official)
UL2 = vancsun.doCalc()
LT2 = UL2.localTime

decl2 = vancsun.Declination
showMore(LT1, LT2, decl1, decl2, p3)
