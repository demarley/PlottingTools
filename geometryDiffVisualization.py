import re
from math import *
from svgfig import rgb, SVG, pathtoPath, load as load_svg
from geometryXMLparser import *
from signConventions import *

def dt_colors(wheel, station, sector):
#    return rgb(0.1, 0.9, 0.)
    return '#FF9900'

def csc_colors(endcap, station, ring, chamber):
#    return rgb(0.1, 0.5, 0.8)
    return '#3ffa3f'

def draw_station(geom1, geom2, station, filename, length_factor=200., angle_factor=200., colors=dt_colors):
    if station == 4: station_template = load_svg("station4_template.svg")
    else: station_template = load_svg("station_template.svg")

    if station == 1: x_scale_factor = 1/6.
    if station == 2: x_scale_factor = 1/7.
    if station == 3: x_scale_factor = 1/8.5
    if station == 4: x_scale_factor = 1/10.
    y_scale_factor = 1/7.

    # make a new group to put the moved chambers into
    new_boxes = SVG("g")

    # loop over the SVG tree, looking for our chambers (by id)
    for treeindex, svgitem in station_template:
        if isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"][:3] == "MB_":
            m = re.match("MB_([0-9mpz]+)_([0-9]+)", svgitem["id"])
            if m is None: raise Exception

            wheel = m.group(1)
            if wheel == "m2": wheel = -2
            elif wheel == "m1": wheel = -1
            elif wheel == "z": wheel = 0
            elif wheel == "p1": wheel = 1
            elif wheel == "p2": wheel = 2
            sector = int(m.group(2))

            xdiff = x_scale_factor * length_factor * (geom1.dt[wheel, station, sector].x - geom2.dt[wheel, station, sector].x) * signConventions["DT", wheel, station, sector][0]
            ydiff = -y_scale_factor * length_factor * (geom1.dt[wheel, station, sector].y - geom2.dt[wheel, station, sector].y) * signConventions["DT", wheel, station, sector][1]
            phizdiff = -angle_factor * (geom1.dt[wheel, station, sector].phiz - geom2.dt[wheel, station, sector].phiz) * signConventions["DT", wheel, station, sector][2]

            sx = float(svgitem["x"]) + float(svgitem["width"])/2.
            sy = float(svgitem["y"]) + float(svgitem["height"])/2.

            svgitem["transform"] = "translate(%g,%g)" % (sx, sy)
            svgitem["x"] = -float(svgitem["width"])/2.
            svgitem["y"] = -float(svgitem["height"])/2.

            svgitem["style"] = "fill:#e1e1e1;fill-opacity:1;stroke:#000000;stroke-width:1.0;stroke-dasharray:1, 1;stroke-dashoffset:0"

            newBox = svgitem.clone()
            newBox["transform"] = "translate(%g,%g) rotate(%g) " % (sx + xdiff, sy + ydiff, phizdiff * 180./pi)
            newBox["style"] = "fill:%s;fill-opacity:0.5;stroke:#000000;stroke-width:1.0;stroke-opacity:1;stroke-dasharray:none" % colors(wheel, station, sector)

            new_boxes.append(newBox)
            
    for treeindex, svgitem in station_template:
        if isinstance(svgitem, SVG) and svgitem.t == "g" and "id" in svgitem.attr and svgitem["id"] == "chambers":
            svgitem.append(new_boxes)

        elif isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"] == "stationx":
            svgitem[0] = "Station %d" % station
            svgitem[0] += " (length x%g, angle x%g)" % (length_factor, angle_factor)

    station_template.save(filename)

