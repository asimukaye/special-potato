#!/usr/bin/env python
import sys
import piexif
from datetime import datetime
import json

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = int((md - m) * 60*3125)
    return [d, m, sd]

def tag (lat, lon, alt):
        datenow = unicode(str(datetime.now()), "utf-8")
        if lat>=0:
            latref = "N"
        else:
            latref = "S"
            
        if lon>=0:
            lonref = "E"
        else:
            lonref = "W"

        # lat_n = int(abs(lat)*1000)
        # lon_n = int(abs(lon)*1000)
        alt_n = int(abs(alt)*1000)    
        lat_n = dd2dms(lat)
        lon_n = dd2dms(lon)
        # print lat_n[1], type(lat_n[1])
        # print lat_n[2], type(lat_n[2])
            
        zeroth_ifd = { piexif.ImageIFD.Make: u"SONY",
                        piexif.ImageIFD.XResolution: (853, 1),
                        piexif.ImageIFD.YResolution: (480, 1),
                        piexif.ImageIFD.Software: u"piexif"
                        }
                            
        exif_ifd = {piexif.ExifIFD.Sharpness: 65535,
                    piexif.ExifIFD.DateTimeOriginal: datenow,
                    piexif.ExifIFD.LensSpecification: ((1, 1), (1, 1), (1, 1), (1, 1)),
                    piexif.ExifIFD.LensMake: u"LensMake",
                    # piexif.ExifIFD.MakerNote: u"Gimbal angle: 13 deg",
                    piexif.ExifIFD.ComponentsConfiguration: u"Gimd",
                    # piexif.ExifIFD.UserComments: u"Gimbal angle: 13 deg",
                    }
                    
        gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
                    piexif.GPSIFD.GPSLatitudeRef: latref,
                    piexif.GPSIFD.GPSLatitude: [(lat_n[0], 1), (lat_n[1], 1), (lat_n[2], 3125)],
                    # piexif.GPSIFD.GPSLatitude: (lat_n, 1000), 
                    piexif.GPSIFD.GPSLongitudeRef: lonref,
                    piexif.GPSIFD.GPSLongitude: [(lon_n[0], 1), (lon_n[1], 1), (lon_n[2], 3125)],
                    # piexif.GPSIFD.GPSLongitude: (lon_n, 1000),
                    piexif.GPSIFD.GPSAltitude: (alt_n, 1000),
                    piexif.GPSIFD.GPSAltitudeRef: 1,
                    piexif.GPSIFD.GPSDateStamp: datenow,
                    }
                    
        exif_dict = {"0th":zeroth_ifd,"Exif":exif_ifd, "GPS":gps_ifd}

        return piexif.dump(exif_dict)


# exif_dict = piexif.load("capture-5.jpg")
# thumbnail = exif_dict.pop("thumbnail")
# if thumbnail is not None:
#     with open("thumbnail.jpg", "wb+") as f:
#         f.write(thumbnail)
# for ifd_name in exif_dict:
#     print("\n{0} IFD:".format(ifd_name))
#     for key in exif_dict[ifd_name]:
#         try:
#             print(key, exif_dict[ifd_name][key][:10])
#         except:
#             print(key, exif_dict[ifd_name][key])

piexif.remove("capture-5-1.jpg")
exif_bytes = tag(12.9501123, 77.656432, 759.592)
piexif.insert(exif_bytes, "capture-5-1.jpg")