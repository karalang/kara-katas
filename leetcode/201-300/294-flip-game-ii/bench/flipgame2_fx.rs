// EQUAL-HASH side probe for LeetCode #294 — NOT part of bench.sh's output.
//
// `flipgame2.rs` uses Rust's default `HashMap`, whose hasher is SipHash-1-3
// seeded per process — DoS-resistant. Kāra's `Map` emits FxHash (rotate-xor-
// multiply) with a compile-time-constant seed, which is materially faster and
// not DoS-resistant. Comparing them head to head measures that safety
// difference as if it were a code-generation difference, which is exactly the
// mistake BENCHMARKS.md forbids on integer overflow.
//
// So this file is `flipgame2.rs` with Kāra's hash function transplanted in
// verbatim — the same rotate-left-5 / XOR / multiply per byte, the same seed —
// leaving the map implementation and everything else identical. The gap between
// this and `flipgame2.rs` is the price of hash-flooding resistance; the gap
// between this and the Kāra binary is the code generation.
//
// Build and run by hand:
//     rustc -O flipgame2_fx.rs -o target/flipgame2_fx && ./target/flipgame2_fx

use std::collections::HashMap;
use std::hash::{BuildHasherDefault, Hasher};

const LEN: usize = 22;
const BOARDS: usize = 300;

/// Kāra's emitted string hash: `h = h.rotate_left(5) ^ byte; h *= SEED`, per
/// byte, from a zero accumulator. See karac `src/codegen/synth.rs`.
#[derive(Default)]
struct FxHasher(u64);

impl Hasher for FxHasher {
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.0 = (self.0.rotate_left(5) ^ (b as u64)).wrapping_mul(0x517c_c1b7_2722_0a95);
        }
    }
    fn finish(&self) -> u64 {
        self.0
    }
}

type FxMap = HashMap<String, bool, BuildHasherDefault<FxHasher>>;

fn next_rand(s: i64) -> i64 { (s.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647 }

fn next_states(s: &str) -> Vec<String> {
    let cs: Vec<char> = s.chars().collect();
    let n = cs.len();
    let mut out = Vec::new();
    for i in 0..n.saturating_sub(1) {
        if cs[i] == '+' && cs[i + 1] == '+' {
            let mut t = String::new();
            for j in 0..n {
                t.push(if j == i || j == i + 1 { '-' } else { cs[j] });
            }
            out.push(t);
        }
    }
    out
}

fn can_win(s: &str, memo: &mut FxMap) -> bool {
    if let Some(&v) = memo.get(s) {
        return v;
    }
    for t in next_states(s) {
        if !can_win(&t, memo) {
            memo.insert(s.to_string(), true);
            return true;
        }
    }
    memo.insert(s.to_string(), false);
    false
}

fn main() {
    let mut seed: i64 = 20260821;
    let densities = [15i64, 50, 85];
    let mut wins: i64 = 0;
    let mut checksum: i64 = 0;

    for &d in densities.iter() {
        for _ in 0..BOARDS {
            let mut s = String::new();
            for _ in 0..LEN {
                seed = next_rand(seed);
                s.push(if ((seed / 65536) % 100) < d { '+' } else { '-' });
            }
            let mut memo = FxMap::default();
            if can_win(&s, &mut memo) {
                wins += 1;
            }
            checksum = (checksum * 31 + memo.len() as i64) % 1_000_000_007;
        }
    }
    println!("wins {} checksum {}", wins, checksum);
}
