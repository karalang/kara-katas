"""Oracle for mini_pymodbus: plays data/jobs.txt through the vendored
pymodbus 3.6.9 and prints what a client and a server on one bus see.

The library is used as is. What this file adds is the bus: a server that
owns a framer and a datastore context and runs each decoded request the
way pymodbus's async server does (server/async_io.py, `_async_execute`,
which is not vendored because it needs a transport), and a client that
owns its own framer and prints every response it decodes.

Run: python3 -I -B oracle.py > expected.out
"""
import asyncio
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from pymodbus import bit_read_message as brm  # noqa: E402
from pymodbus import bit_write_message as bwm  # noqa: E402
from pymodbus import diag_message as dgm  # noqa: E402
from pymodbus import file_message as flm  # noqa: E402
from pymodbus import mei_message as mei  # noqa: E402
from pymodbus import other_message as otm  # noqa: E402
from pymodbus import register_read_message as rrm  # noqa: E402
from pymodbus import register_write_message as rwm  # noqa: E402
from pymodbus.datastore import (  # noqa: E402
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
    ModbusSparseDataBlock,
)
from pymodbus.device import ModbusControlBlock, ModbusDeviceIdentification  # noqa: E402
from pymodbus.events import (  # noqa: E402
    CommunicationRestartEvent,
    EnteredListenModeEvent,
    RemoteReceiveEvent,
    RemoteSendEvent,
)
from pymodbus.exceptions import NoSuchSlaveException  # noqa: E402
from pymodbus.factory import ClientDecoder, ServerDecoder  # noqa: E402
from pymodbus.framer import (  # noqa: E402
    ModbusAsciiFramer,
    ModbusRtuFramer,
    ModbusSocketFramer,
)
from pymodbus.message.ascii import MessageAscii  # noqa: E402
from pymodbus.message.rtu import MessageRTU  # noqa: E402
from pymodbus.pdu import ModbusExceptions as merror  # noqa: E402
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder  # noqa: E402

MCB = ModbusControlBlock()
LOOP = asyncio.new_event_loop()
FRAMERS = {"socket": ModbusSocketFramer, "rtu": ModbusRtuFramer, "ascii": ModbusAsciiFramer}
STORES = {"d": "di", "c": "co", "i": "ir", "h": "hr"}
COUNTERS = ["BusMessage", "BusCommunicationError", "BusExceptionError", "SlaveMessage",
            "SlaveNoResponse", "SlaveNAK", "SlaveBusy", "BusCharacterOverrun", "Event"]


# ------------------------------------------------------------ printing

