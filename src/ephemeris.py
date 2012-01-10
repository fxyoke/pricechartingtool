
# For directory access.
import os
import sys
import inspect

# For copy.deepcopy()
import copy

# For datetimes
import datetime

# For math.floor()
import math

# For timezone conversion info.
import pytz

# For logging.
import logging
import logging.config

# Import the Swiss Ephemeris
import swisseph as swe

##############################################################################

# Directory where the swiss ephemeris files are located.
SWISS_EPHEMERIS_DATA_DIR = \
    os.path.abspath(os.path.join(sys.path[0], "../data/ephe"))

##############################################################################


class PlanetaryInfo:
    """Class that holds information about a planet's position, speed, etc.,
    for a given timestamp.

    The following is a list of data fields accessable through a fully populated
    PlanetaryInfo object.

    # Get info for the Sun.
    p = Ephemeris.getPlanetaryInfo("Sun", datetime.datetime.utcnow())

    # Data fields in 'p':
    p.name      = <Planet Name>
    p.id        = <Planet ID>
    p.dt        = <Timestamp for this planetary data, as a datetime.datetime with datetime.tzinfo>
    p.julianDay = <Timestamp for this planetary data, as a Julian Day integer in UTC>


    p.geocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.geocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.geocentric['tropical']['distance']        = <Distance (AU)>
    p.geocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.geocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.geocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.geocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.geocentric['tropical']['declination']         = <Declination (degrees)>
    p.geocentric['tropical']['distance']            = <Distance (AU)>
    p.geocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.geocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.geocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.geocentric['tropical']['X']  = <X location (AU)>
    p.geocentric['tropical']['Y']  = <Y location (AU)>
    p.geocentric['tropical']['Z']  = <Z location (AU)>
    p.geocentric['tropical']['dX'] = <X speed (AU/day)>
    p.geocentric['tropical']['dY'] = <Y speed (AU/day)>
    p.geocentric['tropical']['dZ'] = <Z speed (AU/day)>

    p.geocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.geocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.geocentric['sidereal']['distance']        = <Distance (AU)>
    p.geocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.geocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.geocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.geocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.geocentric['sidereal']['declination']         = <Declination (degrees)>
    p.geocentric['sidereal']['distance']            = <Distance (AU)>
    p.geocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.geocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.geocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.geocentric['sidereal']['X']  = <X location (AU)>
    p.geocentric['sidereal']['Y']  = <Y location (AU)>
    p.geocentric['sidereal']['Z']  = <Z location (AU)>
    p.geocentric['sidereal']['dX'] = <X speed (AU/day)>
    p.geocentric['sidereal']['dY'] = <Y speed (AU/day)>
    p.geocentric['sidereal']['dZ'] = <Z speed (AU/day)>


    p.topocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.topocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.topocentric['tropical']['distance']        = <Distance (AU)>
    p.topocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.topocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.topocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.topocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.topocentric['tropical']['declination']         = <Declination (degrees)>
    p.topocentric['tropical']['distance']            = <Distance (AU)>
    p.topocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.topocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.topocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.topocentric['tropical']['X']  = <X location (AU)>
    p.topocentric['tropical']['Y']  = <Y location (AU)>
    p.topocentric['tropical']['Z']  = <Z location (AU)>
    p.topocentric['tropical']['dX'] = <X speed (AU/day)>
    p.topocentric['tropical']['dY'] = <Y speed (AU/day)>
    p.topocentric['tropical']['dZ'] = <Z speed (AU/day)>

    p.topocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.topocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.topocentric['sidereal']['distance']        = <Distance (AU)>
    p.topocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.topocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.topocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.topocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.topocentric['sidereal']['declination']         = <Declination (degrees)>
    p.topocentric['sidereal']['distance']            = <Distance (AU)>
    p.topocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.topocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.topocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.topocentric['sidereal']['X']  = <X location (AU)>
    p.topocentric['sidereal']['Y']  = <Y location (AU)>
    p.topocentric['sidereal']['Z']  = <Z location (AU)>
    p.topocentric['sidereal']['dX'] = <X speed (AU/day)>
    p.topocentric['sidereal']['dY'] = <Y speed (AU/day)>
    p.topocentric['sidereal']['dZ'] = <Z speed (AU/day)>


    p.heliocentric['tropical']['longitude']       = <Longitude (degrees)>
    p.heliocentric['tropical']['latitude']        = <Latitude (degrees)>
    p.heliocentric['tropical']['distance']        = <Distance (AU)>
    p.heliocentric['tropical']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.heliocentric['tropical']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.heliocentric['tropical']['distance_speed']  = <Distance speed (AU/day)>
    p.heliocentric['tropical']['rectascension']       = <Rectascension (degrees)>
    p.heliocentric['tropical']['declination']         = <Declination (degrees)>
    p.heliocentric['tropical']['distance']            = <Distance (AU)>
    p.heliocentric['tropical']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.heliocentric['tropical']['declination_speed']   = <Latitude speed (degrees/day)>
    p.heliocentric['tropical']['distance_speed']      = <Distance speed (AU/day)>
    p.heliocentric['tropical']['X']  = <X location (AU)>
    p.heliocentric['tropical']['Y']  = <Y location (AU)>
    p.heliocentric['tropical']['Z']  = <Z location (AU)>
    p.heliocentric['tropical']['dX'] = <X speed (AU/day)>
    p.heliocentric['tropical']['dY'] = <Y speed (AU/day)>
    p.heliocentric['tropical']['dZ'] = <Z speed (AU/day)>

    p.heliocentric['sidereal']['longitude']       = <Longitude (degrees)>
    p.heliocentric['sidereal']['latitude']        = <Latitude (degrees)>
    p.heliocentric['sidereal']['distance']        = <Distance (AU)>
    p.heliocentric['sidereal']['longitude_speed'] = <Longitude speed (degrees/day)>
    p.heliocentric['sidereal']['latitude_speed']  = <Latitude speed (degrees/day)>
    p.heliocentric['sidereal']['distance_speed']  = <Distance speed (AU/day)>
    p.heliocentric['sidereal']['rectascension']       = <Rectascension (degrees)>
    p.heliocentric['sidereal']['declination']         = <Declination (degrees)>
    p.heliocentric['sidereal']['distance']            = <Distance (AU)>
    p.heliocentric['sidereal']['rectascension_speed'] = <Rectascension speed (degrees/day)>
    p.heliocentric['sidereal']['declination_speed']   = <Latitude speed (degrees/day)>
    p.heliocentric['sidereal']['distance_speed']      = <Distance speed (AU/day)>
    p.heliocentric['sidereal']['X']  = <X location (AU)>
    p.heliocentric['sidereal']['Y']  = <Y location (AU)>
    p.heliocentric['sidereal']['Z']  = <Z location (AU)>
    p.heliocentric['sidereal']['dX'] = <X speed (AU/day)>
    p.heliocentric['sidereal']['dY'] = <Y speed (AU/day)>
    p.heliocentric['sidereal']['dZ'] = <Z speed (AU/day)>
    """

    def __init__(self, planetName, planetId, dt, julianDay,
                 geocentricDict=None,
                 topocentricDict=None,
                 heliocentricDict=None):
        """Initializes the PlanetaryInfo class with the given parameters.
        
        Parameters are as follows:
        
        planetName - String holding the name of the planet.
        planetId   - Integer ID that represents the planet in the
                     Swiss Ephemeris.
        dt         - The datetime.datetime object that holds the timestamp for
                     which the planetary information and data is valid for.
        julianDay  - The float value that holds the timestamp for the
                     which the planetary information and data is valid
                     for.  This should be equivalent to the value in
                     'dt' converted to julian day.
        """
        
        self.name = planetName
        self.id = planetId
        self.dt = dt
        self.julianDay = julianDay
        self.geocentric = geocentricDict
        self.topocentric = topocentricDict
        self.heliocentric = heliocentricDict


    def __str__(self):
        """Returns a string representation of this object."""

        return self.toString()

    def toString(self):
        """Returns a string representation of this object."""

        formatStr = "[name={}, id={}, datetime={}, julianDay={}, " + \
                    "geocentric={}, topocentric={}, heliocentric={}]"

        returnStr = formatStr.format(self.name, 
                                     self.id, 
                                     Ephemeris.datetimeToStr(self.dt),
                                     self.julianDay,
                                     self.geocentric,
                                     self.topocentric,
                                     self.heliocentric)

        return returnStr


