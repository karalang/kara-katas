// Benchmark mirror of parenrepair.kara — LeetCode #301, unique-by-construction
// repair. Same recursion, same depth-indexed scratch buffer, same sink.
//
// The scratch buffer is one flat Vec<u8> indexed by `depth * SLOT`, exactly as
// the Kara mirror spells it — not a `[[u8; 32]; 32]` split into disjoint
// borrows. Two reasons: it keeps the five mirrors byte-for-byte the same
// algorithm, and it keeps Rust's bounds checks on the same accesses Kara
// checks, which is what makes the equal-safety column honest.

const NCASES: usize = 2000;
const SLEN: usize = 24;
const PASSES: usize = 64;
const SLOT: usize = 32;
const MAXDEPTH: usize = 32;
const MOD: i64 = 1_000_000_007;

#[allow(clippy::too_many_arguments)]
fn repair(
    scratch: &mut [u8],
    depth: usize,
    len: usize,
    last_i: usize,
    last_j: usize,
    open: u8,
    close: u8,
    results: &mut i64,
    checksum: &mut i64,
) {
    let base = depth * SLOT;
    let child = base + SLOT;

    let mut count: i64 = 0;
    let mut i = last_i;
    while i < len {
        let c = scratch[base + i];
        if c == open {
            count += 1;
        } else if c == close {
            count -= 1;
        }
        if count < 0 {
            let mut j = last_j;
            while j <= i {
                if scratch[base + j] == close
                    && (j == last_j || scratch[base + j - 1] != close)
                {
                    let mut w = 0;
                    for k in 0..len {
                        if k != j {
                            scratch[child + w] = scratch[base + k];
                            w += 1;
                        }
                    }
                    repair(scratch, depth + 1, len - 1, i, j, open, close, results, checksum);
                }
                j += 1;
            }
            return;
        }
        i += 1;
    }

    for r in 0..len {
        scratch[child + r] = scratch[base + len - 1 - r];
    }

    if open == b'(' {
        repair(scratch, depth + 1, len, 0, 0, b')', b'(', results, checksum);
    } else {
        let mut h: i64 = 0;
        for t in 0..len {
            h = (h * 31 + scratch[child + t] as i64) % MOD;
        }
        *results += 1;
        *checksum = (*checksum + h) % MOD;
    }
}

fn main() {
    let mut corpus = vec![0u8; NCASES * SLEN];
    let mut state: i64 = 12345;
    for slot in corpus.iter_mut() {
        state = (state * 1103515245 + 12345) & 0x7fff_ffff;
        let r = (state / 65536) % 3;
        *slot = if r == 0 { b'(' } else if r == 1 { b')' } else { b'a' };
    }

    let mut scratch = vec![0u8; MAXDEPTH * SLOT];
    let mut results: i64 = 0;
    let mut checksum: i64 = 0;

    for _ in 0..PASSES {
        for ci in 0..NCASES {
            let src = ci * SLEN;
            scratch[..SLEN].copy_from_slice(&corpus[src..src + SLEN]);
            repair(&mut scratch, 0, SLEN, 0, 0, b'(', b')', &mut results, &mut checksum);
        }
    }

    println!("results {results}");
    println!("checksum {checksum}");
}
