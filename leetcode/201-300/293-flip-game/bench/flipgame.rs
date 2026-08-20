// Benchmark twin for LeetCode #293 — same algorithm as flipgame.kara.

const LEN: usize = 64;
const BOARDS: usize = 40000;

fn next_rand(s: i64) -> i64 { (s.wrapping_mul(1103515245).wrapping_add(12345)) & 2147483647 }

fn main() {
    let mut seed: i64 = 20260820;
    let densities = [15i64, 50, 85];
    let mut total_states: i64 = 0;
    let mut checksum: i64 = 0;
    let mut cs = [b'-'; LEN];

    for &d in densities.iter() {
        for _ in 0..BOARDS {
            for i in 0..LEN {
                seed = next_rand(seed);
                cs[i] = if ((seed / 65536) % 100) < d { b'+' } else { b'-' };
            }
            let mut out: Vec<String> = Vec::new();
            for i in 0..LEN - 1 {
                if cs[i] == b'+' && cs[i + 1] == b'+' {
                    let mut t = String::with_capacity(LEN);
                    for j in 0..LEN {
                        t.push(if j == i || j == i + 1 { '-' } else { cs[j] as char });
                    }
                    out.push(t);
                }
            }
            total_states += out.len() as i64;
            for s in &out {
                checksum = (checksum * 31 + s.len() as i64) % 1_000_000_007;
            }
        }
    }
    println!("states {} checksum {}", total_states, checksum);
}
