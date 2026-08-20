// Benchmark twin for LeetCode #292 — same algorithm as nimgame.kara.

const N: usize = 20_000_000;

fn main() {
    let mut win = vec![false; N + 1];
    win[0] = false;
    for i in 1..=N {
        let mut w = false;
        for take in 1..=3usize {
            if i >= take && !win[i - take] {
                w = true;
            }
        }
        win[i] = w;
    }
    let mut losing: i64 = 0;
    let mut checksum: i64 = 0;
    for i in 0..=N {
        if !win[i] {
            losing += 1;
            checksum = (checksum * 31 + i as i64) % 1_000_000_007;
        }
    }
    println!("losing {} checksum {}", losing, checksum);
}
