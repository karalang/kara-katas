// LeetCode #91 — Rust bench peer for decode_ways.kara. Single-file rustc -O
// build. Same algorithm, same workload, same sink as the Kara mirror.
//
// Workload: 80-byte mutable digit buffer, hot loop of 1_000_000 calls to
// decode_ways. Each iter mutates one byte (cycling through digits 1..9
// at position k % 80) so the input varies per iter and the compiler
// can't hoist the call. Sum reduced mod 1e9+7; final reduced sum is
// the sink line.

fn decode_ways(bytes: &[u8]) -> i64 {
    let n = bytes.len();
    if n == 0 {
        return 0;
    }
    let zero: u8 = b'0';
    if bytes[0] == zero {
        return 0;
    }

    let mut prev2: i64 = 1;
    let mut prev1: i64 = 1;

    let mut i: usize = 1;
    while i < n {
        let d1: i32 = bytes[i] as i32 - zero as i32;
        let d0: i32 = bytes[i - 1] as i32 - zero as i32;
        let two: i32 = d0 * 10 + d1;

        let mut cur: i64 = 0;
        if d1 >= 1 && d1 <= 9 {
            cur += prev1;
        }
        if two >= 10 && two <= 26 {
            cur += prev2;
        }

        prev2 = prev1;
        prev1 = cur;
        i += 1;
    }

    prev1
}

fn main() {
    const L: i64 = 80;
    const N_ITERS: i64 = 10_000_000;
    const MODULUS: i64 = 1_000_000_007;
    let zero: u8 = b'0';

    let mut buf: Vec<u8> = Vec::with_capacity(L as usize);
    for j in 0..L {
        let d = ((j * 3) % 9) + 1;
        buf.push(zero + d as u8);
    }

    let mut sum: i64 = 0;
    for k in 0..N_ITERS {
        let pos = (k % L) as usize;
        let d = ((k * 11) % 9) + 1;
        buf[pos] = zero + d as u8;
        sum = (sum + decode_ways(&buf)) % MODULUS;
    }
    println!("{}", sum);
}