def text(token):
    """A token with ~XX escapes as bytes."""
    out = bytearray()
    i = 0
    raw = token.encode()
    while i < len(raw):
        if raw[i] == 0x7E and i + 2 < len(raw):
            out.append(int(raw[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(raw[i])
            i += 1
    return bytes(out)


def wire(framer, data):
    if framer == "ascii":
        return data.decode("latin-1").replace("\r", "<CR>").replace("\n", "<LF>")
    return data.hex()


def bitstr(bits):
    return "".join("1" if b else "0" for b in bits)


def ename(exc):
    name = type(exc).__name__
    if isinstance(exc, struct.error):
        return "struct.error"
    if name == "Error":
        return "binascii.Error"
    return name


def has_str(obj):
    return type(obj).__str__ is not object.__str__


def label(msg):
    name = type(msg).__name__
    if has_str(msg):
        return f"{name}: {msg}"
    return name


def fields(msg):
    n = type(msg).__name__
    if n.startswith("Read") and n.endswith("Request") and hasattr(msg, "count") and n != "ReadWriteMultipleRegistersRequest":
        return f"address={msg.address} count={msg.count}"
    if n in ("ReadCoilsResponse", "ReadDiscreteInputsResponse"):
        return f"bits={bitstr(msg.bits)}"
    if n in ("ReadHoldingRegistersResponse", "ReadInputRegistersResponse", "ReadWriteMultipleRegistersResponse"):
        return f"registers={msg.registers}"
    if n in ("WriteSingleCoilRequest", "WriteSingleCoilResponse", "WriteSingleRegisterRequest",
             "WriteSingleRegisterResponse"):
        return f"address={msg.address} value={msg.value}"
    if n == "WriteMultipleCoilsRequest":
        return f"address={msg.address} byte_count={msg.byte_count} values={bitstr(msg.values)}"
    if n == "WriteMultipleRegistersRequest":
        return f"address={msg.address} count={msg.count} byte_count={msg.byte_count} values={msg.values}"
    if n in ("WriteMultipleCoilsResponse", "WriteMultipleRegistersResponse"):
        return f"address={msg.address} count={msg.count}"
    if n in ("MaskWriteRegisterRequest", "MaskWriteRegisterResponse"):
        return f"address={msg.address} and_mask={msg.and_mask:#06x} or_mask={msg.or_mask:#06x}"
    if n == "ReadWriteMultipleRegistersRequest":
        return (f"read={msg.read_address}+{msg.read_count} write={msg.write_address}+{msg.write_count}"
                f" byte_count={msg.write_byte_count} values={msg.write_registers}")
    if isinstance(msg, (dgm.DiagnosticStatusRequest, dgm.DiagnosticStatusResponse)):
        return f"sub={msg.sub_function_code:#06x} message={msg.message!r}"
    if n == "ReadExceptionStatusResponse":
        return f"status={msg.status:#04x}"
    if n == "GetCommEventCounterResponse":
        return f"status={msg.status} count={msg.count}"
    if n == "GetCommEventLogResponse":
        return (f"status={msg.status} events={msg.event_count} messages={msg.message_count}"
                f" log={[hex(e) for e in msg.events]}")
    if n == "ReportSlaveIdResponse":
        return f"byte_count={msg.byte_count}"
    if n in ("ReadFileRecordRequest", "ReadFileRecordResponse", "WriteFileRecordRequest",
             "WriteFileRecordResponse"):
        return "records=[" + ", ".join(f"{r!r} data={r.record_data!r}" for r in msg.records) + "]"
    if n == "ReadFifoQueueRequest":
        return f"address={msg.address}"
    if n == "ReadFifoQueueResponse":
        return f"values={msg.values}"
    if n == "ReadDeviceInformationRequest":
        return f"read_code={msg.read_code} object_id={msg.object_id:#04x}"
    if n == "ReadDeviceInformationResponse":
        objs = []
        for oid, val in msg.information.items():
            objs.append(f"{oid:#04x}={val!r}")
        return (f"read_code={msg.read_code} conformity={msg.conformity:#04x} more={msg.more_follows:#04x}"
                f" next={msg.next_object_id:#04x} objects={msg.number_of_objects} {{{', '.join(objs)}}}")
    if n == "ExceptionResponse":
        return f"exception_code={msg.exception_code}"
    if n == "IllegalFunctionRequest":
        return f"function_code={msg.function_code}"
    return ""


def show(prefix, msg):
    f = fields(msg)
    line = f"{prefix} {label(msg)}"
    if f:
        line += " | " + f
    print(line)


# ------------------------------------------------------------ the bus

class Bus:
    def __init__(self, kind, multi, broadcast, ignore):
        self.kind = kind
        self.multi = multi
        self.broadcast = broadcast
        self.ignore = ignore
        self.context = ModbusServerContext(slaves={} if multi else None, single=not multi)
        self.server = FRAMERS[kind](ServerDecoder())
        self.client = FRAMERS[kind](ClientDecoder())
        self.tid = 0

    def slaves(self):
        slaves = self.context.slaves()
        if self.broadcast and 0 not in slaves:
            slaves.append(0)
        return slaves

    def to_server(self, data, chunk):
        got = []
        pieces = [data] if chunk <= 0 else [data[i:i + chunk] for i in range(0, len(data), chunk)]
        closed = None
        for piece in pieces:
            try:
                self.server.processIncomingPacket(
                    data=piece, callback=got.append, slave=self.slaves(), single=self.context.single)
            except Exception as exc:  # pylint: disable=broad-except
                closed = exc
                break
        replies = []
        for request in got:
            show("  server got", request)
            reply = self.execute(request)
            if reply is not None:
                replies.append(reply)
        if closed is not None:
            print(f"  ! server closed the connection: {ename(closed)}: {closed}")
            self.server = FRAMERS[self.kind](ServerDecoder())
        for reply in replies:
            print(f"  rx {wire(self.kind, reply)}")
            self.to_client(reply)
        if not got and closed is None:
            print("  (server is waiting for more)")

    def execute(self, request):
        """pymodbus server/async_io.py ModbusServerRequestHandler._async_execute."""
        broadcast = False
        try:
            if self.broadcast and not request.slave_id:
                broadcast = True
                for slave_id in self.context.slaves():
                    response = self.run(request, self.context[slave_id])
            else:
                context = self.context[request.slave_id]
                response = self.run(request, context)
        except NoSuchSlaveException:
            if self.ignore:
                print("  (no such slave, no reply)")
                return None
            response = request.doException(merror.GatewayNoResponse)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"  ! datastore: {ename(exc)}")
            response = request.doException(merror.SlaveFailure)
        if broadcast:
            print("  (broadcast, no reply)")
            return None
        response.transaction_id = request.transaction_id
        response.slave_id = request.slave_id
        if not response.should_respond:
            print(f"  (no reply: {type(response).__name__})")
            return None
        try:
            return self.server.buildPacket(response)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"  ! reply not sent: {ename(exc)}")
            return None

    def run(self, request, context):
        async def call():
            return await request.execute(context)
        return LOOP.run_until_complete(call())

    def to_client(self, data):
        try:
            self.client.processIncomingPacket(data, lambda r: show("  client got", r), slave=0)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"  ! client: {ename(exc)}: {exc}")


