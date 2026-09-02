// Benchmark mirror of rangesum.kara — LeetCode #303, O(1) prefix-sum query.
// Same LCG, same query list, same sink.

const N: usize = 65536;
const NQUERIES: usize = 200_000;
const PASSES: usize = 1800;

fn main() {
    let mut state: i64 = 20303;

    let mut prefix = vec![0i64; N + 1];
    for i in 0..N {
        state = (state * 1103515245 + 12345) & 0x7fff_ffff;
        let v = (state / 65536) % 2001 - 1000;
        prefix[i + 1] = prefix[i] + v;
    }

    let mut qs = vec![0i64; NQUERIES * 2];
    for q in 0..NQUERIES {
        state = (state * 1103515245 + 12345) & 0x7fff_ffff;
        let x = (state / 65536) % N as i64;
        state = (state * 1103515245 + 12345) & 0x7fff_ffff;
        let y = (state / 65536) % N as i64;
        if x <= y {
            qs[q * 2] = x;
            qs[q * 2 + 1] = y;
        } else {
            qs[q * 2] = y;
            qs[q * 2 + 1] = x;
        }
    }

    let mut checksum: i64 = 0;
    for _ in 0..PASSES {
        for k in 0..NQUERIES {
            let v = prefix[qs[k * 2 + 1] as usize + 1] - prefix[qs[k * 2] as usize];
            checksum = (checksum + v) & 0x3FFF_FFFF;
        }
    }

    println!("checksum {checksum}");
}