class Ephemeris:
    """Provides access to ephemeris data.  Please exercise caution when 
    using this class in multithreaded environments because the underlying
    implementation of swisseph is a simple C library and there is no way to
    make sure the internally stored data maintains its integrity
    across multiple threads.

    The recommended way to use this class:

    ############################

    # Initialize the class.  This only needs to be called once 
    # before being used.
    Ephemeris.initialize()

    # Set the geographic position (required).
    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Call the get function for the planet of interest.
    p = getVenusPlanetaryInfo(datetime.datetime.utcnow())

    # Extract the value(s) needed from teh PlanetaryInfo object.
    longitude = p.geocentric['tropical']['longitude']

    # Print values.
    print("Venus geocentric tropical longitude is: {}".format(longitude))

    # Close when all done.
    Ephemeris.closeEphemeris()

    #############################


    For more fine-grained control, the class can also be used by manually
    calling the individual set-flags functions and then calling calc_ut().
    """

    # Logger object for this class.
    log = logging.getLogger("ephemeris.Ephemeris")


    # Flag that is used in Swiss Ephemeris calculations.  
    # We make mods to this variable to add options.
    iflag = 0

    # Holds the longitude, latitude, and altitude representing the 
    # geographic positions to use in calculations of houses 
    # (and in topocentric calculations).
    #
    # Note: 
    # Positive longitude degrees refer to East, and 
    # negative longitude degrees refer to West.
    geoLongitudeDeg = 0
    geoLatitudeDeg = 0
    geoAltitudeMeters = 0
    
    # Dictionary for referencing various House Cusp Systems.
    HouseSys = { 'Placidus'      : b'P',
                 'Koch'          : b'K',
                 'Porphyry'      : b'O',
                 'Porphyrius'    : b'O',
                 'Sripathi'      : b'O',
                 'Regiomontanus' : b'R',
                 'Campanus'      : b'C',
                 'Equal'         : b'E',
                 'VehlowEqual'   : b'V',
                 'Whole'         : b'W',
                 'AxialRotationSystem' : b'X',
                 'Azimuthal'     : b'H',
                 'Horizontal'    : b'H',
                 'Polich'        : b'T',
                 'Page'          : b'T',
                 'Alcabitus'     : b'B',
                 'Morinus'       : b'M',
                 'KrusinskiPisa' : b'U',
                 'GauquelinSectors' : b'G'}

    @staticmethod
    def initialize():
        """Initializes the Ephemeris with default settings."""

        Ephemeris.log.debug("Entering initialize()")


        # Set up the swiss ephemeris data directory location.
        Ephemeris.log.info("Setting Ephemeris data directory to " +
                           SWISS_EPHEMERIS_DATA_DIR)
        swe.set_ephe_path(SWISS_EPHEMERIS_DATA_DIR)

        # Reset the iflag used.
        Ephemeris.iflag = 0

        # Use Swiss Ephemeris (and not JPL or Moshier)
        Ephemeris.log.info("Setting flag to use Swiss Ephemeris")
        Ephemeris.iflag |= swe.FLG_SWIEPH

        # Calculate speeds when doing calculations.
        Ephemeris.log.info("Setting flag to calculate speeds")
        Ephemeris.iflag |= swe.FLG_SPEED

        # Use true positions of the planets by default.
        Ephemeris.log.info("Setting to use true planetary positions")
        Ephemeris.setTruePlanetaryPositions()
        
    @staticmethod
    def closeEphemeris():
        """Does any cleanup needed to close the ephemeris.  
        Using the ephemeris after calling this yields undefined results.  
        """

        Ephemeris.log.debug("Entered closeEphemeris()")

        # Call close on the Swiss Ephemeris so it can cleanup files and
        # deallocate memory, etc.
        swe.close()

        Ephemeris.log.debug("Exiting closeEphemeris()")

    @staticmethod
    def setGeographicPosition(geoLongitudeDeg, 
                              geoLatitudeDeg, 
                              altitudeMeters=0.0):
        """Sets the position for planetary calculations.

        Parameters:
        geoLongitudeDeg - Longitude in degrees.  
                          West longitudes are negative,
                          East longitudes are positive.
                          Value should be in the range of -180 to 180.
        geoLatitudeDeg  - Latitude in degrees.  North latitudes are positive, 
                          south latitudes are negative.  
                          Value should be in the range of -90 to 90.
        altitudeMeters  - Altitude in meters.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr = "Entering setGeographicPosition(lon={}, lat={}, alt={})"
            Ephemeris.log.debug(debugStr.format(geoLongitudeDeg, 
                                                geoLatitudeDeg,
                                                altitudeMeters))

        if geoLongitudeDeg < -180 or geoLongitudeDeg > 180:
            Ephemeris.log.warn("Longitude specified was not between " + \
                               "-180 and 180.")
        if geoLatitudeDeg < -90 or geoLatitudeDeg > 90:
            Ephemeris.log.warn("Latitude specified was not between " + \
                               "-90 and 90.")

        # Set the topo values for use in topo calculations.
        swe.set_topo(geoLatitudeDeg, geoLatitudeDeg, altitudeMeters)

        # Save off the values for future use (when getting house positions).
        Ephemeris.geoLongitudeDeg = geoLongitudeDeg
        Ephemeris.geoLatitudeDeg = geoLatitudeDeg
        Ephemeris.geoAltitudeMeters = altitudeMeters

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            infoStr = "Setting geographic location to: " + \
                      "(lon={}, lat={}, alt={})".\
                      format(Ephemeris.geoLongitudeDeg,
                             Ephemeris.geoLatitudeDeg,
                             Ephemeris.geoAltitudeMeters)
            Ephemeris.log.debug(infoStr)

            Ephemeris.log.debug("Exiting setGeographicPosition()")


    @staticmethod
    def datetimeToJulianDay(dt):
        """Utility function for converting a datetime.datetime object 
        to Julian Day.  
        
        Parameters:
        
        dt - A datetime.datetime object with the 'tzinfo' attribute set
        as a pytz-created datetime.tzinfo.  
        
        The tzinfo attribute needing to be set to a pytz-created
        datetime.tzinfo is to allow us to normalize for 
        changes in the timezone properly.  The conversion process 
        to a Julian Day utilizes the Swiss Ephemeris.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering datetimeToJulianDay({})".format(dt))

        # Error checking of the input datetime object.
        if (dt.tzinfo == None):
            errStr = "Ephemeris.datetimeToJulianDay(): tzinfo attribute " + \
                "in the datetime.datetime cannot be None"
            raise ValueError(errStr)

        # Convert to UTC.
        dtUtc = pytz.utc.normalize(dt.astimezone(pytz.utc))

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("datetime converted to UTC is: {}".format(dtUtc))

        # Get the Julian Day as calculated by Swiss Ephemeris.
        cal = swe.GREG_CAL
        (jd_et, jd_ut) = \
                swe.utc_to_jd(dtUtc.year, dtUtc.month, dtUtc.day, 
                              dtUtc.hour, dtUtc.minute, dtUtc.second,
                              cal)

        # We use the Julian Day for Universal Time (UT).
        jd = jd_ut
        
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr = "Swiss Ephemeris converted UTC datetime({}) to " + \
                       "jd_et={}, jd_ut={}.  Using jd_ut as julian day."
            Ephemeris.log.debug(debugStr.format(dtUtc, jd_et, jd_ut))

            Ephemeris.log.debug("Exiting datetimeToJulianDay() and " + \
                                "returning {}".format(jd))
        return jd


    @staticmethod
    def julianDayToDatetime(jd, tzInfo=pytz.utc):
        """Utility function for converting a Julian Day number to 
        a datetime.datetime object.  The returned datetime object is created 
        with the timestamp in the timezone specified (or UTC by default if the
        argument is not specified).
        
        This conversion process utilizes the Swiss Ephemeris to 
        do the conversion and calculation.
        """
        
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering julianDayToDatetime({}, {})".\
                                format(jd, tzInfo))

        gregFlag = 1
        (year, month, day, hour, mins, secs) = swe.jdut1_to_utc(jd, gregFlag)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr = "Got converted values from Swiss Ephemeris: " + \
                       "year={}, month={}, day={}, hour={}, mins={}, secs={}"
            Ephemeris.log.debug(debugStr.\
                                format(year, month, day, hour, mins, secs))

        # Make sure seconds is in a valid range.
        if secs < 0:
            secs = 0
        elif secs >= 60:
            secs = 59.999999

        # Here we need to convert a float seconds to an integer seconds 
        # plus a integer microseconds.
        secsTruncated = int(math.floor(secs))
        usecs = int(round((secs - secsTruncated) * 1000000))
        if usecs > 999999:
            usecs = 999999
            
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("secs={}, secsTruncated={}, usecs={}".\
                                format(secs, secsTruncated, usecs))

        # Make sure the year is within the min and max year range.
        if year < datetime.MINYEAR:
            raise ValueError("Year value '{}'".format(year) +
                             "is less than datetime.MINYEAR value " +
                             "{}.".format(datetime.MINYEAR))
        elif year > datetime.MAXYEAR:
            raise ValueError("Year value '{}'".format(year) +
                             "is greater than datetime.MAXYEAR value " +
                             "{}.".format(datetime.MAXYEAR))

        # Create a datetime.datetime in UTC.
        dtUtc = datetime.datetime(year, month, day, hour, mins, 
                                      secsTruncated, usecs, pytz.utc)

        # Convert to the timezone specified.
        dt = tzInfo.normalize(dtUtc.astimezone(tzInfo))

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Returning julian day converted from " + \
                                "jd={} to datetime={}".format(jd, dt))

        return dt

    @staticmethod
    def datetimeToStr(datetimeObj):
        """Returns a string representation of a datetime.datetime object.
        Normally we wouldn't need to do this, but the datetime.strftime()
        does not work on years less than 1900. 

        Arguments:
        datetimeObj - datetime.datetime object with a tzinfo defined.

        Returns:
        String holding the info about the datetime.datetime object, in 
        the datetime.strftime() format:  "%Y-%m-%d %H:%M:%S.%f %Z%z"
        """

        # Timezone name string, extracted from datetime.tzname().
        # This accounts for the fact that datetime.tzname() can return None.
        tznameStr = datetimeObj.tzname()
        if tznameStr == None:
            tznameStr = ""

        # Return the formatted string.
        return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}.{:06} {}{}".\
            format(datetimeObj.year,
                   datetimeObj.month,
                   datetimeObj.day,
                   datetimeObj.hour,
                   datetimeObj.minute,
                   datetimeObj.second,
                   datetimeObj.microsecond,
                   tznameStr,
                   Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj))


    @staticmethod
    def datetimeToDayStr(datetimeObj):
        """Returns a string representation of a datetime.datetime
        object with the day of the week included.  Normally we
        wouldn't need to do this, but the datetime.strftime() does not
        work on years less than 1900.

        Arguments:
        datetimeObj - datetime.datetime object with a tzinfo defined.

        Returns:
        String holding the info about the datetime.datetime object, in 
        the format:  "Day %Y-%m-%d %H:%M:%S %Z%z", where 'Day' is the
        three-letter abbreviation for the day of the week.
        """

        # Timezone name string, extracted from datetime.tzname().
        # This accounts for the fact that datetime.tzname() can return None.
        tznameStr = datetimeObj.tzname()
        if tznameStr == None:
            tznameStr = ""

        dayOfWeekStr = datetimeObj.ctime()[0:3]
        
        offsetStr = \
            Ephemeris.getTimezoneOffsetFromDatetime(datetimeObj)
            
        # Return value.
        rv = "{} {}-{:02}-{:02} {:02}:{:02}:{:02} {}{}".\
             format(dayOfWeekStr,
                    datetimeObj.year,
                    datetimeObj.month,
                    datetimeObj.day,
                    datetimeObj.hour,
                    datetimeObj.minute,
                    datetimeObj.second,
                    tznameStr,
                    offsetStr)
            
        return rv
        
    @staticmethod
    def getTimezoneOffsetFromDatetime(datetimeObj):
        """Extracts the string that holds the time offset from UTC from 
        the given datetime object.  This is the string that would be 
        outputted from a call to datetime.strftime("%z"), in the format 
        that is the exact same (e.g., "+0230", "-0500", etc.).   
        We have to extract this information manually because 
        datetime.strftime() raises a ValueError exception if the year 
        in the datetime object is less than 1900.

        Arguments: 
        datetimeObj - datetime.datetime object with a tzinfo defined.

        Returns:
        str holding the time offset from UTC.
        """

        offsetStr = ""

        timeDelta = datetimeObj.utcoffset()
        offsetSeconds = (timeDelta.days * (24 * 60 * 60)) + timeDelta.seconds

        if offsetSeconds < 0:
            offsetStr += "-"
        else:
            offsetStr += "+"

        offsetHours = abs(offsetSeconds) // (60 * 60)
        offsetMinutes = (abs(offsetSeconds) - (offsetHours * 60 * 60)) // 60

        offsetStr += "{:02}".format(offsetHours)
        offsetStr += "{:02}".format(offsetMinutes)

        return offsetStr


    @staticmethod
    def getPlanetIdForName(planetName):
        """Returns the planet ID for the given planet name.  This
        planet ID is the is the int that is used in the Swiss
        Ephemeris to specify a planet.  If a planet ID is not found
        for the given planet name, then None is returned.
        
        Arguments:
        planetName - str value for the name of the planet.

        Returns:
        int value for the planet ID.  If a planet ID could not be
        found for the given planet name, then None is returned.
        """

        rv = None
        
        if planetName == "Sun":
            rv = swe.SUN
        elif planetName == "Moon":
            rv = swe.MOON
        elif planetName == "Mercury":
            rv = swe.MERCURY
        elif planetName == "Venus":
            rv = swe.VENUS
        elif planetName == "Mars":
            rv = swe.MARS
        elif planetName == "Jupiter":
            rv = swe.JUPITER
        elif planetName == "Saturn":
            rv = swe.SATURN
        elif planetName == "Uranus":
            rv = swe.URANUS
        elif planetName == "Neptune":
            rv = swe.NEPTUNE
        elif planetName == "Pluto":
            rv = swe.PLUTO
        elif planetName == "MeanNorthNode":
            rv = swe.MEAN_NODE
        elif planetName == "TrueNorthNode":
            rv = swe.TRUE_NODE
        elif planetName == "MeanLunarApogee":
            rv = swe.MEAN_APOG
        elif planetName == "OsculatingLunarApogee":
            rv = swe.OSCU_APOG
        elif planetName == "InterpolatedLunarApogee":
            rv = swe.INTP_APOG
        elif planetName == "InterpolatedLunarPerigee":
            rv = swe.INTP_PERG
        elif planetName == "Earth":
            rv = swe.EARTH
        elif planetName == "Chiron":
            rv = swe.CHIRON
        elif planetName == "Pholus":
            rv = swe.PHOLUS
        elif planetName == "Ceres":
            rv = swe.CERES
        elif planetName == "Pallas":
            rv = swe.PALLAS
        elif planetName == "Juno":
            rv = swe.JUNO
        elif planetName == "Vesta":
            rv = swe.VESTA
        else:
            rv = None

        return rv
            
    @staticmethod
    def getPlanetNameForId(planetId):
        """Returns the string representation of a planet name for the given
        planet ID.

        Parameters:
        planetId - int value that maps to a planet ID in the Swiss Ephemeris.
        """

        # Use the Swiss Ephemeris call to get the planet name.
        planetName = swe.get_planet_name(planetId)

        # Do a bit of cleanup of some of the planet names (if it's one of the
        # following planets).
        if planetName == "mean Node":
            planetName = "MeanNorthNode"
        elif planetName == "true Node":
            planetName = "TrueNorthNode"
        elif planetName == "mean Apogee":
            planetName = "MeanLunarApogee"
        elif planetName == "osc. Apogee":
            planetName = "OsculatingLunarApogee"
        elif planetName == "intp. Apogee":
            planetName = "InterpolatedLunarApogee"
        elif planetName == "intp. Perigee":
            planetName = "InterpolatedLunarPerigee"

        return planetName


    @staticmethod
    def setSiderealZodiac():
        """Initializes the settings to use the sidereal zodiac for
        calculations.  This function sets the Ayanamsa to use as Lahiri, as
        calculated in the Swiss Ephemeris.  It should be noted that the
        calculation done for the Lahiri Ayanamsa from the Swiss Ephemeris is
        not the most accurate, and can be off by approximately 2 arc minutes.
        There are better ways to calculate this Ayanamsa.  More details on this
        topic can be found at: 
        http://jyotish-blog.blogspot.com/2005/12/ayanamsha-in-jhora-702-vs-swiss.html
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering setSiderealZodiac()")
            Ephemeris.log.debug("swe.FLG_SIDEREAL == {}".format(swe.FLG_SIDEREAL))
            Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))

        Ephemeris.iflag |= swe.FLG_SIDEREAL

        swe.set_sid_mode(swe.SIDM_LAHIRI)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))
            Ephemeris.log.debug("Exiting setSiderealZodiac()")

    @staticmethod
    def setTropicalZodiac():
        """Initializes the settings to use the tropical zodiac for
        calculations
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering setTropicalZodiac()")
            Ephemeris.log.debug("swe.FLG_SIDEREAL == {}".format(swe.FLG_SIDEREAL))
            Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
            
        Ephemeris.iflag &= (~swe.FLG_SIDEREAL)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))
            Ephemeris.log.debug("Exiting setTropicalZodiac()")
        

    @staticmethod
    def setTruePlanetaryPositions():
        """Initializes the settings to use the true planetary positions"""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering setTruePlanetaryPositions()")
            Ephemeris.log.debug("swe.FLG_TRUEPOS == {}".format(swe.FLG_TRUEPOS))
            Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))

            
        Ephemeris.iflag |= swe.FLG_TRUEPOS

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))
            Ephemeris.log.debug("Exiting setTruePlanetaryPositions()")

    @staticmethod
    def setApparentPlanetaryPositions():
        """Initializes the settings to use the true planetary positions"""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering setApparentPlanetaryPositions()")
            Ephemeris.log.debug("swe.FLG_TRUEPOS == {}".format(swe.FLG_TRUEPOS))
            Ephemeris.log.debug("iflag before: {}".format(Ephemeris.iflag))
            
        Ephemeris.iflag &= (~swe.FLG_TRUEPOS)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("iflag after: {}".format(Ephemeris.iflag))
            Ephemeris.log.debug("Exiting setApparentPlanetaryPositions()")


    @staticmethod
    def createAveragedPlanetaryInfo(planetName, planetaryInfos):
        """Creates a new PlanetaryInfo object from the averages of all
        values in 'planetaryInfos'.  In the created PlanetaryInfo
        object, the 'id' field will be set to an invalid ID.

        Arguments:
        planetName     - Name of the new PlanetaryInfo to create.
        planetaryInfos - list of PlanetaryInfo objects that will be
                         used to create the new PlanetaryInfo object.
                         It is assumed that the 'dt' field is the same
                         value in all these PlanetaryInfo objects, and
                         the 'julianDay' field is the same value also.

        Returns:
        PlanetaryInfo object that represents the average of the given planets.
        """


        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entered createAveragedPlanetaryInfo()")
            Ephemeris.log.debug("planetName == {}".format(planetName))
            Ephemeris.log.debug("len(planetaryInfos) == {}".\
                                format(len(planetaryInfos)))

        # Check input arguments to make sure there is at least 1
        # PlanetaryInfo.
        numPIs = len(planetaryInfos)
        if numPIs == 0:
            functName = inspect.stack()[0][3]
            Ephemeris.log.warn("Passed an empty list of PlanetaryInfos to " + \
                               functName + "()")
            return None

        # Return value.
        rv = None
        
        for p in planetaryInfos:
            if rv == None:
                # First PlanetaryInfo in the list.  Just start off
                # with a copy.
                rv = copy.deepcopy(p)

                # Change the name and id fields.
                rv.name = planetName
                
                # Use an invalid planet ID.
                #
                # (Note: The number chosen has no meaning.
                # I couldn't use -1, because -1 stands for SE_ECL_NUT.
                # See documentation of the Swiss Ephemeris, in
                # file: pyswisseph-1.76.00-0/doc/swephprg.htm)
                #
                rv.id = -9999
                
            else:
                # Not the first PlanetaryInfo.  Just sum the field values.
                rv.geocentric['tropical']['longitude'] += \
                    p.geocentric['tropical']['longitude']
                rv.geocentric['tropical']['latitude'] += \
                    p.geocentric['tropical']['latitude']
                rv.geocentric['tropical']['distance'] += \
                    p.geocentric['tropical']['distance']
                rv.geocentric['tropical']['longitude_speed'] += \
                    p.geocentric['tropical']['longitude_speed']
                rv.geocentric['tropical']['latitude_speed'] += \
                    p.geocentric['tropical']['latitude_speed']
                rv.geocentric['tropical']['distance_speed'] += \
                    p.geocentric['tropical']['distance_speed']
                rv.geocentric['tropical']['rectascension'] += \
                    p.geocentric['tropical']['rectascension']
                rv.geocentric['tropical']['declination'] += \
                    p.geocentric['tropical']['declination']
                rv.geocentric['tropical']['distance'] += \
                    p.geocentric['tropical']['distance']
                rv.geocentric['tropical']['rectascension_speed'] += \
                    p.geocentric['tropical']['rectascension_speed']
                rv.geocentric['tropical']['declination_speed'] += \
                    p.geocentric['tropical']['declination_speed']
                rv.geocentric['tropical']['distance_speed'] += \
                    p.geocentric['tropical']['distance_speed']
                rv.geocentric['tropical']['X'] += \
                    p.geocentric['tropical']['X']
                rv.geocentric['tropical']['Y'] += \
                    p.geocentric['tropical']['Y']
                rv.geocentric['tropical']['Z'] += \
                    p.geocentric['tropical']['Z']
                rv.geocentric['tropical']['dX'] += \
                    p.geocentric['tropical']['dX']
                rv.geocentric['tropical']['dY'] += \
                    p.geocentric['tropical']['dY']
                rv.geocentric['tropical']['dZ'] += \
                    p.geocentric['tropical']['dZ']

                rv.geocentric['sidereal']['longitude'] += \
                    p.geocentric['sidereal']['longitude']
                rv.geocentric['sidereal']['latitude'] += \
                    p.geocentric['sidereal']['latitude']
                rv.geocentric['sidereal']['distance'] += \
                    p.geocentric['sidereal']['distance']
                rv.geocentric['sidereal']['longitude_speed'] += \
                    p.geocentric['sidereal']['longitude_speed']
                rv.geocentric['sidereal']['latitude_speed'] += \
                    p.geocentric['sidereal']['latitude_speed']
                rv.geocentric['sidereal']['distance_speed'] += \
                    p.geocentric['sidereal']['distance_speed']
                rv.geocentric['sidereal']['rectascension'] += \
                    p.geocentric['sidereal']['rectascension']
                rv.geocentric['sidereal']['declination'] += \
                    p.geocentric['sidereal']['declination']
                rv.geocentric['sidereal']['distance'] += \
                    p.geocentric['sidereal']['distance']
                rv.geocentric['sidereal']['rectascension_speed'] += \
                    p.geocentric['sidereal']['rectascension_speed']
                rv.geocentric['sidereal']['declination_speed'] += \
                    p.geocentric['sidereal']['declination_speed']
                rv.geocentric['sidereal']['distance_speed'] += \
                    p.geocentric['sidereal']['distance_speed']
                rv.geocentric['sidereal']['X'] += \
                    p.geocentric['sidereal']['X']
                rv.geocentric['sidereal']['Y'] += \
                    p.geocentric['sidereal']['Y']
                rv.geocentric['sidereal']['Z'] += \
                    p.geocentric['sidereal']['Z']
                rv.geocentric['sidereal']['dX'] += \
                    p.geocentric['sidereal']['dX']
                rv.geocentric['sidereal']['dY'] += \
                    p.geocentric['sidereal']['dY']
                rv.geocentric['sidereal']['dZ'] += \
                    p.geocentric['sidereal']['dZ']

                rv.topocentric['tropical']['longitude'] += \
                    p.topocentric['tropical']['longitude']
                rv.topocentric['tropical']['latitude'] += \
                    p.topocentric['tropical']['latitude']
                rv.topocentric['tropical']['distance'] += \
                    p.topocentric['tropical']['distance']
                rv.topocentric['tropical']['longitude_speed'] += \
                    p.topocentric['tropical']['longitude_speed']
                rv.topocentric['tropical']['latitude_speed'] += \
                    p.topocentric['tropical']['latitude_speed']
                rv.topocentric['tropical']['distance_speed'] += \
                    p.topocentric['tropical']['distance_speed']
                rv.topocentric['tropical']['rectascension'] += \
                    p.topocentric['tropical']['rectascension']
                rv.topocentric['tropical']['declination'] += \
                    p.topocentric['tropical']['declination']
                rv.topocentric['tropical']['distance'] += \
                    p.topocentric['tropical']['distance']
                rv.topocentric['tropical']['rectascension_speed'] += \
                    p.topocentric['tropical']['rectascension_speed']
                rv.topocentric['tropical']['declination_speed'] += \
                    p.topocentric['tropical']['declination_speed']
                rv.topocentric['tropical']['distance_speed'] += \
                    p.topocentric['tropical']['distance_speed']
                rv.topocentric['tropical']['X'] += \
                    p.topocentric['tropical']['X']
                rv.topocentric['tropical']['Y'] += \
                    p.topocentric['tropical']['Y']
                rv.topocentric['tropical']['Z'] += \
                    p.topocentric['tropical']['Z']
                rv.topocentric['tropical']['dX'] += \
                    p.topocentric['tropical']['dX']
                rv.topocentric['tropical']['dY'] += \
                    p.topocentric['tropical']['dY']
                rv.topocentric['tropical']['dZ'] += \
                    p.topocentric['tropical']['dZ']

                rv.topocentric['sidereal']['longitude'] += \
                    p.topocentric['sidereal']['longitude']
                rv.topocentric['sidereal']['latitude'] += \
                    p.topocentric['sidereal']['latitude']
                rv.topocentric['sidereal']['distance'] += \
                    p.topocentric['sidereal']['distance']
                rv.topocentric['sidereal']['longitude_speed'] += \
                    p.topocentric['sidereal']['longitude_speed']
                rv.topocentric['sidereal']['latitude_speed'] += \
                    p.topocentric['sidereal']['latitude_speed']
                rv.topocentric['sidereal']['distance_speed'] += \
                    p.topocentric['sidereal']['distance_speed']
                rv.topocentric['sidereal']['rectascension'] += \
                    p.topocentric['sidereal']['rectascension']
                rv.topocentric['sidereal']['declination'] += \
                    p.topocentric['sidereal']['declination']
                rv.topocentric['sidereal']['distance'] += \
                    p.topocentric['sidereal']['distance']
                rv.topocentric['sidereal']['rectascension_speed'] += \
                    p.topocentric['sidereal']['rectascension_speed']
                rv.topocentric['sidereal']['declination_speed'] += \
                    p.topocentric['sidereal']['declination_speed']
                rv.topocentric['sidereal']['distance_speed'] += \
                    p.topocentric['sidereal']['distance_speed']
                rv.topocentric['sidereal']['X'] += \
                    p.topocentric['sidereal']['X']
                rv.topocentric['sidereal']['Y'] += \
                    p.topocentric['sidereal']['Y']
                rv.topocentric['sidereal']['Z'] += \
                    p.topocentric['sidereal']['Z']
                rv.topocentric['sidereal']['dX'] += \
                    p.topocentric['sidereal']['dX']
                rv.topocentric['sidereal']['dY'] += \
                    p.topocentric['sidereal']['dY']
                rv.topocentric['sidereal']['dZ'] += \
                    p.topocentric['sidereal']['dZ']

                rv.heliocentric['tropical']['longitude'] += \
                    p.heliocentric['tropical']['longitude']
                rv.heliocentric['tropical']['latitude'] += \
                    p.heliocentric['tropical']['latitude']
                rv.heliocentric['tropical']['distance'] += \
                    p.heliocentric['tropical']['distance']
                rv.heliocentric['tropical']['longitude_speed'] += \
                    p.heliocentric['tropical']['longitude_speed']
                rv.heliocentric['tropical']['latitude_speed'] += \
                    p.heliocentric['tropical']['latitude_speed']
                rv.heliocentric['tropical']['distance_speed'] += \
                    p.heliocentric['tropical']['distance_speed']
                rv.heliocentric['tropical']['rectascension'] += \
                    p.heliocentric['tropical']['rectascension']
                rv.heliocentric['tropical']['declination'] += \
                    p.heliocentric['tropical']['declination']
                rv.heliocentric['tropical']['distance'] += \
                    p.heliocentric['tropical']['distance']
                rv.heliocentric['tropical']['rectascension_speed'] += \
                    p.heliocentric['tropical']['rectascension_speed']
                rv.heliocentric['tropical']['declination_speed'] += \
                    p.heliocentric['tropical']['declination_speed']
                rv.heliocentric['tropical']['distance_speed'] += \
                    p.heliocentric['tropical']['distance_speed']
                rv.heliocentric['tropical']['X'] += \
                    p.heliocentric['tropical']['X']
                rv.heliocentric['tropical']['Y'] += \
                    p.heliocentric['tropical']['Y']
                rv.heliocentric['tropical']['Z'] += \
                    p.heliocentric['tropical']['Z']
                rv.heliocentric['tropical']['dX'] += \
                    p.heliocentric['tropical']['dX']
                rv.heliocentric['tropical']['dY'] += \
                    p.heliocentric['tropical']['dY']
                rv.heliocentric['tropical']['dZ'] += \
                    p.heliocentric['tropical']['dZ']

                rv.heliocentric['sidereal']['longitude'] += \
                    p.heliocentric['sidereal']['longitude']
                rv.heliocentric['sidereal']['latitude'] += \
                    p.heliocentric['sidereal']['latitude']
                rv.heliocentric['sidereal']['distance'] += \
                    p.heliocentric['sidereal']['distance']
                rv.heliocentric['sidereal']['longitude_speed'] += \
                    p.heliocentric['sidereal']['longitude_speed']
                rv.heliocentric['sidereal']['latitude_speed'] += \
                    p.heliocentric['sidereal']['latitude_speed']
                rv.heliocentric['sidereal']['distance_speed'] += \
                    p.heliocentric['sidereal']['distance_speed']
                rv.heliocentric['sidereal']['rectascension'] += \
                    p.heliocentric['sidereal']['rectascension']
                rv.heliocentric['sidereal']['declination'] += \
                    p.heliocentric['sidereal']['declination']
                rv.heliocentric['sidereal']['distance'] += \
                    p.heliocentric['sidereal']['distance']
                rv.heliocentric['sidereal']['rectascension_speed'] += \
                    p.heliocentric['sidereal']['rectascension_speed']
                rv.heliocentric['sidereal']['declination_speed'] += \
                    p.heliocentric['sidereal']['declination_speed']
                rv.heliocentric['sidereal']['distance_speed'] += \
                    p.heliocentric['sidereal']['distance_speed']
                rv.heliocentric['sidereal']['X'] += \
                    p.heliocentric['sidereal']['X']
                rv.heliocentric['sidereal']['Y'] += \
                    p.heliocentric['sidereal']['Y']
                rv.heliocentric['sidereal']['Z'] += \
                    p.heliocentric['sidereal']['Z']
                rv.heliocentric['sidereal']['dX'] += \
                    p.heliocentric['sidereal']['dX']
                rv.heliocentric['sidereal']['dY'] += \
                    p.heliocentric['sidereal']['dY']
                rv.heliocentric['sidereal']['dZ'] += \
                    p.heliocentric['sidereal']['dZ']

        # Now 'rv' should be a PlanetaryInfo object with all fields
        # holding the sum of the field values from the given
        # PlanetaryInfo objects.  Here we will now divide to get the
        # average.
        rv.geocentric['tropical']['longitude'] /= numPIs
        rv.geocentric['tropical']['latitude'] /= numPIs
        rv.geocentric['tropical']['distance'] /= numPIs
        rv.geocentric['tropical']['longitude_speed'] /= numPIs
        rv.geocentric['tropical']['latitude_speed'] /= numPIs
        rv.geocentric['tropical']['distance_speed'] /= numPIs
        rv.geocentric['tropical']['rectascension'] /= numPIs
        rv.geocentric['tropical']['declination'] /= numPIs
        rv.geocentric['tropical']['distance'] /= numPIs
        rv.geocentric['tropical']['rectascension_speed'] /= numPIs
        rv.geocentric['tropical']['declination_speed'] /= numPIs
        rv.geocentric['tropical']['distance_speed'] /= numPIs
        rv.geocentric['tropical']['X'] /= numPIs
        rv.geocentric['tropical']['Y'] /= numPIs
        rv.geocentric['tropical']['Z'] /= numPIs
        rv.geocentric['tropical']['dX'] /= numPIs
        rv.geocentric['tropical']['dY'] /= numPIs
        rv.geocentric['tropical']['dZ'] /= numPIs

        rv.geocentric['sidereal']['longitude'] /= numPIs
        rv.geocentric['sidereal']['latitude'] /= numPIs
        rv.geocentric['sidereal']['distance'] /= numPIs
        rv.geocentric['sidereal']['longitude_speed'] /= numPIs
        rv.geocentric['sidereal']['latitude_speed'] /= numPIs
        rv.geocentric['sidereal']['distance_speed'] /= numPIs
        rv.geocentric['sidereal']['rectascension'] /= numPIs
        rv.geocentric['sidereal']['declination'] /= numPIs
        rv.geocentric['sidereal']['distance'] /= numPIs
        rv.geocentric['sidereal']['rectascension_speed'] /= numPIs
        rv.geocentric['sidereal']['declination_speed'] /= numPIs
        rv.geocentric['sidereal']['distance_speed'] /= numPIs
        rv.geocentric['sidereal']['X'] /= numPIs
        rv.geocentric['sidereal']['Y'] /= numPIs
        rv.geocentric['sidereal']['Z'] /= numPIs
        rv.geocentric['sidereal']['dX'] /= numPIs
        rv.geocentric['sidereal']['dY'] /= numPIs
        rv.geocentric['sidereal']['dZ'] /= numPIs

        rv.topocentric['tropical']['longitude'] /= numPIs
        rv.topocentric['tropical']['latitude'] /= numPIs
        rv.topocentric['tropical']['distance'] /= numPIs
        rv.topocentric['tropical']['longitude_speed'] /= numPIs
        rv.topocentric['tropical']['latitude_speed'] /= numPIs
        rv.topocentric['tropical']['distance_speed'] /= numPIs
        rv.topocentric['tropical']['rectascension'] /= numPIs
        rv.topocentric['tropical']['declination'] /= numPIs
        rv.topocentric['tropical']['distance'] /= numPIs
        rv.topocentric['tropical']['rectascension_speed'] /= numPIs
        rv.topocentric['tropical']['declination_speed'] /= numPIs
        rv.topocentric['tropical']['distance_speed'] /= numPIs
        rv.topocentric['tropical']['X'] /= numPIs
        rv.topocentric['tropical']['Y'] /= numPIs
        rv.topocentric['tropical']['Z'] /= numPIs
        rv.topocentric['tropical']['dX'] /= numPIs
        rv.topocentric['tropical']['dY'] /= numPIs
        rv.topocentric['tropical']['dZ'] /= numPIs

        rv.topocentric['sidereal']['longitude'] /= numPIs
        rv.topocentric['sidereal']['latitude'] /= numPIs
        rv.topocentric['sidereal']['distance'] /= numPIs
        rv.topocentric['sidereal']['longitude_speed'] /= numPIs
        rv.topocentric['sidereal']['latitude_speed'] /= numPIs
        rv.topocentric['sidereal']['distance_speed'] /= numPIs
        rv.topocentric['sidereal']['rectascension'] /= numPIs
        rv.topocentric['sidereal']['declination'] /= numPIs
        rv.topocentric['sidereal']['distance'] /= numPIs
        rv.topocentric['sidereal']['rectascension_speed'] /= numPIs
        rv.topocentric['sidereal']['declination_speed'] /= numPIs
        rv.topocentric['sidereal']['distance_speed'] /= numPIs
        rv.topocentric['sidereal']['X'] /= numPIs
        rv.topocentric['sidereal']['Y'] /= numPIs
        rv.topocentric['sidereal']['Z'] /= numPIs
        rv.topocentric['sidereal']['dX'] /= numPIs
        rv.topocentric['sidereal']['dY'] /= numPIs
        rv.topocentric['sidereal']['dZ'] /= numPIs

        rv.heliocentric['tropical']['longitude'] /= numPIs
        rv.heliocentric['tropical']['latitude'] /= numPIs
        rv.heliocentric['tropical']['distance'] /= numPIs
        rv.heliocentric['tropical']['longitude_speed'] /= numPIs
        rv.heliocentric['tropical']['latitude_speed'] /= numPIs
        rv.heliocentric['tropical']['distance_speed'] /= numPIs
        rv.heliocentric['tropical']['rectascension'] /= numPIs
        rv.heliocentric['tropical']['declination'] /= numPIs
        rv.heliocentric['tropical']['distance'] /= numPIs
        rv.heliocentric['tropical']['rectascension_speed'] /= numPIs
        rv.heliocentric['tropical']['declination_speed'] /= numPIs
        rv.heliocentric['tropical']['distance_speed'] /= numPIs
        rv.heliocentric['tropical']['X'] /= numPIs
        rv.heliocentric['tropical']['Y'] /= numPIs
        rv.heliocentric['tropical']['Z'] /= numPIs
        rv.heliocentric['tropical']['dX'] /= numPIs
        rv.heliocentric['tropical']['dY'] /= numPIs
        rv.heliocentric['tropical']['dZ'] /= numPIs

        rv.heliocentric['sidereal']['longitude'] /= numPIs
        rv.heliocentric['sidereal']['latitude'] /= numPIs
        rv.heliocentric['sidereal']['distance'] /= numPIs
        rv.heliocentric['sidereal']['longitude_speed'] /= numPIs
        rv.heliocentric['sidereal']['latitude_speed'] /= numPIs
        rv.heliocentric['sidereal']['distance_speed'] /= numPIs
        rv.heliocentric['sidereal']['rectascension'] /= numPIs
        rv.heliocentric['sidereal']['declination'] /= numPIs
        rv.heliocentric['sidereal']['distance'] /= numPIs
        rv.heliocentric['sidereal']['rectascension_speed'] /= numPIs
        rv.heliocentric['sidereal']['declination_speed'] /= numPIs
        rv.heliocentric['sidereal']['distance_speed'] /= numPIs
        rv.heliocentric['sidereal']['X'] /= numPIs
        rv.heliocentric['sidereal']['Y'] /= numPIs
        rv.heliocentric['sidereal']['Z'] /= numPIs
        rv.heliocentric['sidereal']['dX'] /= numPIs
        rv.heliocentric['sidereal']['dY'] /= numPIs
        rv.heliocentric['sidereal']['dZ'] /= numPIs


        return rv
        
    @staticmethod
    def __clearCoordinateSystemFlags():
        """Private function that clears the flags for the coordinate position
        calculations.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr ="Clearing flags for different coordinate systems." 
            Ephemeris.log.debug(debugStr)

        Ephemeris.iflag &= (~swe.FLG_EQUATORIAL)
        Ephemeris.iflag &= (~swe.FLG_XYZ)
        Ephemeris.iflag &= (~swe.FLG_RADIANS)

    @staticmethod
    def setEclipticalCoordinateSystemFlag():
        """Sets the ephemeris to return results in ecliptical polar
        coordinates.  This is the default setting in Swiss Ephemeris and is
        equvalent to the flag cleared.  This causes swe_calc() and
        swe_calc_ut() to return the following values when it is called:
        (
         longitude in degrees, 
         latitude in degrees, 
         distance in AU,
         longitude speed in deg/day, 
         latitude speed in deg/day,
         speed in distance units AU/day
         )
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setEclipticalCoordinateSystemFlag()")
            
        # Just clear the coordinate system flags.  Ecliptical coordinates 
        # is the default, so we don't need to do anything more than just 
        # clear the flags. 
        Ephemeris.__clearCoordinateSystemFlags()

    @staticmethod
    def setEquatorialCoordinateSystemFlag():
        """Sets the ephemeris to return results in equatorial 
        coordinates.  This causes swe_calc() and swe_calc_ut() to return
        the following values when it is called:
        (
         Rectascension (degrees in Earth sky)
         Declination (degrees in Earth sky.  Range is: -90 to +90, where -90 is
                      south pole),
         Distance (units in AU),
         Speed in rectascension (deg/day),
         Speed in declination (deg/day),
         Speed in distance (AU/day)
         )
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setEquatorialCoordinateSystemFlag()")
            
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_EQUATORIAL

    @staticmethod
    def setRectangularCoordinateSystemFlag():
        """Sets the ephemeris to return results in XYZ coordinates.
        This causes swe_calc() and swe_calc_ut() to return the following values
        when it is called:
        (
        X (units in AU),
        Y (units in AU),
        Z (units in AU),
        dX (units in AU/day),
        dY (units in AU/day),
        dZ (units in AU/day)
        )
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setRectangularCoordinateSystemFlag()")
            
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_XYZ

    @staticmethod
    def setRadiansCoordinateSystemFlag():
        """Sets the ephemeris to return results in radians coordinates"""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setRadiansCoordinateSystemFlag()")
            
        Ephemeris.__clearCoordinateSystemFlags()
        Ephemeris.iflag |= swe.FLG_RADIANS

    @staticmethod
    def unsetRadiansCoordinateSystemFlag():
        """Unsets the ephemeris from returning results in radians
        coordinates.  Future calls to swe_calc() and swe_calc_ut() will 
        return values in degrees.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("unsetRadiansCoordinateSystemFlag()")
            
        Ephemeris.iflag &= (~swe.FLG_RADIANS)

    @staticmethod
    def setHeliocentricCalculations():
        """Sets the flag to do heliocentric calculations."""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setHeliocentricCalculations()")
            
        Ephemeris.iflag &= (~swe.FLG_TOPOCTR)
        Ephemeris.iflag |= swe.FLG_HELCTR
        
    @staticmethod
    def setGeocentricCalculations():
        """Sets the flag to do geocentric calculations."""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setGeocentricCalculations()")
            
        Ephemeris.iflag &= (~swe.FLG_HELCTR)
        Ephemeris.iflag &= (~swe.FLG_TOPOCTR)
        
    @staticmethod
    def setTopocentricCalculations():
        """Sets the flag to do topocentric calculations."""

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("setTopocentricCalculations()")
            
        Ephemeris.iflag &= (~swe.FLG_HELCTR)
        Ephemeris.iflag |= swe.FLG_TOPOCTR

    @staticmethod
    def calc_ut(jd, planet, flag=swe.FLG_SWIEPH+swe.FLG_SPEED):
        """Wrapper for the Swiss Ephemeris call calc_ut().
        Parameters and return values are the same as they are for calc_ut().
        This is added to enhance debugging.  
        
        Return value:
        Returns a tuple of 6 floats.
        
        Parameters are the same as they are to calc_ut():
        jd - Float value for the Julian Day
        planet - Integer value for the planet to do the calculation for.
        flag - Integer for what flags to use in the calculation.
        """
        
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering calc_ut(jd={}, planet={}, flag={})".\
                                format(jd, planet, flag))

        # Do the calculation.
        (arg1, arg2, arg3, arg4, arg5, arg6) = swe.calc_ut(jd, planet, flag)

        # Log some debug for the calculations and parameters.
        if (Ephemeris.log.isEnabledFor(logging.DEBUG)):
            Ephemeris.__logDebugCalcUTInfo(jd, planet, flag, 
                                           arg1, arg2, arg3, arg4, arg5, arg6)
        
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Exiting calc_ut(jd={}, planet={}, flag={})".\
                                format(jd, planet, flag))

        # Return calculated values.
        return (arg1, arg2, arg3, arg4, arg5, arg6)

    @staticmethod
    def swe_houses_ex(jd, 
                      geoLatitudeDeg, 
                      geoLongitudeDeg,
                      houseSystem=b"O", 
                      flag=swe.FLG_SIDEREAL):
        """Wrapper for the Swiss Ephemeris call swe_houses_ex().

        Return value:

        Tuple containing two tuples of 12 and 8 floats as follows:

        cusps[0] = House 1 cusp
        cusps[1] = House 2 cusp
        cusps[2] = House 3 cusp
        cusps[3] = House 4 cusp
        cusps[4] = House 5 cusp
        cusps[5] = House 6 cusp
        cusps[6] = House 7 cusp
        cusps[7] = House 8 cusp
        cusps[8] = House 9 cusp
        cusps[9] = House 10 cusp
        cusps[10] = House 11 cusp
        cusps[11] = House 12 cusp

        ascmc[0] = Ascendant
        ascmc[1] = MC
        ascmc[2] = ARMC
        ascmc[3] = Vertex
        ascmc[4] = "Equatorial ascendant"
        ascmc[5] = "Co-ascendant" (Walter Koch)
        ascmc[6] = "Co-ascendant" (Michael Munkasey)
        ascmc[7] = "Polar ascendant" (M. Munkasey)
        

        Parameters:
        jd - float value for the Julian Day, UT.
        geoLongitudeDeg - Longitude in degrees.  
                          West longitudes are negative,
                          East longitudes are positive.
                          Value should be in the range of -180 to 180.
        geoLatitudeDeg  - Latitude in degrees.  North latitudes are positive, 
                          south latitudes are negative.  
                          Value should be in the range of -90 to 90.
        houseSystem - byte string of length 1, that is one of the letters:
                      PKORCAEVXHTBG.

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors
        flag - int value that is a bit flag.
               Flag is checked for an OR of any the following:
               - 0 
               - swe.FLG_SIDEREAL
               - swe.FLG_RADIANS
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Entering swe_houses_ex(" + \
                                "jd={}, ".format(jd) + \
                                "houseSystem={})".format(houseSystem))

        # Do the calculation.
        (cusps, ascmc) = \
            swe.houses_ex(jd, 
                          geoLatitudeDeg,
                          geoLongitudeDeg,
                          houseSystem,
                          flag)

        # Log some debug for the calculations and parameters.
        if (Ephemeris.log.isEnabledFor(logging.DEBUG)):
            Ephemeris.__logDebugSweHousesEx(jd, 
                                            geoLatitudeDeg,
                                            geoLongitudeDeg,
                                            houseSystem,
                                            flag,
                                            cusps,
                                            ascmc)
        
        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            Ephemeris.log.debug("Exiting swe_houses_ex(" + \
                                "jd={}, ".format(jd) + \
                                "houseSystem={})".format(houseSystem))

        # Return calculated values.
        return (cusps, ascmc)
        

    @staticmethod
    def __logDebugCalcUTInfo(jd, planet, flag, 
                             arg1, arg2, arg3, arg4, arg5, arg6):
        """Helper function that simply logs the parameters provided.
        These are the parameters provided to calc_ut() and returned 
        values from calc_ut().
        """
        
        # Only continue and log if the logging level is set to DEBUG.
        if (not Ephemeris.log.isEnabledFor(logging.DEBUG)):
            return

        debugStr = "calc_ut(): ----------------------------------------------"
        Ephemeris.log.debug(debugStr)
        Ephemeris.log.debug("calc_ut(): jd={}, planet={}, flag={}".\
                format(jd, planet, flag))

        Ephemeris.log.debug("calc_ut(): Julian day {} converts to UTC timestamp: {}".\
                format(jd, Ephemeris.julianDayToDatetime(jd)))

        Ephemeris.log.debug("calc_ut(): Planet {} converts to: {}".\
                format(planet, Ephemeris.getPlanetNameForId(planet)))

        Ephemeris.log.debug("calc_ut(): Flags that set are: ")
        
        if (Ephemeris.iflag & swe.FLG_JPLEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_JPLEPH")
        if (Ephemeris.iflag & swe.FLG_SWIEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_SWIEPH")
        if (Ephemeris.iflag & swe.FLG_MOSEPH):
            Ephemeris.log.debug("calc_ut():  - FLG_MOSEPH")
        if (Ephemeris.iflag & swe.FLG_HELCTR):
            Ephemeris.log.debug("calc_ut():  - FLG_HELCTR")
        if (Ephemeris.iflag & swe.FLG_TRUEPOS):
            Ephemeris.log.debug("calc_ut():  - FLG_TRUEPOS")
        if (Ephemeris.iflag & swe.FLG_SPEED):
            Ephemeris.log.debug("calc_ut():  - FLG_SPEED")
        if (Ephemeris.iflag & swe.FLG_EQUATORIAL):
            Ephemeris.log.debug("calc_ut():  - FLG_EQUATORIAL")
        if (Ephemeris.iflag & swe.FLG_XYZ):
            Ephemeris.log.debug("calc_ut():  - FLG_XYZ")
        if (Ephemeris.iflag & swe.FLG_RADIANS):
            Ephemeris.log.debug("calc_ut():  - FLG_RADIANS")
        if (Ephemeris.iflag & swe.FLG_TOPOCTR):
            Ephemeris.log.debug("calc_ut():  - FLG_TOPOCTR")
        if (Ephemeris.iflag & swe.FLG_SIDEREAL):
            Ephemeris.log.debug("calc_ut():  - FLG_SIDEREAL")

        Ephemeris.log.debug("calc_ut(): Calculated values:")
        if (Ephemeris.iflag & swe.FLG_EQUATORIAL):
            # Equatorial position calculated.
            # output here:
            debugStr = "calc_ut():  {:<36}{}"
            Ephemeris.log.debug(debugStr.\
                    format("Rectascension (deg):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Declination (deg):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Distance (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in rectascension (deg/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in declination (deg/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in distance (AU/day)", arg6))
        elif (Ephemeris.iflag & swe.FLG_XYZ): 
            # XYZ position calculated.
            debugStr = "calc_ut():  {:<15}{}"
            Ephemeris.log.debug(debugStr.\
                    format("X (AU):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Y (AU):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Z (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("dX (AU/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("dY (AU/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("dZ (AU/day):", arg6))
        else:
            # Ecliptic position calculated.
            debugStr = "calc_ut():  {:<32}{}"
            Ephemeris.log.debug(debugStr.\
                    format("Longitude (deg):", arg1))
            Ephemeris.log.debug(debugStr.\
                    format("Latitude (deg):", arg2))
            Ephemeris.log.debug(debugStr.\
                    format("Distance (AU):", arg3))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in longitude (deg/day):", arg4))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in latitude (deg/day):", arg5))
            Ephemeris.log.debug(debugStr.\
                    format("Speed in distance (AU/day):", arg6))
    
    @staticmethod
    def __logDebugSweHousesEx(jd, 
                              geoLatitudeDeg,
                              geoLongitudeDeg,
                              houseSystem,
                              flag,
                              cusps,
                              ascmc):
        """Helper function that simply logs the parameters provided.
        These are the parameters and return values from running
        swe_houses_ex().
        """

        # Only continue and log if the logging level is set to DEBUG.
        if (not Ephemeris.log.isEnabledFor(logging.DEBUG)):
            return
        
        prefix = "swe_house_ex(): "

        debugStr = prefix + "-----------------------------------------------"
        Ephemeris.log.debug(debugStr)

        Ephemeris.log.debug(prefix + \
                "jd={}, ".format(jd) + \
                "geoLatitudeDeg={}, ".format(geoLatitudeDeg) + \
                "geoLongitudeDeg={}, ".format(geoLongitudeDeg) + \
                "houseSystem={}, ".format(houseSystem) + \
                "flag={}".format(flag))

        # Output the flag set.
        if (flag & swe.FLG_JPLEPH):
            Ephemeris.log.debug(prefix + " - FLG_JPLEPH")
        if (flag & swe.FLG_SWIEPH):
            Ephemeris.log.debug(prefix + " - FLG_SWIEPH")
        if (flag & swe.FLG_MOSEPH):
            Ephemeris.log.debug(prefix + " - FLG_MOSEPH")
        if (flag & swe.FLG_HELCTR):
            Ephemeris.log.debug(prefix + " - FLG_HELCTR")
        if (flag & swe.FLG_TRUEPOS):
            Ephemeris.log.debug(prefix + " - FLG_TRUEPOS")
        if (flag & swe.FLG_SPEED):
            Ephemeris.log.debug(prefix + " - FLG_SPEED")
        if (flag & swe.FLG_EQUATORIAL):
            Ephemeris.log.debug(prefix + " - FLG_EQUATORIAL")
        if (flag & swe.FLG_XYZ):
            Ephemeris.log.debug(prefix + " - FLG_XYZ")
        if (flag & swe.FLG_RADIANS):
            Ephemeris.log.debug(prefix + " - FLG_RADIANS")
        if (flag & swe.FLG_TOPOCTR):
            Ephemeris.log.debug(prefix + " - FLG_TOPOCTR")
        if (flag & swe.FLG_SIDEREAL):
            Ephemeris.log.debug(prefix + " - FLG_SIDEREAL")

        # Output the values returned.
        Ephemeris.log.debug(prefix + " returns: ")

        # House cusps.
        for i in len(cusps):
            Ephemeris.log.debug(prefix + " cusps[{}]={}".format(i, cusps[i]))

        # Other miscellaneous cusps.
        Ephemeris.log.debug(prefix + " Ascendant={}".\
                format(ascmc[0]))
        Ephemeris.log.debug(prefix + " MC={}".\
                format(ascmc[1]))
        Ephemeris.log.debug(prefix + " ARMC={}".\
                format(ascmc[2]))
        Ephemeris.log.debug(prefix + " Vertex={}".\
                format(ascmc[3]))
        Ephemeris.log.debug(prefix + " Equatorial ascendant={}".\
                format(ascmc[4]))
        Ephemeris.log.debug(prefix + " Co-ascendant (W.Koch)={}".\
                format(ascmc[5]))
        Ephemeris.log.debug(prefix + " Co-ascendant (M. Munkasey)={}".\
                format(ascmc[6]))
        Ephemeris.log.debug(prefix + " Polar ascendant (M. Munkasey)={}".\
                format(ascmc[7]))

        
    @staticmethod
    def getHouseCusps(dt, houseSystem=HouseSys['Porphyry']):
        """Returns a list of floats that are the degree locations
        of the house cusps.  

        Preconditions: 

            Ephemeris.setGeographicPosition() has been called previously.

        Arguments:
        
        dt - datetime.datetime object that holds the timestamp for which
             you want to get the house cusps.

        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.  E.g.  
                      
                      cusps = \
                          Ephemeris.\
                              getHouseCusps(dt, Ephemeris.HouseSys['Koch'])
                      
        Return value: 

        Dictionary holding the house cusps in degrees.

        cusps['tropical'][0]  = float value for the 1st House cusp (degrees).
        cusps['tropical'][1]  = float value for the 2nd House cusp (degrees).
        cusps['tropical'][2]  = float value for the 3rd House cusp (degrees).
        cusps['tropical'][3]  = float value for the 4th House cusp (degrees).
        cusps['tropical'][4]  = float value for the 5th House cusp (degrees).
        cusps['tropical'][5]  = float value for the 6th House cusp (degrees).
        cusps['tropical'][6]  = float value for the 7th House cusp (degrees).
        cusps['tropical'][7]  = float value for the 8th House cusp (degrees).
        cusps['tropical'][8]  = float value for the 9th House cusp (degrees).
        cusps['tropical'][9]  = float value for the 10th House cusp (degrees).
        cusps['tropical'][10] = float value for the 11th House cusp (degrees).
        cusps['tropical'][11] = float value for the 12th House cusp (degrees).

        cusps['sidereal'][0]  = float value for the 1st House cusp (degrees).
        cusps['sidereal'][1]  = float value for the 2nd House cusp (degrees).
        cusps['sidereal'][2]  = float value for the 3rd House cusp (degrees).
        cusps['sidereal'][3]  = float value for the 4th House cusp (degrees).
        cusps['sidereal'][4]  = float value for the 5th House cusp (degrees).
        cusps['sidereal'][5]  = float value for the 6th House cusp (degrees).
        cusps['sidereal'][6]  = float value for the 7th House cusp (degrees).
        cusps['sidereal'][7]  = float value for the 8th House cusp (degrees).
        cusps['sidereal'][8]  = float value for the 9th House cusp (degrees).
        cusps['sidereal'][9]  = float value for the 10th House cusp (degrees).
        cusps['sidereal'][10] = float value for the 11th House cusp (degrees).
        cusps['sidereal'][11] = float value for the 12th House cusp (degrees).
        """

        # Validate input.
        validHouseSystems = list(Ephemeris.HouseSys.values())
        if houseSystem not in validHouseSystems:
            Ephemeris.log.error("getHouseCusps(): " + \
                "Invalid house system specified: {}".format(houseSystem))
            return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        # Convert datetime to julian day.
        jd = Ephemeris.datetimeToJulianDay(dt)

        # Get the house cusps in the tropical zodiac coordinates.
        Ephemeris.setTropicalZodiac()
        Ephemeris.unsetRadiansCoordinateSystemFlag()

        # Obtain the house cusps.
        (tropicalCusps, tropicalAscmc) = \
            Ephemeris.swe_houses_ex(jd, 
                                    Ephemeris.geoLatitudeDeg, 
                                    Ephemeris.geoLongitudeDeg,
                                    houseSystem,
                                    Ephemeris.iflag)

        # Get the house cusps in the sidereal zodiac coordinates.
        Ephemeris.setSiderealZodiac()
        Ephemeris.unsetRadiansCoordinateSystemFlag()

        # Obtain the house cusps.
        (siderealCusps, siderealAscmc) = \
            Ephemeris.swe_houses_ex(jd, 
                                    Ephemeris.geoLatitudeDeg, 
                                    Ephemeris.geoLongitudeDeg,
                                    houseSystem,
                                    Ephemeris.iflag)

        cusps = {'tropical' : tropicalCusps,
                 'sidereal' : siderealCusps}

        return cusps


    @staticmethod
    def getHouseCuspPlanetaryInfo(houseNumber,
                                  dt,
                                  houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the desired astrological house number at the given timestamp.
        
        Parameters:
        houseNumber - int value for the house number desired.
                      Value 1 refers to the first house.
        dt          - datetime.datetime object holding the timestamp at which 
                      to do the lookup.  Timezone information is automatically
                      converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.

        Returns:
        PlanetaryInfo object containing information about
        the desired astrological house number at the given timestamp.
        If there is an error or invalid input, None is returned.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug("Entered " + functName + \
                                "({}, {}, {})".\
                                format(houseNumber, dt, houseSystem))

        if houseNumber < 1 or houseNumber > 12:
            Ephemeris.log.error(functName + "(): Invalid houseNumber '{}'".\
                                format(houseNumber))
            return None

        # Store some str in variables so they don't get instantiated a
        # bunch of times.
        tropicalStr = "tropical"
        siderealStr = "sidereal"
        
        # Planet name.
        planetName = "H{}".format(houseNumber)

        # Planet ID.
        # Here we will use an invalid planet ID.
        #
        # (Note: The number chosen has no meaning.
        # I couldn't use -1, because -1 stands for SE_ECL_NUT.
        # See documentation of the Swiss Ephemeris, in
        # file: pyswisseph-1.76.00-0/doc/swephprg.htm)
        #
        planetId = -9999

        # julian day for the timestamp.
        jd = Ephemeris.datetimeToJulianDay(dt)
        
        # House cusp index.
        houseCuspIndex = houseNumber - 1
        
        # Get the tuple holding values for the house cusps.
        cusps = Ephemeris.getHouseCusps(dt, houseSystem)

        # Now fill out the dictionaries that go into a PlanetaryInfo object.
        
        # Geocentric, Tropical.
        longitude = cusps[tropicalStr][houseCuspIndex]
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        geocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Geocentric, Sidereal.
        longitude = cusps[siderealStr][houseCuspIndex]
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        geocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Topocentric, Tropical.  Not supported, so all values set to 0.0
        longitude = 0.0
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        topocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Topocentric, Sidereal.  Not supported, so all values set to 0.0
        longitude = 0.0
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        topocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Tropical.  Not supported, so all values set to 0.0
        longitude = 0.0
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        heliocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Sidereal.  Not supported, so all values set to 0.0
        longitude = 0.0
        latitude = 0.0
        distance = 0.0
        longitude_speed = 360.0
        latitude_speed = 0.0
        distance_speed = 0.0
        rectascension = 0.0
        declination = 0.0
        rectascension_speed = 0.0
        declination_speed = 0.0
        distance_speed = 0.0
        x = 0.0
        y = 0.0
        z = 0.0
        dx = 0.0
        dy = 0.0
        dz = 0.0
        
        heliocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Dictionary holding all the geocentric information.
        geocentricDict = {'tropical': geocentricTropicalDict,
                          'sidereal': geocentricSiderealDict}

        # Dictionary holding all the topocentric information.
        topocentricDict = {'tropical': topocentricTropicalDict,
                           'sidereal': topocentricSiderealDict}

        # Dictionary holding all the heliocentric information.
        heliocentricDict = {'tropical': heliocentricTropicalDict,
                            'sidereal': heliocentricSiderealDict}

        # Create the PlanetaryInfo object.
        planetaryInfo = PlanetaryInfo(planetName,
                                      planetId,
                                      dt,
                                      jd,
                                      geocentricDict,
                                      topocentricDict,
                                      heliocentricDict)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug("Exiting " + functName + \
                                "({}, {}, {})".\
                                format(houseNumber, dt, houseSystem))
        
        return planetaryInfo
    

    @staticmethod
    def getPlanetaryInfo(planetName, dt):
        """Returns a PlanetaryInfo object with a bunch of information about a
        planet at a given date/time.

        Parameters:
        planetName  - str that holds the name of the planet
        dt          - datetime.datetime object that represents the date and time
                      for which the info is requested.  This object must 
                      have the tzinfo attribute defined and it must created 
                      from pytz.
        
        Returns:
        A PlanetaryInfo object for the given timestamp.
        It has all fields populated.  The timestamp in the PlanetaryInfo 
        object returned is the same timestamp passed into this function.
        See the class description for PlanetaryInfo for details on 
        all the fields available.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr = "Entered getPlanetaryInfo(planetName={}, datetime={}"
            Ephemeris.log.debug(debugStr.format(planetName, dt))

        # Get the planet id.
        planetId = Ephemeris.getPlanetIdForName(planetName)
        
        if planetId == None:
            # This means that it is one of our additional custom
            # planets (not built into Swiss Ephemeris).
            # Handle these cases for building PlanetaryInfo separately.

            houseSystem = Ephemeris.HouseSys['Porphyry']
        
            if planetName == "H1":
                return Ephemeris.getH1PlanetaryInfo(dt, houseSystem)
            elif planetName == "H2":
                return Ephemeris.getH2PlanetaryInfo(dt, houseSystem)
            elif planetName == "H3":
                return Ephemeris.getH3PlanetaryInfo(dt, houseSystem)
            elif planetName == "H4":
                return Ephemeris.getH4PlanetaryInfo(dt, houseSystem)
            elif planetName == "H5":
                return Ephemeris.getH5PlanetaryInfo(dt, houseSystem)
            elif planetName == "H6":
                return Ephemeris.getH6PlanetaryInfo(dt, houseSystem)
            elif planetName == "H7":
                return Ephemeris.getH7PlanetaryInfo(dt, houseSystem)
            elif planetName == "H8":
                return Ephemeris.getH8PlanetaryInfo(dt, houseSystem)
            elif planetName == "H9":
                return Ephemeris.getH9PlanetaryInfo(dt, houseSystem)
            elif planetName == "H10":
                return Ephemeris.getH10PlanetaryInfo(dt, houseSystem)
            elif planetName == "H11":
                return Ephemeris.getH11PlanetaryInfo(dt, houseSystem)
            elif planetName == "H12":
                return Ephemeris.getH12PlanetaryInfo(dt, houseSystem)
            #elif planetName == "HoraLagna":
            #    # TODO:  update for HoraLagna.
            #    return Ephemeris.getHoraLagnaPlanetaryInfo(dt)
            #elif planetName == "GhatiLagna":
            #    # TODO:  update for GhatiLagna.
            #    return Ephemeris.getGhatiLagnaPlanetaryInfo(dt)
            #elif planetName == "Gulika":
            #    # TODO:  update for Gulika.
            #    return Ephemeris.getGulikaPlanetaryInfo(dt)
            #elif planetName == "Mandi":
            #    # TODO:  update for Mandi.
            #    return Ephemeris.getMandiPlanetaryInfo(dt)
            #elif planetName == "MeanSouthNode":
            #    # TODO:  update for MeanSouthNode.
            #    return Ephemeris.getMeanSouthNodePlanetaryInfo(dt)
            #elif planetName == "TrueSouthNode":
            #    # TODO:  update for TrueSouthNode.
            #    return Ephemeris.getTrueSouthNodePlanetaryInfo(dt)
            elif planetName == "MeanOfFive":
                return Ephemeris.getMeanOfFivePlanetaryInfo(dt)
            elif planetName == "CycleOfEight":
                return Ephemeris.getCycleOfEightPlanetaryInfo(dt)
            elif planetName == "AvgMaJuSaUrNePl":
                return Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(dt)
            elif planetName == "AvgJuSaUrNe":
                return Ephemeris.getAvgJuSaUrNePlanetaryInfo(dt)
            elif planetName == "AvgJuSa":
                return Ephemeris.getAvgJuSaPlanetaryInfo(dt)
            else:
                Ephemeris.log.error("Unknown planetName given to " + \
                                    "getPlanetaryInfo(): {}".format(planetName))
                return None
            
        # If it got here, then the planet name given is a standard
        # planet supported by the Swiss Ephemeris.

        # Convert time to Julian Day.
        jd = Ephemeris.datetimeToJulianDay(dt)
        
        # Geocentric, Tropical, Ecliptical info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Geocentric, Tropical, Equatorial info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Geocentric, Tropical, Rectangular info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        geocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Geocentric, Sidereal, Ecliptical info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Geocentric, Sidereal, Equatorial info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Geocentric, Sidereal, Rectangular info.
        Ephemeris.setGeocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        geocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}


        # Topocentric, Tropical, Ecliptical info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Topocentric, Tropical, Equatorial info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Topocentric, Tropical, Rectangular info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        topocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Topocentric, Sidereal, Ecliptical info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Topocentric, Sidereal, Equatorial info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Topocentric, Sidereal, Rectangular info.
        Ephemeris.setTopocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        topocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Tropical, Ecliptical info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Heliocentric, Tropical, Equatorial info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Heliocentric, Tropical, Rectangular info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setTropicalZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        heliocentricTropicalDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Heliocentric, Sidereal, Ecliptical info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEclipticalCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        longitude = arg1
        latitude = arg2
        distance = arg3
        longitude_speed = arg4
        latitude_speed = arg5
        distance_speed = arg6

        # Heliocentric, Sidereal, Equatorial info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setEquatorialCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        rectascension = arg1
        declination = arg2
        distance = arg3
        rectascension_speed = arg4
        declination_speed = arg5
        distance_speed = arg6

        # Heliocentric, Sidereal, Rectangular info.
        Ephemeris.setHeliocentricCalculations()
        Ephemeris.setSiderealZodiac()
        Ephemeris.setRectangularCoordinateSystemFlag()
        (arg1, arg2, arg3, arg4, arg5, arg6) = \
                Ephemeris.calc_ut(jd, planetId, Ephemeris.iflag)
        x = arg1
        y = arg2
        z = arg3
        dx = arg4
        dy = arg5
        dz = arg6

        heliocentricSiderealDict = \
                {'longitude': longitude, 
                 'latitude': latitude,
                 'distance': distance,
                 'longitude_speed': longitude_speed,
                 'latitude_speed': latitude_speed,
                 'distance_speed': distance_speed,
                 'rectascension': rectascension, 
                 'declination': declination,
                 'distance': distance,
                 'rectascension_speed': rectascension_speed,
                 'declination_speed': declination_speed,
                 'distance_speed': distance_speed,
                 'X': x,
                 'Y': y,
                 'Z': z,
                 'dX': dx,
                 'dY': dy,
                 'dZ': dz}

        # Dictionary holding all the geocentric information.
        geocentricDict = {'tropical': geocentricTropicalDict,
                          'sidereal': geocentricSiderealDict}

        # Dictionary holding all the topocentric information.
        topocentricDict = {'tropical': topocentricTropicalDict,
                           'sidereal': topocentricSiderealDict}

        # Dictionary holding all the heliocentric information.
        heliocentricDict = {'tropical': heliocentricTropicalDict,
                            'sidereal': heliocentricSiderealDict}

        # Create the PlanetaryInfo object.
        planetaryInfo = PlanetaryInfo(planetName,
                                      planetId,
                                      dt,
                                      jd,
                                      geocentricDict,
                                      topocentricDict,
                                      heliocentricDict)

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            debugStr = "Exiting getPlanetaryInfo(planetName={}, datetime={}"
            Ephemeris.log.debug(debugStr.format(planetName, dt))

        return planetaryInfo


    ######################################################################

    @staticmethod
    def getH1PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H1' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 1
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH2PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H2' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 2
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH3PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H3' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 3
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH4PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H4' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 4
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH5PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H5' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 5
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH6PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H6' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 6
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH7PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H7' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 7
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH8PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H8' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 8
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH9PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H9' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 9
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH10PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H10' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 10
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH11PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H11' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 11
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)
        
    @staticmethod
    def getH12PlanetaryInfo(timestamp, houseSystem=HouseSys['Porphyry']):
        """Returns a PlanetaryInfo containing information about
        the 'H12' at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        houseSystem - byte string of length 1.  That character is one of:

                      P - Placidus
                      K - Koch
                      O - Porphyrius
                      R - Regiomontanus
                      C - Campanus
                      A or E - Equal (cusp 1 is ascendant)
                      V - Vehlow equal (asc. in middle of house 1)
                      W - Whole sign
                      X - Axial rotation system
                      H - Azimuthal or horizontal system
                      T - Polich/Page ('topocentric' system)
                      B - Alcabitus
                      M - Morinus
                      U - Krusinski-Pisa
                      G - Gauquelin sectors

                      For convenience you can use the dict at
                      Ephemeris.HouseSys to reference the house system you
                      want.
        """

        houseNumber = 12
        
        return Ephemeris.getHouseCuspPlanetaryInfo(houseNumber,
                                                    timestamp,
                                                    houseSystem)

    # TODO:  Add and write function: getHoraLagnaPlanetaryInfo()
    # TODO:  Add and write function: getGhatiLagnaPlanetaryInfo()
        
    @staticmethod
    def getSunPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about the Sun at
        the given timestamp. 
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Sun", timestamp)

    @staticmethod
    def getMoonPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about the Moon at
        the given timestamp. 
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Moon", timestamp)

    @staticmethod
    def getMercuryPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Mercury at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Mercury", timestamp)

    @staticmethod
    def getVenusPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Venus at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Venus", timestamp)

    @staticmethod
    def getMarsPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Mars at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Mars", timestamp)

    @staticmethod
    def getJupiterPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Jupiter at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Jupiter", timestamp)

    @staticmethod
    def getSaturnPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Saturn at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Saturn", timestamp)

    @staticmethod
    def getUranusPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Uranus at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Uranus", timestamp)

    @staticmethod
    def getNeptunePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Neptune at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Neptune", timestamp)

    @staticmethod
    def getPlutoPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Pluto at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Pluto", timestamp)

    @staticmethod
    def getMeanNorthNodePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the MeanNorthNode at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("MeanNorthNode", timestamp)

    # TODO:  Add and write function: getMeanSouthNodePlanetaryInfo()

    @staticmethod
    def getTrueNorthNodePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the TrueNorthNode at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("TrueNorthNode", timestamp)

    # TODO:  Add and write function: getTrueSouthNodePlanetaryInfo()
    
    @staticmethod
    def getMeanLunarApogeePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the MeanLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("MeanLunarApogee", timestamp)

    @staticmethod
    def getOsculatingLunarApogeePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the OsculatingLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("OsculatingLunarApogee", timestamp)

    @staticmethod
    def getInterpolatedLunarApogeePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the InterpolatedLunarApogee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("InterpolatedLunarApogee", timestamp)

    @staticmethod
    def getInterpolatedLunarPerigeePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the InterpolatedLunarPerigee at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("InterpolatedLunarPerigee", timestamp)

    @staticmethod
    def getEarthPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Earth at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Earth", timestamp)

    @staticmethod
    def getChironPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Chiron at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Chiron", timestamp)

    # TODO:  Add and write function: getGulikaPlanetaryInfo()
    # TODO:  Add and write function: getMandiPlanetaryInfo()
    
    @staticmethod
    def getPholusPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Pholus at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Pholus", timestamp)

    @staticmethod
    def getCeresPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Ceres at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Ceres", timestamp)

    @staticmethod
    def getPallasPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Pallas at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Pallas", timestamp)

    @staticmethod
    def getJunoPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Juno at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Juno", timestamp)

    @staticmethod
    def getVestaPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the Vesta at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which to
                    do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        return Ephemeris.getPlanetaryInfo("Vesta", timestamp)

    @staticmethod
    def getMeanOfFivePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the 'Mean Of Five' (MOF) at the given timestamp.
        
        'Mean Of Five' is the average of Jupiter, Saturn, Uranus,
        Neptune and Pluto.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        jupiterPI = Ephemeris.getJupiterPlanetaryInfo(timestamp)
        saturnPI  = Ephemeris.getSaturnPlanetaryInfo(timestamp)
        uranusPI  = Ephemeris.getUranusPlanetaryInfo(timestamp)
        neptunePI = Ephemeris.getNeptunePlanetaryInfo(timestamp)
        plutoPI   = Ephemeris.getPlutoPlanetaryInfo(timestamp)

        planetaryInfos = []
        planetaryInfos.append(jupiterPI)
        planetaryInfos.append(saturnPI)
        planetaryInfos.append(uranusPI)
        planetaryInfos.append(neptunePI)
        planetaryInfos.append(plutoPI)

        planetName = "MeanOfFive"
        rv = Ephemeris.createAveragedPlanetaryInfo(planetName, planetaryInfos)

        return rv

    @staticmethod
    def getCycleOfEightPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about
        the 'Cycle Of Eight' (COE) at the given timestamp.
        This is the average of Mercury, Venus, Mars, Jupiter, Saturn,
        Uranus, Neptune, and Pluto.

        'Cycle Of Eight' is the average of Mercury, Venus, Mars,
        Jupiter, Saturn, Uranus, Neptune, and Pluto.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        mercuryPI = Ephemeris.getMercuryPlanetaryInfo(timestamp)
        venusPI   = Ephemeris.getVenusPlanetaryInfo(timestamp)
        marsPI    = Ephemeris.getMarsPlanetaryInfo(timestamp)
        jupiterPI = Ephemeris.getJupiterPlanetaryInfo(timestamp)
        saturnPI  = Ephemeris.getSaturnPlanetaryInfo(timestamp)
        uranusPI  = Ephemeris.getUranusPlanetaryInfo(timestamp)
        neptunePI = Ephemeris.getNeptunePlanetaryInfo(timestamp)
        plutoPI   = Ephemeris.getPlutoPlanetaryInfo(timestamp)

        planetaryInfos = []
        planetaryInfos.append(mercuryPI)
        planetaryInfos.append(venusPI)
        planetaryInfos.append(marsPI)
        planetaryInfos.append(jupiterPI)
        planetaryInfos.append(saturnPI)
        planetaryInfos.append(uranusPI)
        planetaryInfos.append(neptunePI)
        planetaryInfos.append(plutoPI)

        planetName = "CycleOfEight"
        rv = Ephemeris.createAveragedPlanetaryInfo(planetName, planetaryInfos)

        return rv

    @staticmethod
    def getAvgMaJuSaUrNePlPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about the
        average of the 6 outer planets (Mars to Pluto) at the given
        timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        marsPI    = Ephemeris.getMarsPlanetaryInfo(timestamp)
        jupiterPI = Ephemeris.getJupiterPlanetaryInfo(timestamp)
        saturnPI  = Ephemeris.getSaturnPlanetaryInfo(timestamp)
        uranusPI  = Ephemeris.getUranusPlanetaryInfo(timestamp)
        neptunePI = Ephemeris.getNeptunePlanetaryInfo(timestamp)
        plutoPI   = Ephemeris.getPlutoPlanetaryInfo(timestamp)

        planetaryInfos = []
        planetaryInfos.append(marsPI)
        planetaryInfos.append(jupiterPI)
        planetaryInfos.append(saturnPI)
        planetaryInfos.append(uranusPI)
        planetaryInfos.append(neptunePI)
        planetaryInfos.append(plutoPI)

        planetName = "AvgMaJuSaUrNePl"
        rv = Ephemeris.createAveragedPlanetaryInfo(planetName, planetaryInfos)

        return rv

    @staticmethod
    def getAvgJuSaUrNePlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about the
        average of 4 outer planets (Jupiter, Saturn, Uranus, Neptune)
        at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        jupiterPI = Ephemeris.getJupiterPlanetaryInfo(timestamp)
        saturnPI  = Ephemeris.getSaturnPlanetaryInfo(timestamp)
        uranusPI  = Ephemeris.getUranusPlanetaryInfo(timestamp)
        neptunePI = Ephemeris.getNeptunePlanetaryInfo(timestamp)

        planetaryInfos = []
        planetaryInfos.append(jupiterPI)
        planetaryInfos.append(saturnPI)
        planetaryInfos.append(uranusPI)
        planetaryInfos.append(neptunePI)

        planetName = "AvgJuSaUrNe"
        rv = Ephemeris.createAveragedPlanetaryInfo(planetName, planetaryInfos)

        return rv

    @staticmethod
    def getAvgJuSaPlanetaryInfo(timestamp):
        """Returns a PlanetaryInfo containing information about the
        average of Jupiter and Saturn at the given timestamp.
        
        Parameters:
        timestamp - datetime.datetime object holding the timestamp at which 
                    to do the lookup.  Timezone information is automatically
                    converted to UTC for getting the planetary info.
        """

        if Ephemeris.log.isEnabledFor(logging.DEBUG) == True:
            functName = inspect.stack()[0][3]
            Ephemeris.log.debug(functName + "({})".format(timestamp))

        jupiterPI = Ephemeris.getJupiterPlanetaryInfo(timestamp)
        saturnPI  = Ephemeris.getSaturnPlanetaryInfo(timestamp)

        planetaryInfos = []
        planetaryInfos.append(jupiterPI)
        planetaryInfos.append(saturnPI)

        planetName = "AvgJuSa"
        rv = Ephemeris.createAveragedPlanetaryInfo(planetName, planetaryInfos)

        return rv

def testGetPlanetaryInfos():
    print("Running " + inspect.stack()[0][3] + "()")

    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("    now is: {}".format(now))

    # Get planetary info for all the planets, and print out the info.
    p = Ephemeris.getSunPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMoonPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMercuryPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getVenusPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMarsPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getJupiterPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getSaturnPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getUranusPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getNeptunePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getPlutoPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanNorthNodePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getTrueNorthNodePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanLunarApogeePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getEarthPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getChironPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getPholusPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getCeresPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getPallasPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getJunoPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getVestaPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getMeanOfFivePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getCycleOfEightPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getAvgMaJuSaUrNePlPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getAvgJuSaUrNePlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))
    p = Ephemeris.getAvgJuSaPlanetaryInfo(now)
    print("    At {}, planet '{}' has the following info: \n{}".\
            format(now, p.name, p.toString()))

def testHouseCusps():
    print("Running " + inspect.stack()[0][3] + "()")

    Ephemeris.setGeographicPosition(-77.084444, 38.890277)

    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("    now is: {}".format(now))
    
    cusps = Ephemeris.getHouseCusps(now, Ephemeris.HouseSys['Porphyry'])
    print("    Tropical house cusps are: {}".format(cusps['tropical']))
    
    for i in range(len(cusps['tropical'])):
        print("    House {}:    {}".format(i, cusps['tropical'][i]))
        
    print("    Sidereal house cusps are: {}".format(cusps['sidereal']))
    
    for i in range(len(cusps['sidereal'])):
        print("    House {}:    {}".format(i, cusps['sidereal'][i]))


def testPlanetTopicalLongitude():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)

    # Get planetary info for Mercury.
    p = Ephemeris.getMercuryPlanetaryInfo(now)

    # Pick out the tropical longitude.
    longitude = p.geocentric['tropical']['longitude']
    print("    At {}, the Geocentric Tropical Longitude of {} is: {}".\
            format(now, p.name, longitude))

def testDatetimeJulianPrecisionLoss():
    print("Running " + inspect.stack()[0][3] + "()")

    print("    This test shows how we lose about a second of precision " + \
          "converting between datetime and julian day:")

    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    print("    now is: {}".format(now))

    jd = Ephemeris.datetimeToJulianDay(now)
    print("    now to jd is: {}".format(jd))

    dt = Ephemeris.julianDayToDatetime(jd, eastern)
    print("    jd back to eastern datetime is: {}".format(dt))

    amsterdam = pytz.timezone('Europe/Amsterdam')
    dt = Ephemeris.julianDayToDatetime(jd, amsterdam)
    print("    jd to asterdam datetime is: {}".format(dt))
    print("    jd to asterdam datetime formatted is: {}".\
          format(Ephemeris.datetimeToStr(dt)))


    dt = Ephemeris.julianDayToDatetime(jd, pytz.utc)
    print("    jd to UTC datetime (explicit) is: {}".format(dt))

    dt = Ephemeris.julianDayToDatetime(jd)
    print("    jd to UTC datetime (implicit) is: {}".format(dt))


def testMinMaxPlanetLongitudeSpeeds():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')

    # Pick a time and calculate the min and max speeds over X years.

    # Moon.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMoonPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))

    # Mercury.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMercuryPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))

    # Venus.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getVenusPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Mars.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMarsPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Jupiter.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 120
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getJupiterPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Saturn.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getSaturnPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Uranus.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getUranusPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Neptune.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 480
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getNeptunePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Pluto.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 840
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getPlutoPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # MeanNorthNode.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMeanNorthNodePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # TrueNorthNode.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getTrueNorthNodePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # MeanLunarApogee.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMeanLunarApogeePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # OsculatingLunarApogee.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # InterpolatedLunarApogee.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # InterpolatedLunarPerigee.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Earth.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getEarthPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Chiron.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getChironPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Pholus.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getPholusPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Ceres.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getCeresPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Pallas.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getPallasPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Juno.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getJunoPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))
        
    # Vesta.
    if False:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getVestaPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))

    # MeanOfFive.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getMeanOfFivePlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))

    # CycleOfEight.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxSpeed = 0
        minSpeed = 0
        while curr < end:
            newMaxSpeedFlag = 0
            newMinSpeedFlag = 0
            p = Ephemeris.getCycleOfEightPlanetaryInfo(curr)
            if p.geocentric['sidereal']['longitude_speed'] > maxSpeed:
                maxSpeed = p.geocentric['sidereal']['longitude_speed']
                newMaxSpeedFlag = 1
            if p.geocentric['sidereal']['longitude_speed'] < minSpeed:
                minSpeed = p.geocentric['sidereal']['longitude_speed']
                newMinSpeedFlag = 1
            #if newMaxSpeedFlag == 1 or newMinSpeedFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxSpeedFlag == 1:
            #        print("    new maxSpeed of {} is: ".format(p.name) +
            #              str(maxSpeed))
            #    if newMinSpeedFlag == 1:
            #        print("    new minSpeed of {} is: ".format(p.name) +
            #              str(minSpeed))
            curr += increment
        print("    FINAL: maxSpeed of {} is: {}".\
              format(p.name, maxSpeed))
        print("    FINAL: minSpeed of {} is: {}".\
              format(p.name, minSpeed))


def testMinMaxPlanetLatitude():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')

    # Pick a time and calculate the min and max speeds over X years.

    # Moon.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMoonPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))

    # Mercury.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMercuryPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))

    # Venus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getVenusPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Mars.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMarsPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Jupiter.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 120
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getJupiterPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Saturn.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getSaturnPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Uranus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getUranusPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Neptune.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 480
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getNeptunePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Pluto.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 840
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getPlutoPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # MeanNorthNode.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMeanNorthNodePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # TrueNorthNode.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getTrueNorthNodePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # MeanLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMeanLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # OsculatingLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # InterpolatedLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # InterpolatedLunarPerigee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Earth.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getEarthPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Chiron.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getChironPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Pholus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getPholusPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Ceres.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getCeresPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Pallas.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getPallasPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Juno.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getJunoPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))
        
    # Vesta.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getVestaPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))

    # MeanOfFive.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getMeanOfFivePlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))

    # CycleOfEight.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxLatitude = 0
        minLatitude = 0
        while curr < end:
            newMaxLatitudeFlag = 0
            newMinLatitudeFlag = 0
            p = Ephemeris.getCycleOfEightPlanetaryInfo(curr)
            if p.geocentric['tropical']['latitude'] > maxLatitude:
                maxLatitude = p.geocentric['tropical']['latitude']
                newMaxLatitudeFlag = 1
            if p.geocentric['tropical']['latitude'] < minLatitude:
                minLatitude = p.geocentric['tropical']['latitude']
                newMinLatitudeFlag = 1
            #if newMaxLatitudeFlag == 1 or newMinLatitudeFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxLatitudeFlag == 1:
            #        print("    new maxLatitude of {} is: ".format(p.name) +
            #              str(maxLatitude))
            #    if newMinLatitudeFlag == 1:
            #        print("    new minLatitude of {} is: ".format(p.name) +
            #              str(minLatitude))
            curr += increment
        print("    FINAL: maxLatitude of {} is: {}".\
              format(p.name, maxLatitude))
        print("    FINAL: minLatitude of {} is: {}".\
              format(p.name, minLatitude))


def testMinMaxPlanetDeclination():
    print("Running " + inspect.stack()[0][3] + "()")
    
    # Get the current time, which we will use to get planetary info.
    #now = datetime.datetime.utcnow()
    eastern = pytz.timezone('US/Eastern')

    # Pick a time and calculate the min and max speeds over X years.

    # Moon.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMoonPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))

    # Mercury.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 30
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMercuryPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))

    # Venus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getVenusPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Mars.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMarsPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Jupiter.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 120
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getJupiterPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Saturn.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getSaturnPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Uranus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 240
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getUranusPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Neptune.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 480
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getNeptunePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Pluto.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=2)
        years = 840
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getPlutoPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # MeanNorthNode.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMeanNorthNodePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # TrueNorthNode.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getTrueNorthNodePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # MeanLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMeanLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # OsculatingLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getOsculatingLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # InterpolatedLunarApogee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getInterpolatedLunarApogeePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # InterpolatedLunarPerigee.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getInterpolatedLunarPerigeePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Earth.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getEarthPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Chiron.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getChironPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Pholus.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getPholusPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Ceres.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getCeresPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Pallas.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getPallasPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Juno.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getJunoPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))
        
    # Vesta.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getVestaPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))

    # MeanOfFive.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getMeanOfFivePlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))

    # CycleOfEight.
    if True:
        start = datetime.datetime.now(eastern)
        increment = datetime.timedelta(hours=1)
        years = 60
        finishDelta = datetime.timedelta(days=years*365)
        end = start + finishDelta
        curr = start
        maxDeclination = 0
        minDeclination = 0
        while curr < end:
            newMaxDeclinationFlag = 0
            newMinDeclinationFlag = 0
            p = Ephemeris.getCycleOfEightPlanetaryInfo(curr)
            if p.geocentric['tropical']['declination'] > maxDeclination:
                maxDeclination = p.geocentric['tropical']['declination']
                newMaxDeclinationFlag = 1
            if p.geocentric['tropical']['declination'] < minDeclination:
                minDeclination = p.geocentric['tropical']['declination']
                newMinDeclinationFlag = 1
            #if newMaxDeclinationFlag == 1 or newMinDeclinationFlag == 1:
            #    print("    curr is: {}".format(curr))
            #    if newMaxDeclinationFlag == 1:
            #        print("    new maxDeclination of {} is: ".format(p.name) +
            #              str(maxDeclination))
            #    if newMinDeclinationFlag == 1:
            #        print("    new minDeclination of {} is: ".format(p.name) +
            #              str(minDeclination))
            curr += increment
        print("    FINAL: maxDeclination of {} is: {}".\
              format(p.name, maxDeclination))
        print("    FINAL: minDeclination of {} is: {}".\
              format(p.name, minDeclination))


# For debugging the Ephemeris class during development.  
if __name__=="__main__":
    # Exercising the PlanetaryInfo and Ephemeris classes.
    print("------------------------")

    # Initialize Logging for the Ephemeris class (required).
    LOG_CONFIG_FILE = os.path.join(sys.path[0], "../conf/logging.conf")
    logging.config.fileConfig(LOG_CONFIG_FILE)

    # Initialize Ephemeris (required).
    Ephemeris.initialize()

    # Set the Location (required).

    # Chicago:
    #lat = -87.627777777777
    #lon = 41.8819444444444444
    
    # Chantilly/Arlington:
    lat = -77.084444
    lon = 38.890277

    #Ephemeris.setGeographicPosition(lat, lon, -68)
    Ephemeris.setGeographicPosition(lat, lon)
    
    # Different tests that can be run:
    #testGetPlanetaryInfos()
    #testHouseCusps()
    #testPlanetTopicalLongitude()
    #testDatetimeJulianPrecisionLoss()

    # These tests will take a long time, so I've commented it out.
    #testMinMaxPlanetLongitudeSpeeds()
    #testMinMaxPlanetLatitude()
    testMinMaxPlanetDeclination()
    
    # Close the Ephemeris so it can do necessary cleanups.
    Ephemeris.closeEphemeris()

    # Shutdown logging so all the file handles get flushed and 
    # cleanup can happen.
    logging.shutdown()

    print("Exiting.")





