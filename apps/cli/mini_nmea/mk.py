"""Writes data/: NMEA 0183 logs from a morning's sail out of the Solent
(the GPS, the instruments on the bus, and proprietary sentences from a
dozen receivers), a file of broken and odd lines, and the job list.
Every sentence that should carry a checksum gets the right one here,
except the ones that are meant to be wrong."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def cs(body):
    c = 0
    for ch in body:
        c ^= ord(ch)
    return c


def s(body):
    return "$%s*%02X" % (body, cs(body))


def hms(t):
    return "%02d%02d%02d" % (t // 3600, t // 60 % 60, t % 60)


def lat_s(minutes):
    d = int(minutes // 60)
    return "%02d%07.4f" % (d, minutes - d * 60)


def lon_s(minutes):
    d = int(minutes // 60)
    return "%03d%07.4f" % (d, minutes - d * 60)


def trip():
    out = []
    t0 = 8 * 3600
    lat = 50 * 60 + 46.512   # minutes north
    lon = 1 * 60 + 17.204    # minutes west
    out.append(s("GPTXT,01,01,02,u-blox ag - www.u-blox.com"))
    out.append(s("GPTXT,01,01,02,ANTSTATUS=OK"))
    out.append(s("GPRTE,2,1,c,SOLENT,HAMBLE,CALSHOT,NEEDLES,YARMOUTH"))
    out.append(s("GPRTE,2,2,c,SOLENT,LYMINGTON,HURST"))
    out.append(s("GPWPL,5050.6200,N,00119.0800,W,HAMBLE"))
    out.append(s("GPWPL,5049.0300,N,00118.1100,W,CALSHOT"))
    out.append(s("GPWPL,5039.6500,N,00135.0500,W,NEEDLES"))
    for step in range(36):
        t = t0 + step * 20
        lost = 14 <= step <= 16
        sog = 4.2 + (step % 7) * 0.35
        cog = 212.0 + (step % 5) * 1.5
        frac = ".00" if step % 3 else ".50"
        ts = hms(t) + frac
        la, lo = lat_s(lat), lon_s(lon)
        if lost:
            out.append(s("GPRMC,%s,V,,,,,,,150624,,,N" % ts))
            out.append(s("GPGGA,%s,,,,,0,00,99.99,,,,,," % ts))
            out.append(s("GPGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99"))
            out.append(s("GPVTG,,,,,,,,,N"))
        else:
            mode = "D" if step % 4 == 0 else "A"
            out.append(s("GPRMC,%s,A,%s,N,%s,W,%.2f,%.1f,150624,0.9,W,%s,%s" % (ts, la, lo, sog, cog, mode, "SSSCU"[step % 5] if step != 20 else "V")))
            alt = 2.1 + (step % 3) * 0.4
            qual = 2 if mode == "D" else 1
            out.append(s("GPGGA,%s,%s,N,%s,W,%d,%02d,0.9%d,%.1f,M,47.3,M,%s,%s" % (
                ts, la, lo, qual, 8 + step % 4, step % 10, alt,
                "3.0" if qual == 2 else "", "0120" if qual == 2 else "")))
            out.append(s("GPVTG,%.1f,T,%.1f,M,%.2f,N,%.2f,K,%s" % (cog, cog + 0.9, sog, sog * 1.852, mode)))
            if step % 2 == 0:
                out.append(s("GPGSA,A,3,02,05,12,15,18,24,25,29,,,,,1.6,0.9,1.3"))
            if step % 6 == 0:
                out.append(s("GPGSV,3,1,11,02,47,123,40,05,23,061,36,12,71,268,45,15,18,302,33"))
                out.append(s("GPGSV,3,2,11,18,09,330,28,24,55,190,44,25,34,084,41,29,62,145,46"))
                out.append(s("GPGSV,3,3,11,31,05,025,,32,12,248,22,36,30,160,38"))
                out.append(s("GPGLL,%s,N,%s,W,%s,A,%s" % (la, lo, ts, mode)))
        if step % 3 == 0:
            depth = 8.4 + (step % 9) * 1.3 - (2.5 if step in (24, 27) else 0)
            out.append(s("SDDBT,%.1f,f,%.1f,M,%.1f,F" % (depth * 3.28084, depth, depth * 0.546807)))
            out.append(s("SDDPT,%.1f,0.5,100" % depth))
            out.append(s("SDMTW,16.%d,C" % (step % 10)))
        if step % 4 == 1:
            awa = 42.0 + step % 11
            aws = 11.5 + (step % 8) * 0.9 + (9.0 if step == 29 else 0)
            out.append(s("WIMWV,%.1f,R,%.1f,N,A" % (awa, aws)))
            out.append(s("WIMWV,%.1f,T,%.1f,N,A" % (awa + 18.0, aws - 2.2)))
            out.append(s("WIMWD,%.1f,T,%.1f,M,%.1f,N,%.1f,M" % (cog + 60, cog + 59.1, aws - 2.2, (aws - 2.2) * 0.514444)))
            out.append(s("HCHDG,%.1f,,,0.9,W" % (cog - 3.0)))
            out.append(s("HCHDT,%.1f,T" % (cog - 3.9)))
            out.append(s("VWVHW,%.1f,T,%.1f,M,%.2f,N,%.2f,K" % (cog - 3.9, cog - 3.0, sog - 0.4, (sog - 0.4) * 1.852)))
        if step % 9 == 4:
            out.append(s("GPZDA,%s,15,06,2024,01,00" % ts))
            out.append(s("WIXDR,C,19.5,C,TempAir,P,1.0132,B,Barometer,H,71.2,P,Humidity"))
            out.append(s("WIMDA,29.9213,I,1.0132,B,19.5,C,16.2,C,71.2,,13.9,C,%.1f,T,%.1f,M,9.3,N,4.8,M" % (cog + 60, cog + 59.1)))
            out.append(s("APXTE,A,A,0.0%d,%s,N" % (step % 7, "L" if step % 2 else "R")))
            out.append(s("APAPB,A,A,0.0%d,%s,N,V,V,236.4,T,NEEDLES,235.1,T,233.9,M" % (step % 7, "L" if step % 2 else "R")))
            out.append(s("GPRMB,A,0.0%d,%s,CALSHOT,NEEDLES,5039.6500,N,00135.0500,W,9.8,236.4,4.9,V" % (step % 7, "L" if step % 2 else "R")))
            out.append(s("GPBOD,236.4,T,235.5,M,NEEDLES,CALSHOT"))
            out.append(s("GPBWC,%s,5039.6500,N,00135.0500,W,236.4,T,235.5,M,9.8,N,NEEDLES,A" % ts))
        lat -= 0.0123 * sog
        lon += 0.0151 * sog
    out.append(s("GPZDA,082000.00,15,06,2024,-05,-30"))
    out.append(s("GPZDA,082000.00,15,06,2024,-05,30"))
    out.append(s("GPAAM,A,A,0.10,N,NEEDLES"))
    return out


def instruments():
    return [
        s("GPGNS,014035.00,4332.69262,S,17235.48549,E,RR,13,0.9,25.63,11.24,,"),
        s("GNGNS,014035.00,,,,,NNN,00,99.99,,,,"),
        s("GPGRS,024603.00,1,-1.1,-0.5,0.2,0.4,1.7,-0.7,,,,,,"),
        s("GPGST,172814.0,0.006,0.023,0.020,273.6,0.023,0.020,0.031"),
        s("GPGBS,235458.00,1.4,1.3,3.1,03,,-21.4,3.8,1,0"),
        s("GPDTM,W84,,0.0,N,0.0,E,0.0,W84"),
        s("GPDTM,999,CH95,0.08,N,0.07,E,-47.7,W84"),
        s("GPALM,1,1,15,1159,00,441d,4e,16be,fd5e,a10c9f,4a2da4,686e81,58cbe1,0a4,001"),
        s("GPAPA,A,A,0.10,R,N,V,V,011,M,DEST"),
        s("GPBEC,220516,5130.02,N,04607.80,W,213.8,T,218.0,M,0004.6,N,EGLM,A"),
        s("GPBWR,220516,5130.02,N,00046.34,W,213.8,T,218.0,M,0004.6,N,EGLM"),
        s("GPBWW,213.8,T,218.0,M,TOWER,EGLM"),
        s("GPSTN,10"),
        s("GPTRF,183220,030994,4917.24,N,12309.57,W,59.3,3,6,1.8,32"),
        s("GPWCV,2.3,N,NEEDLES"),
        s("GPWNC,200.00,N,370.40,K,START,END"),
        s("GPR00,EGLL,EGLM,EGTB,EGUB,EGTK,MBOT,EGTB,,,,,,,"),
        s("GPRMA,A,4917.24,N,12309.57,W,,,12.5,054.7,5.2,E"),
        s("APHSC,40.12,T,39.11,M"),
        s("AGRSA,-2.4,A,,V"),
        s("RAOSD,35.1,A,36.0,M,5.8,M,,,N"),
        s("RATLL,01,5042.12,N,00121.50,W,TANKER,082003.50,T,"),
        s("RATTM,02,1.43,170.5,T,0.16,264.4,T,1.42,36.9,N,FERRY,T,,082004.00,A"),
        s("VWVDR,10.1,T,12.3,M,1.2,N"),
        s("VWVPW,4.5,N,6.7,M"),
        s("WIVWR,75,R,1.0,N,0.51,M,1.85,K"),
        s("WIVWT,30.0,L,12.5,N,6.4,M,23.2,K"),
        s("SDDBS,24.6,f,7.5,M,4.1,F"),
        s("HCHDM,238.5,M"),
        s("VWVLW,1234.5,N,12.3,N"),
        s("TIROT,-1.3,A"),
        s("ERRPM,E,1,2418.2,10.5,A"),
        s("ERRPM,S,2,,-5.0,V"),
        s("GPVBW,4.5,0.2,A,4.6,0.1,A"),
        s("GPVBW,4.5,0.2,A,,,V"),
        s("STALK,84,B6,10,00,00,00,00,00,00"),
        s("STALK,9C,01,25,00"),
        s("STALK,30,00,0C"),
        s("WIXDR,C,19.52,C,TempAir,P,1.02481,B,Barometer,A,-0.5,D,Pitch,A,1.3,D,Roll,G,,,Spare"),
        s("GPZDA,201530.00,04,07,2002,00,00"),
        s("GPZDA,201530.00,31,02,2002,00,00"),
        s("GPZDA,201530.00,04,07,,00,00"),
        s("GPZDA,201530.00,04,07,2002,,"),
        s("GPZDA,201530.00,04,07,2002,+03,"),
        s("GPZDA,,04,07,2002,00,00"),
        s("GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E"),
        s("GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E,A"),
        s("GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E,N,U"),
        s("GPRMC,225446.333,A,4916.45,N,12311.12,W,000.5,054.7,311294,020.3,E,A,S"),
        s("GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,310294,020.3,E"),
        s("GPRMC,2254,A,4916.45,N,12311.12,W,000.5,054.7,11294,020.3,E"),
        s("GPRMC,245446,A,4916.45,N,12311.12,W,000.5,054.7,1 1294,020.3,E"),
        s("GPRMC,225460,A,16.45,N,12311.12,X,inf,nan,191169,,"),
        s("GPRMC,225446.9999999,A,0,N,0.0,E,1_000.5,_5,010100,,"),
        s("GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000"),
        s("GPGGA,184353.07,1929.045,S,02410.506,E,7,04,2.6,1e3,M,-33.9,M,,0000"),
        s("GPGGA,184353.07,1929.045,S,02410.506,E,x,04,2.6, 12 ,M,-33.9,M,,0000"),
        s("GPGSA,A,,,,,,,,,,,,,,,,"),
        s("GPGSA,A, 2 ,04,05,,,,,,,,,,,2.5,1.3,2.1"),
        s("GPGSA,A,3.0,04,05,,,,,,,,,,,2.5,1.3,2.1"),
        s("GPHDG,98.3,0.0,E,12.6,W"),
        s("GPHDG,98.30,-0,E,1_2.6,W"),
        s("GPHDG,1E2,.5,E,5.,W"),
        s("GPHDG,0.0000001,100E-2,E,-.0,W"),
        s("GPHDG,NaN,Infinity,E,-Inf,W"),
        s("GPHDG,12.3.4,abc,E,,W"),
    ]


def devices():
    return [
        s("PGRME,15.0,M,45.0,M,25.0,M"),
        s("PGRMM,WGS 84"),
        s("PGRMZ,246,f,3"),
        s("PGRMW,Home,32,1B,My house"),
        s("PGRMT,GPS 18x-5Hz,P,P,R,R,P,,23,R"),
        s("PKWDWPL,150803,V,4237.14,N,07120.83,W,,,190316,,test,5,/'"),
        s("PKWDWPL,204714,V,4237.1400,N,07120.8300,W,,,200316,,test|5,/'"),
        s("PKWDWPL,204714,A,4237.1400,N,07120.8300,W,12.5,270.0,200316,35,KD2ABC,/>"),
        s("PMGNWPL,4228.7520,N,07040.4680,W,0000000,M,Plymouth,Plymouth Rock,a"),
        s("PMGNWPL,4228.7520,N,07040.4680,W,12_5,M,Gurnet,\"Light\",b,xx"),
        s("PRDID,-1.31,7.81,47.31"),
        s("PRDID,-1.31,seven,47.31,extra"),
        s("PSRF100,1,9600,8,1,0"),
        s("PSXN,20,0,0,0,0"),
        s("PSXN,21,1"),
        s("PSXN,22,0.12,0.05"),
        s("PSXN,23,0.30,-0.97,298.57,0.13"),
        s("PSXN,24,0.01,-0.02,0.10,0.00"),
        s("PSXN,26,0,44.5000,0.7800,-0.9000,NRP"),
        s("PTNL,AVR,212405.20,+52.1531,Yaw,-0.0806,Tilt,,,12.575,3,1.4,16"),
        s("PTNL,BPQ,224445.06,021207,3723.09383914,N,12200.32620132,W,EHT-5.923,M,5"),
        s("PTNL,GGK,172814.00,071296,3723.46587704,N,12202.26957864,W,3,06,1.7,EHT-6.777,M"),
        s("PTNL,VHD,030556.00,300998,187.718,-22.138,-76.929,-5.015,0.033,0.006,3,07,2.4"),
        s("PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404"),
        s("PTNL,,QTA,1,2"),
        s("PUBX,00,081350.00,4717.113210,N,00833.915187,E,546.589,G3,2.1,2.0,0.007,77.52,0.007,,0.92,1.19,0.77,9,0,0"),
        s("PUBX,03,11,23,-,,,45,010,29,-,,,46,013,07,-,,,42,015,08,U,067,31,42,025"),
        s("PUBX,04,073731.00,091202,113851.00,1196,15D,1930035,-2660.664,43"),
        s("PUBX,41,1,0007,0003,19200,0"),
        s("PVTX,0002,000123,135.5,M,120.4,D,-1.2,2.3,E"),
        s("PVTX,0000,135.5,M,2.1016,0.0123,-0.0209,R"),
        s("PVTX,0020,000124,4717.1132,N,00833.9152,E,546.6,M"),
        s("PVTX,0012,000125,4717.4501,N,00834.1102,E,551.2,M,4.6,M"),
        s("PASHR,130533.620,0.311,T,-80.467,-1.395,,0.066,0.067,0.215,2,3"),
        s("PASHR,130533.62,0.311,T,-80.467,-1.395,0.25,0.066,0.067,0.215,2,3"),
        s("PASHR,HPR,085335.00,224.19,-01.26,+00.83,0.000,0.000,0,1,0,2.5"),
        s("PASHR,LTN,3"),
        s("PASHR,POS,0,09,224645.00,3722.62223,N,12159.97347,W,00010.384,,000.0,000.0,+000.0,02.0,01.0,01.7,01.2,0000"),
        s("PASHR,VEL,0,100115.50,+0.012,-0.034,+0.002,0.050,0.050,0.090,1000"),
        s("PASHR,XYZ,1,2"),
        s("PASHR,att,1,2"),
        s("PNORBT0,1,040721,131335.3341,23.961,-48.122,-32.76800,10.00000,0.00,0x00000000"),
        s("PNORBT4,1.234,-1.234,1.234,23.4,12.34567,12.3"),
        s("PNORBT7,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45"),
        s("PNORBT9,1452244916.7508,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF"),
        s("PNORWT4,1.2345,-1.2345,1.234,23.4,12.34,12.3"),
        s("PNORWT7,1452244916.0000005,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45"),
        s("PNORWT9,-86400.25,1.234,-1.234,0.1234,0.1234,0.1234,12.34,23.45,23.45,23.45,23.45,23.4,1567.8,1.2,12.3,0x000FFFFF"),
        s("PNORI1,4,123456,3,30,1.00,5.00,BEAM"),
        s("PNORS1,161109,132455,0,34000034,23.9,1500.0,123.4,0.02,45.6,0.02,23.4,0.02,123.456,0.02,24.56"),
        s("PNORS4,23.6,1530.2,0.0,0.0,0.0,0.000,23.30"),
        s("PNORC1,083013,132455,3,11.0,0.332,0.332,0.332,78.9,78.9,78.9,78,78,78"),
        s("PNORC4,1.5,1.395,227.1,32,32"),
        s("PNORH4,161109,143459,0,204C0002"),
        s("PNORXX,1,2"),
        s("PXYZ,1,2,3"),
        s("PFEC,GPatt,123.4,-1.2,0.5"),
        s("PASHR"),
        s("PSXN"),
    ]


def edge():
    good = s("GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000")
    return [
        good,
        good.replace("*6D", "*6E"),
        good.lower(),
        "$" + good[1:-3].lower() + "*%02x" % cs(good[1:-3].lower()),
        "$" + good[1:-3] + "*6d",
        "  " + good + " \t ",
        good[1:],
        "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000",
        "GPGLL,4916.45,N,12311.12,W,225444,A  ",
        good + "x",
        good[:-1],
        good + "D",
        "$$" + good[1:],
        "",
        "   ",
        "garbage",
        s("GPXYZ,1,2,3"),
        s("GPGGAX,1"),
        s("CCGPQ,GGA"),
        s("ccgpq,rmc"),
        s("CCGPQ,GGA,1"),
        s("G_GGA,1,2"),
        s("12RMC,1,2"),
        s("PGPGGA,1,2"),
        s("pgrme,15.0,M,45.0,M,25.0,M"),
        s("GPTXT,01,01,02,a") + "*b",
        "$GPTXT,01,01,02,a*b*00",
        s("GPTXT,01,01,02,tab\there"),
        s("GPTXT,01,01,02,it's \"quoted\""),
        s("GPTXT,01,01,02,back\\slash"),
        s("GPTXT,01,01,02,caf\xe9 \x7f\x01"),
        s("GPMWV,214.8,R,0.1,K,A") + "\x00",
        s("GPHDT,274.07,T,extra,fields,here"),
        s("GPHDT"),
        s("GPHDT,"),
        s("GPHDT,,"),
        "$GPHDT,274.07,T*03",
        s("GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E"),
    ]


def jobs():
    j = []
    for f in ("trip", "instruments", "devices", "edge"):
        j.append("parse %s.nmea" % f)
    j.append("strict edge.nmea")
    j.append("strict devices.nmea")
    j.append("attrs devices.nmea talker,manufacturer,sentence_type,listener,subtype,data")
    j.append("attrs edge.nmea talker,sentence_type,listener,manufacturer,timestamp,heading,nope")
    j.append("stream edge.nmea yield 23")
    j.append("stream edge.nmea ignore 50")
    j.append("stream edge.nmea raise 40")
    j.append("stream devices.nmea yield 400")
    j.append("stream instruments.nmea raise 1000")
    j.append("stream trip.nmea skip 10")
    j.append("streamfile trip.nmea yield 6")
    j.append("streamfile tail.nmea raise 4")
    j.append("file trip.nmea")
    j.append("file edge.nmea")
    j.append("fileread instruments.nmea")
    j.append("fileread devices.nmea")
    j.append("filelines tail.nmea 4")
    j.append("filenext tail.nmea 3")
    j.append("filenext cr.nmea 4")
    j.append("edit trip.nmea 8 lat=5046.0000 lat_dir=S spd_over_grnd=f:7.25 true_course=d:212.50 talker=GN")
    j.append("edit trip.nmea 9 gps_qual=i:4 num_sats=i:12 altitude=f:3.5 age_gps_data= ref_station_id=0042")
    j.append("edit trip.nmea 3 waypoint_list=SOLENT|NEEDLES active_route_id=WEST num_in_seq=i:1")
    j.append("edit instruments.nmea 17 waypoint_list=A|B|C")
    j.append("edit trip.nmea 8 nav_status=S latitude=f:1.0")
    j.append("edit trip.nmea 8 nav_status=S")
    j.append("edit instruments.nmea 46 true_course=f:1e-07 mode_indicator=A spd_over_grnd=i:3")
    j.append("edit devices.nmea 1 hpe=d:0.0000001 osepe_unit=F")
    j.append("edit devices.nmea 42 dt1=f:-0.0 stat=0x1 ")
    j.append("edit edge.nmea 19 sentence_type=RMC talker=II")
    j.append("edit instruments.nmea 13 talker_id_num=i:99 color=red")
    j.append("build GGA GP 184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000")
    j.append("build RMC GN 081836,A,3751.65,S,14507.36,E,000.0,360.0,130998,011.3,E")
    j.append("build XDR WI C,19.5,C,TempAir")
    j.append("build R00 GP EGLL,EGLM")
    j.append("build ZZZ GP 1,2")
    j.append("buildp GRM E,15.0,M,45.0,M,25.0,M")
    j.append("buildp GRM Q,1")
    j.append("buildp NOR BT4,1.0,2.0,3.0,4.0,5.0,6.0")
    j.append("buildp SXN ,23,0.30,-0.97,298.57,0.13")
    j.append("buildp TNL ,PJT,NAD83,Zone")
    j.append("buildp ASH R,130533.620,0.311,T")
    j.append("buildp XYZ A,B")
    j.append("query CC GP GGA")
    j.append("query II AP rmb")
    j.append("render trip.nmea 8")
    j.append("render devices.nmea 42")
    j.append("render edge.nmea 19")
    j.append("report trip.nmea")
    j.append("report instruments.nmea")
    j.append("gpx trip.nmea track.gpx")
    j.append("mux mux.nmea GN RMC,GGA,ZDA trip.nmea instruments.nmea edge.nmea")
    j.append("alarms trip.nmea instruments.nmea devices.nmea")
    return j


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    os.makedirs(os.path.join(DATA, "out"))

    def put(name, lines, nl):
        with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
            f.write("".join(l + nl for l in lines))

    put("trip.nmea", trip(), "\r\n")
    put("instruments.nmea", instruments(), "\n")
    put("devices.nmea", devices(), "\n")
    put("edge.nmea", edge(), "\r\n")
    with open(os.path.join(DATA, "tail.nmea"), "w", newline="") as f:
        f.write(s("GPHDT,274.07,T") + "\r\n" + s("GPHDM,272.4,M"))
    with open(os.path.join(DATA, "cr.nmea"), "w", newline="") as f:
        f.write(s("GPHDT,274.07,T") + "\r" + s("GPHDM,272.4,M") + "\r\r\n" + "$GPHDG,98.3,,,,\n")
    with open(os.path.join(DATA, "jobs.txt"), "w") as f:
        f.write("".join(l + "\n" for l in jobs()))


main()