def draw_wheel(geom1, geom2, wheel, filename, length_factor=100., angle_factor=100., colors=dt_colors):
    wheel_template = load_svg("wheel_template.svg")

    # make a new group to put the moved chambers into
    new_boxes = SVG("g")

    # loop over the SVG tree, looking for our chambers (by id)
    for treeindex, svgitem in wheel_template:
        if isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"][:3] == "MB_":
            m = re.match("MB_([0-9]+)_([0-9]+)", svgitem["id"])
            if m is None: raise Exception

            station, sector = int(m.group(1)), int(m.group(2))
            xdiff = -length_factor * (geom1.dt[wheel, station, sector].x - geom2.dt[wheel, station, sector].x) * signConventions["DT", wheel, station, sector][0]
            zdiff = length_factor * (geom1.dt[wheel, station, sector].z - geom2.dt[wheel, station, sector].z) * signConventions["DT", wheel, station, sector][2]
            phiydiff = -angle_factor * (geom1.dt[wheel, station, sector].phiy - geom2.dt[wheel, station, sector].phiy) * signConventions["DT", wheel, station, sector][1]

	    m = re.search("translate\(([0-9\.\-\+eE]+),\s([0-9\.\-\+eE]+)\)\srotate\(([0-9\.\-\+eE]+)\)",svgitem["transform"])

	    tx = float(m.group(1))
	    ty = float(m.group(2))
	    tr = float(m.group(3))

            newBox = svgitem.clone()

	    svgitem["style"] = "fill:#e1e1e1;fill-opacity:1;stroke:#000000;stroke-width:5.0;stroke-dasharray:1, 1;stroke-dashoffset:0"
            newBox["style"] = "fill:%s;fill-opacity:0.5;stroke:#000000;stroke-width:5.0;stroke-opacity:1;stroke-dasharray:none" % colors(wheel, station, sector)
            newBox["id"] = newBox["id"] + "_moved"

            newBox["transform"] = "translate(%g,%g) rotate(%g)" % (tx - xdiff*cos(tr*pi/180.) + zdiff*sin(tr*pi/180.), ty - xdiff*sin(tr*pi/180.) - zdiff*cos(tr*pi/180.), tr - phiydiff*180./pi) 

            new_boxes.append(newBox)

    for treeindex, svgitem in wheel_template:
        if isinstance(svgitem, SVG) and svgitem.t == "g" and "id" in svgitem.attr and svgitem["id"] == "chambers":
            svgitem.append(new_boxes)

        elif isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"] == "wheelx":
            if wheel == 0: svgitem[0] = "Wheel 0"
            else: svgitem[0] = "Wheel %+d" % wheel
            svgitem[0] += " (length x%g, angle x%g)" % (length_factor, angle_factor)

    wheel_template.save(filename)

def draw_disk(geom1, geom2, endcap, station, filename, length_factor=1., angle_factor=100., colors=csc_colors):
    if station == 1: disk_template = load_svg("disk1_template.svg")
    if station in (2, 3, 4): disk_template = load_svg("disk234_template.svg")

    scale_factor = 0.233
    
    new_boxes = SVG("g")

    # center of the template
    originx = 339.74905
    originy = 513.50318

    for treeindex, svgitem in disk_template:
        if isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"][:3] == "ME_":
            m = re.match("ME_([0-9]+)_([0-9]+)", svgitem["id"])
            if m is None: raise Exception

            ring, chamber = int(m.group(1)), int(m.group(2))

            xdiff = scale_factor * length_factor * (geom2.csc[endcap, station, ring, chamber].x - geom1.csc[endcap, station, ring, chamber].x) * signConventions["CSC", endcap, station, ring, chamber][0]
            ydiff = scale_factor * length_factor * (geom2.csc[endcap, station, ring, chamber].y - geom1.csc[endcap, station, ring, chamber].y) * signConventions["CSC", endcap, station, ring, chamber][1]
            phizdiff = -angle_factor * (geom2.csc[endcap, station, ring, chamber].phiz - geom1.csc[endcap, station, ring, chamber].phiz) * signConventions["CSC", endcap, station, ring, chamber][2]

            svgitem["style"] = "fill:#e1e1e1;fill-opacity:1;stroke:#000000;stroke-width:1.0;stroke-dasharray:1, 1;stroke-dashoffset:0"

            # copy chamber
            newBox = pathtoPath(svgitem)

            # find the center of the chamber
            sumx = 0.
            sumy = 0.
            sum1 = 0.
            for i, di in enumerate(newBox.d):
                if di[0] == "L":
                    sumx += di[1]
                    sumy += di[2]
                    sum1 += 1.
            centerx = sumx/sum1
            centery = sumy/sum1

            # global phi of the chamber
            phipos = atan2(originy-centery, centerx - originx)

            # global shifts of the chamber calculated from local shifts
            dx = -sin(phipos)*xdiff - cos(phipos)*ydiff
            dy = -cos(phipos)*xdiff + sin(phipos)*ydiff

            # shift the chamber along global X and Y
            for i, di in enumerate(newBox.d):
                if di[0] in ("M", "L"):
                    di = list(di)
                    di[1] += dx
                    di[2] += dy
                    newBox.d[i] = tuple(di)

            # shift the center of the chamber along global X and Y
            centerx += dx
            centery += dy

            for i, di in enumerate(newBox.d):
                if di[0] in ("M", "L"):
                    di = list(di)
                    # global shifts of the chamber calculated from local rotation
                    dispx = cos(phizdiff) * (di[1] - centerx) - sin(phizdiff) * (di[2] - centery)
                    dispy = sin(phizdiff) * (di[1] - centerx) + cos(phizdiff) * (di[2] - centery)
                    # shift the chamber along global X and Y
                    di[1] = dispx + centerx
                    di[2] = dispy + centery
                    newBox.d[i] = tuple(di)

            newBox = newBox.SVG()
            newBox["style"] = "fill:%s;fill-opacity:0.5;stroke:#000000;stroke-width:1.0;stroke-opacity:1;stroke-dasharray:none" % colors(endcap, station, ring, chamber)
            newBox["id"] = newBox["id"] + "_moved"

            new_boxes.append(newBox)

    for treeindex, svgitem in disk_template:
        if isinstance(svgitem, SVG) and svgitem.t == "g" and "id" in svgitem.attr and svgitem["id"] == "chambers":
            svgitem.append(new_boxes)

        elif isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"] == "diskx":
            if endcap == 1: svgitem[0] = "Disk %+d" % station
            else: svgitem[0] = "Disk %+d" % (-station)
            svgitem[0] += " (length x%g, angle x%g)" % (length_factor, angle_factor)

    disk_template.save(filename)
    
