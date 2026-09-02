// Benchmark mirror of meetpoint.kara — LeetCode #296, separable medians.
// Same two scans (row-major then column-major), same reused scratch, same sink.

const NCASES: usize = 400;
const DIM: usize = 128;
const PASSES: usize = 30;
const CELLS: usize = DIM * DIM;
const MOD: i64 = 1_000_000_007;

fn main() {
    let mut corpus = vec![0u8; NCASES * CELLS];
    let mut state: i64 = 24601;
    for slot in corpus.iter_mut() {
        state = (state * 1103515245 + 12345) & 0x7fff_ffff;
        *slot = if (state / 65536) % 100 < 10 { 1 } else { 0 };
    }

    let mut rows = vec![0i64; CELLS];
    let mut cols = vec![0i64; CELLS];
    let mut checksum: i64 = 0;

    for _ in 0..PASSES {
        for ci in 0..NCASES {
            let base = ci * CELLS;

            let mut k = 0usize;
            for r in 0..DIM {
                for c in 0..DIM {
                    if corpus[base + r * DIM + c] == 1 {
                        rows[k] = r as i64;
                        k += 1;
                    }
                }
            }

            let mut k2 = 0usize;
            for c in 0..DIM {
                for r in 0..DIM {
                    if corpus[base + r * DIM + c] == 1 {
                        cols[k2] = c as i64;
                        k2 += 1;
                    }
                }
            }

            let mut total: i64 = 0;
            if k > 0 {
                let mr = rows[k / 2];
                let mc = cols[k / 2];
                for i in 0..k {
                    total += (rows[i] - mr).abs();
                    total += (cols[i] - mc).abs();
                }
            }
            checksum = (checksum + total) % MOD;
        }
    }

    println!("checksum {checksum}");
}