# ------------------------------------------------------------ requests

def ints(token):
    if token == "-":
        return []
    return [int(x, 0) for x in token.split(",")]


def records(token):
    out = []
    for part in token.split(";"):
        f = part.split(":")
        if not f[2].startswith("h"):
            out.append(flm.FileRecord(file_number=int(f[0]), record_number=int(f[1]), record_length=int(f[2])))
        else:
            data = bytes.fromhex(f[2][1:])
            out.append(flm.FileRecord(file_number=int(f[0]), record_number=int(f[1]), record_data=data))
    return out


DIAG = {
    0x02: dgm.ReturnDiagnosticRegisterRequest, 0x03: dgm.ChangeAsciiInputDelimiterRequest,
    0x04: dgm.ForceListenOnlyModeRequest, 0x0A: dgm.ClearCountersRequest,
    0x0B: dgm.ReturnBusMessageCountRequest, 0x0C: dgm.ReturnBusCommunicationErrorCountRequest,
    0x0D: dgm.ReturnBusExceptionErrorCountRequest, 0x0E: dgm.ReturnSlaveMessageCountRequest,
    0x0F: dgm.ReturnSlaveNoResponseCountRequest, 0x10: dgm.ReturnSlaveNAKCountRequest,
    0x11: dgm.ReturnSlaveBusyCountRequest, 0x12: dgm.ReturnSlaveBusCharacterOverrunCountRequest,
    0x13: dgm.ReturnIopOverrunCountRequest, 0x14: dgm.ClearOverrunCountRequest,
    0x15: dgm.GetClearModbusPlusRequest,
}


