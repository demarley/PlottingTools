"""
7 August 2017
Dan Marley
daniel.edison.marley@cernSPAMNOT.ch

General information to be kept in one central location.
*Only need to edit one file rather than many!*
"""


def csc():
    """Collection of information about CSCs"""
    endcaps = [1,2]
    disks   = [1,2,3,4]
    rings   = {1:[1,2,3],   # different rings for different disks
               2:[1,2], 
               3:[1,2],
               4:[1,2]}

    csc_info = {
      "endcaps":endcaps,
      "disks":  disks,
      "rings":  rings}

    return csc_info


def dt():
    """Collection of information about DTs"""
    wheels   = [-2, -1, 0, 1, 2]
    stations = [1,2,3,4]
    sectors  = range(1,13)
    sectors4 = range(1,15)      # more sections for station 4

    dt_info  = {
      "wheels":wheels,
      "stations":stations,
      "sectors": sectors,
      "sectors4":sectors4}

    return dt_info