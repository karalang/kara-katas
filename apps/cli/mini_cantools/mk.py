"""Generate the inputs of mini_cantools: a vehicle DBC, a candump log of a
one-minute drive and charge, the codec jobs and some broken DBC files.

Everything is integer arithmetic over a fixed LCG, so the files are the
same on every run.  Run from the app directory: python3 -s -P -B mk.py
"""

import os

OUT = "data"

DBC = r'''VERSION "KV7-2026.10"


NS_ :
	NS_DESC_
	CM_
	BA_DEF_
	BA_
	VAL_
	BA_DEF_DEF_
	VAL_TABLE_
	BO_TX_BU_

BS_:

BU_: VCU BMS MCU OBC DASH GW

VAL_TABLE_ GearTable 4 "SPORT" 3 "DRIVE" 2 "NEUTRAL" 1 "REVERSE" 0 "PARK" ;
VAL_TABLE_ OnOff 1 "ON" 0 "OFF" ;


BO_ 256 VCU_Status: 8 VCU
 SG_ VehicleSpeed : 0|16@1+ (0.01,0) [0|250] "km/h" DASH,MCU
 SG_ Gear : 16|3@1+ (1,0) [0|4] "" DASH,MCU
 SG_ ReadyFlag : 19|1@1+ (1,0) [0|1] "" DASH
 SG_ DriveMode : 20|2@1+ (1,0) [0|2] "" DASH
 SG_ AccelPedal : 24|8@1+ (0.4,0) [0|100] "%" MCU
 SG_ BrakePressure : 32|12@1+ (0.1,0) [0|400] "bar" MCU
 SG_ Counter : 48|4@1+ (1,0) [0|15] "" GW
 SG_ Checksum : 63|8@0+ (1,0) [0|255] "" GW

BO_ 512 BMS_Pack: 8 BMS
 SG_ PackVoltage : 7|16@0+ (0.1,0) [0|900] "V" VCU,DASH
 SG_ PackCurrent : 23|16@0- (0.1,0) [-3276.8|3276.7] "A" VCU
 SG_ StateOfCharge : 39|8@0+ (0.5,0) [0|100] "%" VCU,DASH
 SG_ MaxCellTemp : 47|8@0+ (1,-40) [-40|125] "degC" VCU
 SG_ MinCellTemp : 55|8@0+ (1,-40) [-40|125] "degC" VCU
 SG_ PackState : 63|4@0+ (1,0) [0|5] "" VCU
 SG_ IsolationOk : 59|1@0+ (1,0) [0|1] "" VCU

BO_ 513 BMS_Cells: 8 BMS
 SG_ CellGroup M : 0|4@1+ (1,0) [0|3] "" VCU
 SG_ CellVoltA m0 : 8|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltB m0 : 24|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltC m0 : 40|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltD m1 : 8|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltE m1 : 24|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltF m1 : 40|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltG m2 : 8|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltH m2 : 24|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ CellVoltI m2 : 40|16@1+ (1,0) [0|5000] "mV" VCU
 SG_ BalanceMask m3 : 8|12@1+ (1,0) [0|0] "" VCU
 SG_ CellTempAvg m3 : 24|8@1+ (0.5,-20) [-20|107.5] "degC" VCU
 SG_ RollingCount : 60|4@1+ (1,0) [0|15] "" VCU

BO_ 768 MCU_Motor: 8 MCU
 SG_ MotorRpm : 0|16@1- (1,0) [-12000|12000] "rpm" VCU
 SG_ MotorTorque : 16|12@1- (0.5,0) [-1000|1000] "Nm" VCU
 SG_ InverterTemp : 28|8@1+ (1,-40) [-40|150] "degC" VCU
 SG_ MotorTemp : 36|8@1+ (1,-40) [-40|180] "degC" VCU,DASH
 SG_ FaultCode : 44|8@1+ (1,0) [0|255] "" VCU,DASH,GW
 SG_ DeratePct : 52|7@1+ (2.0,0) [0|100] "%" VCU

BO_ 2566869221 OBC_Charge: 8 OBC
 SG_ ChargerVoltage : 0|16@1+ (0.1,0) [0|1000] "V" BMS
 SG_ ChargerCurrent : 16|16@1+ (0.05,-1600) [-1600|1676.75] "A" BMS
 SG_ ChargeState : 32|3@1+ (1,0) [0|4] "" BMS,DASH
 SG_ TimeToFull : 40|16@1+ (1,0) [0|65534] "min" DASH
 SG_ PlugTemp : 56|8@1+ (1,-40) [-40|120] "degC" BMS

BO_ 1024 DASH_Odometer: 6 DASH
 SG_ Odometer : 0|32@1+ (0.1,0) [0|0] "km" GW
 SG_ TripA : 32|16@1+ (0.1,0) [0|6553.5] "km" GW

BO_ 2015 GW_Diag: 3 GW
 SG_ ServiceId : 0|8@1+ (1,0) [0|255] "" VCU,BMS,MCU
 SG_ Did : 15|16@0+ (1,0) [0|65535] "" VCU,BMS,MCU

BO_ 1792 TESTER_Ping: 2 Vector__XXX
 SG_ PingSeq : 0|8@1+ (1,0) [0|255] "" Vector__XXX
 SG_ PingFlags : 8|8@1+ (1,0) [0|0] "" Vector__XXX

BO_TX_BU_ 2015 : DASH,VCU;


CM_ "KV7 powertrain bus, 500 kbit/s";
CM_ BU_ VCU "Vehicle control unit";
CM_ BU_ BMS "Battery management system";
CM_ BU_ MCU "Motor control unit";
CM_ BO_ 256 "Driver demand and vehicle state";
CM_ BO_ 513 "Cell voltages, three per frame, and the thermal page";
CM_ SG_ 256 Checksum "Sum of bytes 0 to 6, inverted";
CM_ SG_ 512 PackCurrent "Positive while discharging";
CM_ SG_ 513 CellGroup "Selects what bytes 1 to 6 carry";
CM_ SG_ 768 FaultCode "Latched; cleared by \"key off\"";
BA_DEF_  "DBName" STRING ;
BA_DEF_  "BusType" STRING ;
BA_DEF_ BU_  "ECUAddress" HEX 0 255;
BA_DEF_ BO_  "GenMsgCycleTime" INT 0 10000;
BA_DEF_ BO_  "GenMsgSendType" ENUM  "Cyclic","Event","IfActive";
BA_DEF_ SG_  "GenSigStartValue" INT 0 100000;
BA_DEF_DEF_  "DBName" "";
BA_DEF_DEF_  "BusType" "CAN";
BA_DEF_DEF_  "ECUAddress" 0;
BA_DEF_DEF_  "GenMsgCycleTime" 0;
BA_DEF_DEF_  "GenMsgSendType" "Cyclic";
BA_DEF_DEF_  "GenSigStartValue" 0;
BA_ "DBName" "KV7_Powertrain";
BA_ "ECUAddress" BU_ VCU 16;
BA_ "ECUAddress" BU_ BMS 32;
BA_ "ECUAddress" BU_ MCU 48;
BA_ "GenMsgCycleTime" BO_ 256 100;
BA_ "GenMsgCycleTime" BO_ 512 100;
BA_ "GenMsgCycleTime" BO_ 513 250;
BA_ "GenMsgCycleTime" BO_ 768 50;
BA_ "GenMsgCycleTime" BO_ 2566869221 1000;
BA_ "GenMsgCycleTime" BO_ 1024 1000;
BA_ "GenMsgSendType" BO_ 2015 1;
BA_ "GenMsgSendType" BO_ 1792 2;
BA_ "GenSigStartValue" SG_ 768 MotorTemp 60;
BA_ "GenSigStartValue" SG_ 2566869221 TimeToFull 65535;
VAL_ 256 Gear 4 "SPORT" 3 "DRIVE" 2 "NEUTRAL" 1 "REVERSE" 0 "PARK" ;
VAL_ 256 DriveMode 2 "SNOW" 1 "NORMAL" 0 "ECO" ;
VAL_ 512 PackState 5 "SHUTDOWN" 4 "FAULT" 3 "CHARGE" 2 "DRIVE" 1 "STANDBY" 0 "INIT" ;
VAL_ 513 CellGroup 3 "THERMAL" 2 "CELLS_7_9" 1 "CELLS_4_6" 0 "CELLS_1_3" ;
VAL_ 768 FaultCode 17 "RESOLVER" 3 "UNDERVOLT" 2 "OVERTEMP" 1 "OVERCURRENT" 0 "NONE" ;
VAL_ 2566869221 ChargeState 4 "DONE" 3 "CV" 2 "CC" 1 "PRECHARGE" 0 "IDLE" ;
'''