def make_request(op, args, kw):
    if op in ("rc", "rdi", "rhr", "rir"):
        cls = {"rc": brm.ReadCoilsRequest, "rdi": brm.ReadDiscreteInputsRequest,
               "rhr": rrm.ReadHoldingRegistersRequest, "rir": rrm.ReadInputRegistersRequest}[op]
        return cls(int(args[0], 0), int(args[1], 0), **kw)
    if op == "wc":
        return bwm.WriteSingleCoilRequest(int(args[0], 0), int(args[1], 0), **kw)
    if op == "wr":
        return rwm.WriteSingleRegisterRequest(int(args[0], 0), int(args[1], 0), **kw)
    if op == "wcs":
        return bwm.WriteMultipleCoilsRequest(int(args[0], 0), [c == "1" for c in args[1]], **kw)
    if op == "wrs":
        return rwm.WriteMultipleRegistersRequest(int(args[0], 0), ints(args[1]), **kw)
    if op == "mask":
        return rwm.MaskWriteRegisterRequest(int(args[0], 0), int(args[1], 0), int(args[2], 0), **kw)
    if op == "rw":
        return rrm.ReadWriteMultipleRegistersRequest(
            read_address=int(args[0], 0), read_count=int(args[1], 0),
            write_address=int(args[2], 0), write_registers=ints(args[3]), **kw)
    if op == "diag":
        sub = int(args[0], 0)
        if sub == 0x00:
            return dgm.ReturnQueryDataRequest(text(args[1]) if len(args) > 1 else b"\x00\x00", **kw)
        if sub == 0x01:
            return dgm.RestartCommunicationsOptionRequest(int(args[1], 0) != 0, **kw)
        return DIAG[sub](data=int(args[1], 0) if len(args) > 1 else 0x0000, **kw)
    if op == "exc":
        return otm.ReadExceptionStatusRequest(**kw)
    if op == "evc":
        return otm.GetCommEventCounterRequest(**kw)
    if op == "evl":
        return otm.GetCommEventLogRequest(**kw)
    if op == "sid":
        return otm.ReportSlaveIdRequest(**kw)
    if op == "fifo":
        return flm.ReadFifoQueueRequest(int(args[0], 0), **kw)
    if op == "rfr":
        return flm.ReadFileRecordRequest(records(args[0]), **kw)
    if op == "wfr":
        return flm.WriteFileRecordRequest(records(args[0]), **kw)
    if op == "mei":
        return mei.ReadDeviceInformationRequest(int(args[0], 0), int(args[1], 0), **kw)
    raise ValueError(op)


# ------------------------------------------------------------ payloads

ORDER = {"big": ">", "little": "<"}


def payload_step(state, words):
    cmd = words[0]
    if cmd == "build":
        state["b"] = BinaryPayloadBuilder(byteorder=ORDER[words[1]], wordorder=ORDER[words[2]],
                                          repack=len(words) > 3 and words[3] == "repack")
        return
    if cmd == "add":
        b = state["b"]
        kind, val = words[1], words[2]
        try:
            if kind == "bits":
                b.add_bits([c == "1" for c in val])
            elif kind == "str":
                b.add_string(text(val).decode("latin-1"))
            elif kind.startswith("f"):
                getattr(b, f"add_{kind[1:]}bit_float")(float(val))
            elif kind.startswith("u"):
                getattr(b, f"add_{kind[1:]}bit_uint")(int(val, 0))
            else:
                getattr(b, f"add_{kind[1:]}bit_int")(int(val, 0))
        except (struct.error, OverflowError) as exc:
            print(f"  ! add {kind} {val}: {ename(exc)}")
        return
    if cmd == "regs":
        print(f"  registers {state['b'].to_registers()}")
        return
    if cmd == "coils":
        print(f"  coils {bitstr(state['b'].to_coils())}")
        return
    if cmd == "bytes":
        print(f"  bytes {state['b'].encode().hex()}")
        return
    if cmd == "decode":
        regs = ints(words[3])
        state["d"] = BinaryPayloadDecoder.fromRegisters(regs, byteorder=ORDER[words[1]], wordorder=ORDER[words[2]])
        return
    if cmd == "decodecoils":
        coils = [c == "1" for c in words[2]]
        state["d"] = BinaryPayloadDecoder.fromCoils(coils, byteorder=ORDER[words[1]])
        return
    if cmd == "get":
        d = state["d"]
        kind = words[1]
        try:
            if kind == "bits":
                v = bitstr(d.decode_bits())
            elif kind == "str":
                v = repr(d.decode_string(int(words[2])))
            elif kind == "skip":
                d.skip_bytes(int(words[2]))
                v = "skipped"
            elif kind.startswith("f"):
                v = repr(getattr(d, f"decode_{kind[1:]}bit_float")())
            elif kind.startswith("u"):
                v = getattr(d, f"decode_{kind[1:]}bit_uint")()
            else:
                v = getattr(d, f"decode_{kind[1:]}bit_int")()
            print(f"  {kind} {v}")
        except struct.error as exc:
            print(f"  ! get {kind}: {ename(exc)}")
        return
    if cmd == "reset":
        state["d"].reset()
        return
    raise ValueError(cmd)


