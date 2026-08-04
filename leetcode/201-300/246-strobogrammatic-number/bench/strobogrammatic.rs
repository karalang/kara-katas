// Benchmark mirror for LeetCode #246 - Strobogrammatic Number.
//
// Same algorithm, same LCG, same sink as the Kara/C/Go/Python mirrors.
// Byte-indexed (`as_bytes()[i]`), matching every other compiled lane: the input
// is ASCII digits, so all five index bytes in place and do the same work.

const N: usize = 20000;
const LEN: usize = 32;
const PASSES: usize = 100;

const PAIR_A: [u8; 5] = [b'0', b'1', b'8', b'6', b'9'];
const PAIR_B: [u8; 5] = [b'0', b'1', b'8', b'9', b'6'];
const ALLD: [u8; 10] = [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9'];

#[inline]
fn rotate_byte(b: u8) -> u8 {
    match b {
        b'0' => b'0',
        b'1' => b'1',
        b'8' => b'8',
        b'6' => b'9',
        b'9' => b'6',
        _ => 0,
    }
}

fn is_strobogrammatic(num: &[u8]) -> bool {
    let mut lo = 0usize;
    let mut hi = num.len() - 1;
    loop {
        if lo > hi {
            return true;
        }
        let r = rotate_byte(num[lo]);
        if r == 0 || r != num[hi] {
            return false;
        }
        lo += 1;
        if hi == 0 {
            return true;
        }
        hi -= 1;
    }
}

fn lcg(state: i64) -> i64 {
    (state.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647
}

fn main() {
    let mut corpus: Vec<u8> = vec![0u8; N * LEN];
    let mut state: i64 = 1;
    for k in 0..N {
        let num = &mut corpus[k * LEN..(k + 1) * LEN];
        let mut lo = 0usize;
        let mut hi = LEN - 1;
        while lo < hi {
            state = lcg(state);
            let p = ((state / 65536) % 5) as usize;
            num[lo] = PAIR_A[p];
            num[hi] = PAIR_B[p];
            lo += 1;
            hi -= 1;
        }
        state = lcg(state);
        if (state / 65536) % 8 == 0 {
            state = lcg(state);
            let pos = ((state / 65536) % LEN as i64) as usize;
            state = lcg(state);
            num[pos] = ALLD[((state / 65536) % 10) as usize];
        }
    }

    let mut acc: i64 = 0;
    for _ in 0..PASSES {
        for i in 0..N {
            let v = is_strobogrammatic(&corpus[i * LEN..(i + 1) * LEN]) as i64;
            acc = (acc * 131 + v) % 1000000007;
        }
    }
    println!("{}", acc);
}
