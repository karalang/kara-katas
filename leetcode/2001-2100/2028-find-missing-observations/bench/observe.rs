// LeetCode #2028: Find Missing Observations -- the ★ arm in Rust, the same
// algorithm and workload as observe.kara.

fn missing_rolls(rolls: &[i64], mean: i64, n: i64) -> Vec<i64> {
    let m = rolls.len() as i64;
    let need = mean * (m + n) - rolls.iter().sum::<i64>();
    if need < n || need > 6 * n {
        return Vec::new();
    }
    let (q, r) = (need / n, need % n);
    (0..n).map(|i| if i < r { q + 1 } else { q }).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2028;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    let mut means: Vec<i64> = Vec::new();
    let mut ns: Vec<i64> = Vec::new();
    for _ in 0..20 {
        lists.push((0..100000).map(|_| next_random(&mut seed) % 6 + 1).collect());
        means.push(next_random(&mut seed) % 4 + 2);
        ns.push(next_random(&mut seed) % 100000 + 1);
    }
    let (mut calls, mut rolls, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..50 {
        for a in 0..20 {
            let got = missing_rolls(&lists[a], means[a], ns[a]);
            calls += 1;
            rolls += got.len() as i64;
            if !got.is_empty() {
                check = (check * 31 + got[0] * 7 + got[got.len() - 1]) % 1000000007;
            } else {
                check = (check * 31 + 1) % 1000000007;
            }
        }
    }
    println!("{} calls: {} rolls, checksum {}", calls, rolls, check);
}
