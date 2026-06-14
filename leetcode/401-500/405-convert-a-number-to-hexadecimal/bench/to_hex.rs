// LeetCode #405 bench harness — Rust peer (rustc -O, single-thread).
//
// Bitwise mask-and-shift hex render — same canonical algorithm as the Kāra
// mirror. Sequential string-building bench: concatenate TOTAL hex renderings
// into one buffer, then byte-checksum it. Persisting the output defeats
// allocation-elision (a per-render byte-sum would let rustc fold the work to
// arithmetic). Sink = byte-sum of the concatenated output.

const TOTAL: i64 = 4_000_000;
const HEX: &[u8; 16] = b"0123456789abcdef";

fn to_hex(num: i64) -> String {
    if num == 0 {
        return "0".to_string();
    }
    let mut n = num & 0xffff_ffff;
    let mut buf: Vec<i64> = Vec::new();
    while n > 0 {
        buf.push(n & 0xf);
        n >>= 4;
    }
    let mut out = String::new();
    for k in (0..buf.len()).rev() {
        out.push(HEX[buf[k] as usize] as char);
    }
    out
}

fn main() {
    let mut out = String::new();
    for k in 0..TOTAL {
        let v = (k * 2654435761) & 0xffff_ffff;
        out.push_str(&to_hex(v));
    }
    let mut sum: i64 = 0;
    for &b in out.as_bytes() {
        sum += b as i64;
    }
    println!("{}", sum);
}