def draw_sector(geom1, geom2, sector, filename, length_factor=100., angle_factor=100., colors=dt_colors):
    if sector < 13: 
    	sector_template = load_svg("sector_template.svg")
    else:
    	sector_template = load_svg("sector_template_station4.svg")

    # make a new group to put the moved chambers into
    new_boxes = SVG("g")

    # loop over the SVG tree, looking for our chambers (by id)
    for treeindex, svgitem in sector_template:
        if isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"][:3] == "MB_":
            m = re.match("MB_([0-9])_([0-9])", svgitem["id"])
            if m is None: raise Exception

            wheel, station = int(m.group(1))-2, int(m.group(2))

            m = re.search("translate\(([0-9\.\-\+eE]+),([0-9\.\-\+eE]+)\)",svgitem["transform"])

            tx = float(m.group(1))
            ty = float(m.group(2))

            ydiff =    -length_factor * (geom2.dt[wheel, station, sector].y   - geom1.dt[wheel, station, sector].y)    * signConventions["DT", wheel, station, sector][1]
            zdiff =    -length_factor * (geom2.dt[wheel, station, sector].z   - geom1.dt[wheel, station, sector].z)    * signConventions["DT", wheel, station, sector][2]
            phixdiff = angle_factor * (geom2.dt[wheel, station, sector].phix - geom1.dt[wheel, station, sector].phix) * signConventions["DT", wheel, station, sector][0]

            newBox = svgitem.clone()

            svgitem["style"] = "fill:#e1e1e1;fill-opacity:1;stroke:#000000;stroke-width:5.0;stroke-dasharray:1, 1;stroke-dashoffset:0"
            newBox["style"] = "fill:%s;fill-opacity:0.5;stroke:#000000;stroke-width:5.0;stroke-opacity:1;stroke-dasharray:none" % colors(wheel, station, sector)
            newBox["id"] = newBox["id"] + "_moved"

            newBox["transform"] = "translate(%g,%g) rotate(%g)" % (tx + ydiff, ty - zdiff, phixdiff*180./pi) 

            new_boxes.append(newBox)

    for treeindex, svgitem in sector_template:
        if isinstance(svgitem, SVG) and svgitem.t == "g" and "id" in svgitem.attr and svgitem["id"] == "chambers":
            svgitem.append(new_boxes)

        elif isinstance(svgitem, SVG) and "id" in svgitem.attr and svgitem["id"] == "title":
            svgitem[0] = "Sector %d (length x%g, angle x%g)" % (sector,length_factor, angle_factor)

    sector_template.save(filename)