# ---------------------------------------------------------------- packing

def put_le(buf, start, length, raw):
    """Little-endian (Intel) signal: start is the LSB's bit number."""
    if raw < 0:
        raw += 1 << length
    for i in range(length):
        bit = start + i
        if (raw >> i) & 1:
            buf[bit // 8] |= 1 << (bit % 8)


def put_be(buf, start, length, raw):
    """Big-endian (Motorola) signal: start is the MSB in sawtooth order."""
    if raw < 0:
        raw += 1 << length
    net = 8 * (start // 8) + 7 - start % 8
    for i in range(length):
        n = net + i
        if (raw >> (length - 1 - i)) & 1:
            buf[n // 8] |= 1 << (7 - n % 8)


class Rng:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def next(self):
        self.s = (self.s * 1103515245 + 12345) & 0xFFFFFFFF
        return self.s >> 8

    def jitter(self, span):
        return self.next() % (2 * span + 1) - span


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


# ---------------------------------------------------------------- the drive

T0 = 1729771200 * 1000000
END = 60 * 1000000


def speed_at(t):
    """Speed in 0.01 km/h at time t (microseconds)."""
    ms = t // 1000
    if ms < 4000:
        return 0
    if ms < 16000:
        return (ms - 4000) * 9000 // 12000
    if ms < 30000:
        ph = (ms - 16000) % 14000
        if ph < 7000:
            return 9000 - ph * 3 // 10
        return 6900 + (ph - 7000) * 3 // 10
    if ms < 40000:
        return 9000 - (ms - 30000) * 9000 // 10000
    return 0


def phase_at(t):
    ms = t // 1000
    if ms < 2000:
        return "off"
    if ms < 4000:
        return "ready"
    if ms < 40000:
        return "drive"
    if ms < 45000:
        return "park"
    return "charge"


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "vehicle.dbc"), "w") as f:
        f.write(DBC)

    rng = Rng(20261024)
    events = []  # (time, seq, id_text, data bytes)
    seq = [0]

    def emit(t, ident, ext, data):
        idt = f"{ident:08X}" if ext else f"{ident:03X}"
        events.append((t, seq[0], idt, bytes(data)))
        seq[0] += 1

    soc2 = 164  # state of charge in half percent
    odo = 1234567  # 0.1 km
    trip = 873
    dist_um = 0  # travelled distance in micrometres... in 0.01 km/h * us
    motor_temp = 62
    inv_temp = 58
    vcu_count = 0
    cell_page = 0
    cell_roll = 0
    fault = 0
    obc_state = 0

    # VCU_Status, 100 ms
    t = 7000
    k = 0
    while t < END:
        tt = t + rng.jitter(300)
        sp = speed_at(tt)
        ph = phase_at(tt)
        gear = {"off": 0, "ready": 0, "drive": 3, "park": 0, "charge": 0}[ph]
        if ph == "drive" and 30000000 <= tt < 40000000:
            gear = 3
        if ph == "drive" and 18000000 <= tt < 24000000:
            gear = 4
        ready = 0 if ph in ("off", "charge") else 1
        mode = 1 if tt < 20000000 else 0
        if ph == "drive" and speed_at(tt + 100000) > sp:
            pedal = clamp(60 + (sp // 60) + rng.jitter(8), 0, 250)
        elif ph == "drive" and speed_at(tt + 100000) == sp:
            pedal = clamp(40 + rng.jitter(5), 0, 250)
        else:
            pedal = 0
        brake = clamp(1800 + rng.jitter(150), 0, 4000) if (ph == "drive" and tt >= 30000000) else 0
        buf = bytearray(8)
        put_le(buf, 0, 16, sp)
        put_le(buf, 16, 3, gear)
        put_le(buf, 19, 1, ready)
        put_le(buf, 20, 2, mode)
        put_le(buf, 24, 8, pedal)
        put_le(buf, 32, 12, brake)
        cnt = vcu_count % 16
        if k == 211:
            cnt = (cnt + 1) % 16  # a skipped counter value
            vcu_count += 1
        put_le(buf, 48, 4, cnt)
        vcu_count += 1
        if k == 377:
            buf[2] |= 0x40  # a stray bit in the unused part of byte 2
        csum = (~sum(buf[0:7])) & 0xFF
        if k == 452:
            csum ^= 0x10  # a corrupted checksum
        put_be(buf, 63, 8, csum)
        emit(tt, 0x100, False, buf)
        t += 100000
        k += 1

    # BMS_Pack, 100 ms
    t = 20000
    k = 0
    volt = 3712
    while t < END:
        tt = t + rng.jitter(250)
        ph = phase_at(tt)
        sp = speed_at(tt)
        if ph == "drive":
            nxt = speed_at(tt + 100000)
            if nxt > sp:
                cur = 900 + sp // 8 + rng.jitter(40)
            elif nxt == sp:
                cur = 260 + sp // 30 + rng.jitter(30)
            else:
                cur = -(300 + sp // 20) + rng.jitter(30)
        elif ph == "charge":
            ms = tt // 1000
            cur = -60 if ms < 46000 else -1100 + rng.jitter(10)
        elif ph == "off":
            cur = 3 + rng.jitter(2)
        else:
            cur = 18 + rng.jitter(4)
        if k % 25 == 0 and cur > 0:
            soc2 -= 1
        if ph == "charge" and k % 30 == 0:
            soc2 += 1
        v = volt - cur // 12 + rng.jitter(3)
        st = {"off": 1, "ready": 2, "drive": 2, "park": 1, "charge": 3}[ph]
        buf = bytearray(8)
        put_be(buf, 7, 16, v)
        put_be(buf, 23, 16, cur)
        put_be(buf, 39, 8, soc2)
        put_be(buf, 47, 8, 40 + 29 + (tt // 6000000))
        put_be(buf, 55, 8, 40 + 24 + (tt // 15000000))
        put_be(buf, 63, 4, st)
        put_be(buf, 59, 1, 1)
        data = buf
        if k == 333:
            data = buf[:5]  # a frame cut short on the bus
        emit(tt, 0x200, False, data)
        t += 100000
        k += 1

    # BMS_Cells, 250 ms, cycling its four pages
    t = 40000
    k = 0
    base = [3671, 3668, 3675, 3662, 3670, 3673, 3659, 3669, 3666]
    while t < END:
        tt = t + rng.jitter(300)
        page = cell_page % 4
        ph = phase_at(tt)
        sag = 0
        if ph == "drive":
            sag = speed_at(tt) // 300 + 6
        if ph == "charge":
            sag = -25
        buf = bytearray(8)
        put_le(buf, 0, 4, page)
        if page < 3:
            for j in range(3):
                mv = base[page * 3 + j] - sag + rng.jitter(2)
                if page == 2 and j == 0 and ph == "drive":
                    mv -= 31  # the weak cell
                put_le(buf, 8 + 16 * j, 16, mv)
        else:
            put_le(buf, 8, 12, (0x041 if ph == "charge" else 0x000) | (rng.next() % 2) << 8)
            put_le(buf, 24, 8, 2 * (27 + tt // 10000000) + 40 + (rng.next() % 2))
        put_le(buf, 60, 4, cell_roll % 16)
        if k == 101:
            buf[0] = (buf[0] & 0xF0) | 9  # a page number the DBC does not know
        emit(tt, 0x201, False, buf)
        cell_page += 1
        cell_roll += 1
        t += 250000
        k += 1

    # MCU_Motor, 50 ms
    t = 5000
    k = 0
    while t < END:
        tt = t + rng.jitter(150)
        ph = phase_at(tt)
        sp = speed_at(tt)
        rpm = sp * 96 // 100
        if ph == "drive" and 30000000 <= tt < 40000000 and sp > 0:
            torque = -(120 + sp // 50) + rng.jitter(6)
        elif ph == "drive" and speed_at(tt + 50000) > sp:
            torque = 420 + rng.jitter(20)
        elif ph == "drive" and sp > 0:
            torque = 140 + rng.jitter(12)
        else:
            torque = 0
        if k % 40 == 0 and ph == "drive":
            motor_temp += 1
            inv_temp += 1 if k % 80 == 0 else 0
        if ph == "charge" and k % 60 == 0:
            motor_temp -= 1
        if 25000000 <= tt < 27500000:
            fault = 2
            derate = 30
        elif tt >= 27500000:
            fault = 0
            derate = 0
        else:
            derate = 0
        mt = motor_temp
        if k == 620:
            mt = 190  # a sensor spike above the DBC maximum
        buf = bytearray(8)
        put_le(buf, 0, 16, rpm)
        put_le(buf, 16, 12, torque)
        put_le(buf, 28, 8, inv_temp + 40)
        put_le(buf, 36, 8, mt + 40)
        put_le(buf, 44, 8, fault)
        put_le(buf, 52, 7, derate // 2)
        emit(tt, 0x300, False, buf)
        t += 50000
        k += 1

    # OBC_Charge, 1 s, extended id
    t = 500000
    while t < END:
        tt = t + rng.jitter(500)
        ms = tt // 1000
        if ms < 45000:
            vv, cc, stt, ttf, pt = 0, 32000, 0, 65535, 21
        elif ms < 47000:
            vv, cc, stt, ttf, pt = 3650, 32000 + 120, 1, 65535, 22
        else:
            vv, cc, stt, ttf, pt = 3725, 32000 + 2200, 2, 96 - (ms - 47000) // 1000, 23 + (ms - 47000) // 4000
        buf = bytearray(8)
        put_le(buf, 0, 16, vv)
        put_le(buf, 16, 16, cc)
        put_le(buf, 32, 3, stt)
        put_le(buf, 40, 16, ttf)
        put_le(buf, 56, 8, pt + 40)
        emit(tt, 0x18FF50E5, True, buf)
        t += 1000000

    # DASH_Odometer, 1 s
    t = 700000
    last = 0
    while t < END:
        tt = t + rng.jitter(400)
        # integrate speed: 0.01 km/h over microseconds -> 0.1 km
        for u in range(last, tt, 10000):
            dist_um += speed_at(u) * 10000
        last = tt
        tenths = dist_um // (360 * 1000000 * 1000 // 10)
        buf = bytearray(6)
        put_le(buf, 0, 32, odo + tenths)
        put_le(buf, 32, 16, trip + tenths)
        emit(tt, 0x400, False, buf)
        t += 1000000

    # GW_Diag requests and the ECU responses on an id the DBC lacks
    for tt, sid, did in [(10002113, 0x22, 0xF190), (10503877, 0x22, 0xF18C), (33300410, 0x19, 0x0209)]:
        buf = bytearray(3)
        put_le(buf, 0, 8, sid)
        put_be(buf, 15, 16, did)
        emit(tt, 0x7DF, False, buf)
        emit(tt + 4810, 0x7E8, False, bytes([0x62, did >> 8, did & 0xFF, 0x4B, 0x56, 0x37]))

    # A body-controller frame this DBC does not describe, every 5 s
    t = 1250000
    while t < END:
        emit(t + rng.jitter(500), 0x3A0, False, bytes([0x01, 0x00, rng.next() % 256, 0x00]))
        t += 5000000

    # A tester ping, once
    emit(51234567, 0x700, False, bytes([0x2A, 0x00]))

    events.sort(key=lambda e: (e[0], e[1]))
    lines = []
    for tt, _, idt, data in events:
        lines.append(f"({(T0 + tt) // 1000000}.{(T0 + tt) % 1000000:06d}) can0 {idt}#{data.hex().upper()}")
    # Damage on the logger's side: a line cut mid-write and a bad hex digit.
    lines.insert(812, lines[812][:31])
    lines.insert(2040, lines[2040].replace("#", "#G", 1))
    with open(os.path.join(OUT, "drive.log"), "w") as f:
        f.write("\n".join(lines) + "\n")

    # ------------------------------------------------------------ the jobs
    jobs = [
        "encode VCU_Status VehicleSpeed=88.5 Gear='DRIVE' ReadyFlag=1 DriveMode='ECO' AccelPedal=36.4 BrakePressure=0 Counter=7 Checksum=0",
        "encode VCU_Status VehicleSpeed=88 Gear=3 ReadyFlag=1 DriveMode=0 AccelPedal=36 BrakePressure=0.0 Counter=12.5 Checksum=255",
        "encode VCU_Status -pad VehicleSpeed=0 Gear='PARK' ReadyFlag=0 DriveMode='NORMAL' AccelPedal=0 BrakePressure=12.3 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=251 Gear='DRIVE' ReadyFlag=1 DriveMode='ECO' AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=-0.5 Gear='DRIVE' ReadyFlag=1 DriveMode='ECO' AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=250.000001 Gear='DRIVE' ReadyFlag=1 DriveMode='ECO' AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=10 Gear='TURBO' ReadyFlag=1 DriveMode='ECO' AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=10 Gear='DRIVE' ReadyFlag=1 AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status VehicleSpeed=10 Gear='DRIVE' ReadyFlag=1 DriveMode=1 AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0 Horn=1",
        "encode VCU_Status -noscale VehicleSpeed=8850 Gear=3 ReadyFlag=1 DriveMode=0 AccelPedal=91 BrakePressure=0 Counter=7 Checksum=0",
        "encode VCU_Status -noscale VehicleSpeed=26000 Gear=3 ReadyFlag=1 DriveMode=0 AccelPedal=91 BrakePressure=0 Counter=7 Checksum=0",
        "encode VCU_Status -loose VehicleSpeed=700 Gear=3 ReadyFlag=1 DriveMode=0 AccelPedal=91 BrakePressure=0 Counter=7 Checksum=0",
        "encode VCU_Status -loose VehicleSpeed=10 Gear=9 ReadyFlag=1 DriveMode=0 AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode VCU_Status -loose VehicleSpeed=10 Gear=3 ReadyFlag=1 AccelPedal=0 BrakePressure=0 Counter=0 Checksum=0",
        "encode BMS_Pack PackVoltage=371.2 PackCurrent=-112.5 StateOfCharge=81.5 MaxCellTemp=29 MinCellTemp=24 PackState='DRIVE' IsolationOk=1",
        "encode BMS_Pack -pad PackVoltage=371.2 PackCurrent=0.1 StateOfCharge=81 MaxCellTemp=25.5 MinCellTemp=-40 PackState='CHARGE' IsolationOk=0",
        "encode BMS_Pack PackVoltage=371.2 PackCurrent=-3276.8 StateOfCharge=100 MaxCellTemp=125 MinCellTemp=-40.5 PackState=5 IsolationOk=1",
        "encode BMS_Pack PackVoltage=371.2 PackCurrent=3276.7 StateOfCharge=0.25 MaxCellTemp=24.5 MinCellTemp=-39.5 PackState=4 IsolationOk=1",
        "encode BMS_Pack -noscale PackVoltage=3712 PackCurrent=-1125 StateOfCharge=163 MaxCellTemp=69 MinCellTemp=64 PackState=2 IsolationOk=1",
        "encode BMS_Pack -loose PackVoltage=371.2 PackCurrent=-3300 StateOfCharge=81 MaxCellTemp=29 MinCellTemp=24 PackState=2 IsolationOk=1",
        "encode BMS_Cells CellGroup=0 CellVoltA=3671 CellVoltB=3668 CellVoltC=3675 RollingCount=3",
        "encode BMS_Cells CellGroup='THERMAL' BalanceMask=65 CellTempAvg=33.5 RollingCount=15",
        "encode BMS_Cells -pad CellGroup='CELLS_4_6' CellVoltD=3662 CellVoltE=3670 CellVoltF=3673 RollingCount=0",
        "encode BMS_Cells CellGroup=4 CellVoltA=3671 CellVoltB=3668 CellVoltC=3675 RollingCount=3",
        "encode BMS_Cells CellGroup=1 CellVoltA=3671 CellVoltB=3668 CellVoltC=3675 RollingCount=3",
        "encode BMS_Cells CellGroup=2 CellVoltG=3659 CellVoltH=3669 RollingCount=3",
        "encode BMS_Cells CellGroup='CELLS_7_9' CellVoltG=3659 CellVoltH=3669 CellVoltI=5001 RollingCount=3",
        "encode BMS_Cells -loose CellGroup=7 CellVoltA=1 RollingCount=1",
        "encode BMS_Cells CellGroup='THERMAL' BalanceMask=4096 CellTempAvg=33.5 RollingCount=15",
        "encode BMS_Cells -loose CellGroup='THERMAL' BalanceMask=4096 CellTempAvg=33.5 RollingCount=15",
        "encode MCU_Motor MotorRpm=-850 MotorTorque=-62.5 InverterTemp=58 MotorTemp=63 FaultCode='NONE' DeratePct=0",
        "encode MCU_Motor MotorRpm=8640 MotorTorque=210 InverterTemp=61 MotorTemp=71 FaultCode='OVERTEMP' DeratePct=37",
        "encode MCU_Motor MotorRpm=8640 MotorTorque=210 InverterTemp=61 MotorTemp=71 FaultCode=99 DeratePct=38.0",
        "encode MCU_Motor MotorRpm=8640.5 MotorTorque=210.25 InverterTemp=61 MotorTemp=71 FaultCode=17 DeratePct=39",
        "encode MCU_Motor -noscale MotorRpm=-1 MotorTorque=-1 InverterTemp=0 MotorTemp=255 FaultCode=2 DeratePct=127",
        "encode MCU_Motor MotorRpm=12001 MotorTorque=0 InverterTemp=61 MotorTemp=71 FaultCode=0 DeratePct=0",
        "encode MCU_Motor -loose MotorRpm=-40000 MotorTorque=0 InverterTemp=61 MotorTemp=71 FaultCode=0 DeratePct=0",
        "encode MCU_Motor -loose MotorRpm=0 MotorTorque=1100 InverterTemp=61 MotorTemp=71 FaultCode=0 DeratePct=0",
        "encode MCU_Motor -loose MotorRpm=0 MotorTorque=0 InverterTemp=61 MotorTemp=71 FaultCode='SMOKE' DeratePct=0",
        "encode OBC_Charge ChargerVoltage=372.5 ChargerCurrent=110 ChargeState='CC' TimeToFull=96 PlugTemp=23",
        "encode OBC_Charge ChargerVoltage=0 ChargerCurrent=-1600 ChargeState='IDLE' TimeToFull=65534 PlugTemp=-40",
        "encode OBC_Charge ChargerVoltage=0 ChargerCurrent=0.025 ChargeState='IDLE' TimeToFull=0 PlugTemp=0",
        "encode OBC_Charge ChargerVoltage=0 ChargerCurrent=0.075 ChargeState=4 TimeToFull=0 PlugTemp=120.4",
        "encode DASH_Odometer Odometer=123456.7 TripA=87.3",
        "encode DASH_Odometer -pad Odometer=429496729.5 TripA=6553.5",
        "encode DASH_Odometer Odometer=-1 TripA=0",
        "encode DASH_Odometer -loose Odometer=-1 TripA=0",
        "encode GW_Diag ServiceId=34 Did=61840",
        "encode GW_Diag -pad ServiceId=25 Did=521",
        "encode TESTER_Ping PingSeq=42 PingFlags=3",
        "encode Wiper_Status Speed=1",
        "decode 0x100 2A22030E00000700",
        "decode 0x100 2A22030E00000700 -nochoices",
        "decode 0x100 2A22030E00000700 -noscale",
        "decode 0x100 2A22030E00000700 -nochoices -noscale",
        "decode 0x100 FFFFFFFFFFFFFFFF",
        "decode 0x100 2A2203 -trunc",
        "decode 0x100 2A22030E0000 -trunc",
        "decode 0x100 2A2203",
        "decode 0x100 2A22030E0000070011223344",
        "decode 0x200 0E80FB9AA3453C21",
        "decode 0x200 0E80FB9AA3453C21 -noscale",
        "decode 0x200 FFFF8000C8A5000F",
        "decode 0x200 0E80FB9AA3 -trunc",
        "decode 0x200 0E80FB -trunc",
        "decode 0x201 F0570E540E5B0E00",
        "decode 0x201 F3411001670000F0",
        "decode 0x201 F3411001670000F0 -nochoices",
        "decode 0x201 F3411001670000F0 -noscale",
        "decode 0x201 0E570E540E5B0E00",
        "decode 0x201 01 -trunc",
        "decode 0x201 F1 -trunc",
        "decode 0x201 F2 -trunc",
        "decode 0x300 AEFC830EBF46C000",
        "decode 0x300 C021A4E1F11D6302",
        "decode 0x300 C021A4E1F1D06312",
        "decode 0x300 C021A4E1F1D06312 -nochoices",
        "decode 0x18FF50E5 8D0E30860200FF3F",
        "decode 0x18FF50E5 0000007D0060FFFF",
        "decode OBC_Charge 0000007D0060FFFF",
        "decode 0x400 87D61200690300",
        "decode 0x400 FFFFFFFFFFFF",
        "decode 0x7DF 22F190",
        "decode 0x7DF 22F19000",
        "decode 0x700 2A03",
        "decode 0x7E8 62F1904B5637",
        "decode Wiper_Status 00",
    ]
    with open(os.path.join(OUT, "jobs.txt"), "w") as f:
        f.write("\n".join(jobs) + "\n")

    # ------------------------------------------------------------ broken DBCs
    head = 'VERSION ""\n\nNS_ :\n\nBS_:\n\nBU_: ECU\n\n'
    bad = {
        "overlap": head + "BO_ 300 Lamp: 2 ECU\n SG_ Left : 0|6@1+ (1,0) [0|63] \"\" ECU\n SG_ Right : 4|6@1+ (1,0) [0|63] \"\" ECU\n",
        "overlap_be": head + "BO_ 301 Lamp: 2 ECU\n SG_ Head : 7|8@0+ (1,0) [0|0] \"\" ECU\n SG_ Fog : 0|4@1+ (1,0) [0|0] \"\" ECU\n",
        "nofit": head + "BO_ 302 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"\" ECU\n SG_ Right : 12|8@1+ (1,0) [0|0] \"\" ECU\n",
        "nofit_be": head + "BO_ 303 Lamp: 2 ECU\n SG_ Left : 7|8@0+ (1,0) [0|0] \"\" ECU\n SG_ Right : 13|12@0+ (1,0) [0|0] \"\" ECU\n",
        "zero_length": head + "BO_ 304 Lamp: 2 ECU\n SG_ Left : 0|0@1+ (1,0) [0|0] \"\" ECU\n",
        "std_id": head + "BO_ 2048 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"\" ECU\n",
        "ext_id": head + "BO_ 3758096384 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"\" ECU\n",
        "mux_overlap": head + "BO_ 305 Lamp: 4 ECU\n SG_ Page M : 0|4@1+ (1,0) [0|0] \"\" ECU\n SG_ A m0 : 8|8@1+ (1,0) [0|0] \"\" ECU\n SG_ B m1 : 8|8@1+ (1,0) [0|0] \"\" ECU\n SG_ C m1 : 12|8@1+ (1,0) [0|0] \"\" ECU\n",
        "syntax": head + "BO_ 306 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"\" ECU\n SG_ Right : 8 8@1+ (1,0) [0|0] \"\" ECU\n",
        "string": head + "BO_ 307 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"\" ECU\nCM_ BO_ 307 \"never closed;\n",
        "char": head + "BO_ 308 Lamp: 2 ECU\n SG_ Left : 0|8@1+ (1,0) [0|0] \"%\" ECU\n SG_ Right : 8|8@1+ (1,0) [0|0] \"\" ECU#2\n",
    }
    for name, text in bad.items():
        with open(os.path.join(OUT, f"bad_{name}.dbc"), "w") as f:
            f.write(text)


main()