# ------------------------------------------------------------ the jobs

def block(kind, spec, frozen):
    if kind == "seq":
        addr, vals = spec.split("=")
        values = []
        for part in vals.split(","):
            if "*" in part:
                n, v = part.split("*")
                values += [int(v, 0)] * int(n)
            else:
                values.append(int(part, 0))
        return ModbusSequentialDataBlock(int(addr, 0), values)
    if kind == "sparselist":
        return ModbusSparseDataBlock(ints(spec), mutable=not frozen)
    values = {}
    for part in spec.split(";"):
        addr, vals = part.split("=")
        values[int(addr, 0)] = ints(vals)
    return ModbusSparseDataBlock(values, mutable=not frozen)


def main():
    path = os.path.join(HERE, "data", "jobs.txt")
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    bus = None
    slave = None
    pl = {}
    for line in lines:
        if line == "" or line.startswith("#"):
            continue
        words = line.split(" ")
        cmd = words[0]
        if cmd == "job":
            print(f"== {' '.join(words[1:])}")
        elif cmd == "server":
            flags = words[2:]
            bus = Bus(words[1], "multi" in flags, "broadcast" in flags, "ignore" in flags)
            print(f"server {words[1]}{''.join(' ' + w for w in flags)}")
        elif cmd == "slave":
            sid = int(words[1], 0)
            slave = ModbusSlaveContext(zero_mode=len(words) > 2 and words[2] == "zero")
            try:
                bus.context[sid] = slave
                print(f"slave {sid}{' zero' if slave.zero_mode else ''}")
            except NoSuchSlaveException as exc:
                print(f"slave {sid}: {exc}")
        elif cmd == "block":
            slave.store[words[1]] = block(words[2], words[3], len(words) > 4 and words[4] == "frozen")
            print(f"block {words[1]} {words[2]} {slave.store[words[1]]}")
        elif cmd == "drop":
            try:
                del bus.context[int(words[1], 0)]
                print(f"dropped slave {words[1]}")
            except Exception as exc:  # pylint: disable=broad-except
                print(f"drop {words[1]}: {type(exc).__name__}: {exc}")
        elif cmd == "ident":
            how = words[1]
            pairs = [w.split("=", 1) for w in words[2:]]
            if how == "names":
                ModbusDeviceIdentification(info_name={k: text(v).decode("latin-1") for k, v in pairs})
            elif how == "info":
                ModbusDeviceIdentification(info={int(k, 0): text(v).decode("latin-1") for k, v in pairs})
            elif how == "set":
                for k, v in pairs:
                    MCB.Identity[int(k, 0)] = text(v).decode("latin-1")
            else:
                MCB.Identity.update({int(k, 0): text(v).decode("latin-1") for k, v in pairs})
            summary = MCB.Identity.summary()
            print("identity " + ", ".join(f"{k}={v!r}" for k, v in summary.items()))
        elif cmd == "counters":
            MCB.Counter.update({k: int(v) for k, v in (w.split("=") for w in words[1:])})
            print("counters " + " ".join(f"{k}={getattr(MCB.Counter, k)}" for k in COUNTERS)
                  + f" summary={MCB.Counter.summary():#x}")
        elif cmd == "event":
            kind = words[1]
            flags = {w: True for w in words[2:]}
            if kind == "recv":
                ev = RemoteReceiveEvent(**flags)
            elif kind == "send":
                ev = RemoteSendEvent(**flags)
            elif kind == "listen":
                ev = EnteredListenModeEvent()
            else:
                ev = CommunicationRestartEvent()
            MCB.addEvent(ev)
            print(f"event {kind} {ev.encode().hex()}: {len(MCB.Events)} logged, counter {MCB.Counter.Event}")
        elif cmd == "diagbits":
            MCB.setDiagnostic({int(k): v == "1" for k, v in (w.split("=") for w in words[1:])})
            print(f"diagnostic {bitstr(MCB.getDiagnosticRegister())} bit0={MCB.getDiagnostic(0)}"
                  f" bit1={MCB.getDiagnostic(1)} bit16={MCB.getDiagnostic(16)}")
        elif cmd == "control":
            print(f"control mode={MCB.Mode} listen_only={MCB.ListenOnly} delimiter={MCB.Delimiter!r}"
                  f" events={len(MCB.Events)} log={MCB.getEvents().hex()} diag={bitstr(MCB.getDiagnosticRegister())}")
        elif cmd == "slaveid":
            bus.context[int(words[1], 0)].reportSlaveIdData = text(words[2])
            print(f"slave {words[1]} reports {text(words[2])!r}")
        elif cmd == "req":
            op = words[1]
            args = []
            kw = {"slave": 1}
            chunk = 0
            for w in words[2:]:
                if w.startswith("slave="):
                    kw["slave"] = int(w[6:], 0)
                elif w.startswith("tid="):
                    kw["transaction"] = int(w[4:], 0)
                elif w.startswith("split="):
                    chunk = int(w[6:])
                else:
                    args.append(w)
            if "transaction" not in kw:
                bus.tid += 1
                kw["transaction"] = bus.tid
            try:
                request = make_request(op, args, kw)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"> {op}: ! {type(exc).__name__}: {exc}")
                continue
            try:
                packet = bus.client.buildPacket(request)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"> {label(request)}: ! {ename(exc)}")
                continue
            print(f"> {label(request)}")
            print(f"  tx {wire(bus.kind, packet)}")
            bus.to_server(packet, chunk)
        elif cmd == "raw":
            data = text(words[1]) if bus.kind == "ascii" else bytes.fromhex(words[1])
            print(f"> raw {len(data)} bytes")
            bus.to_server(data, int(words[2]) if len(words) > 2 else 0)
        elif cmd == "devraw":
            data = text(words[1]) if bus.kind == "ascii" else bytes.fromhex(words[1])
            print(f"< device {len(data)} bytes")
            bus.to_client(data)
        elif cmd == "peek":
            ctx = bus.context[int(words[1], 0)]
            store = ctx.store[words[2]]
            addr, count = int(words[3], 0), int(words[4], 0)
            if store.validate(addr, count):
                vals = [int(v) for v in store.getValues(addr, count)]
                print(f"peek {words[1]} {words[2]} {addr}+{count}: {vals}")
            else:
                print(f"peek {words[1]} {words[2]} {addr}+{count}: out of range")
        elif cmd == "reset":
            bus.context[int(words[1], 0)].reset()
            print(f"slave {words[1]} reset")
        elif cmd == "crc":
            data = bytes.fromhex(words[1])
            print(f"crc {words[1]} = {MessageRTU.compute_CRC(data):04x}")
        elif cmd == "lrc":
            data = bytes.fromhex(words[1])
            print(f"lrc {words[1]} = {MessageAscii.compute_LRC(data):02x}")
        elif cmd == "pl":
            print(f"pl {' '.join(words[1:])}")
            payload_step(pl, words[1:])
        else:
            raise ValueError(line)


main()
