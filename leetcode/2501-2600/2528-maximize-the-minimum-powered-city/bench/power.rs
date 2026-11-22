// LeetCode #2528: Maximize the Minimum Powered City -- Rust mirror of the
// benchmark (power.kara): the same cities, passes, order and checksum.

fn reachable(power: &[i64], r: i64, k: i64, target: i64) -> bool {
    let n = power.len() as i64;
    let mut ends = vec![0i64; n as usize + 1];
    let mut running = 0;
    let mut used = 0;
    for i in 0..n {
        running += ends[i as usize];
        let have = power[i as usize] + running;
        if have < target {
            let need = target - have;
            used += need;
            if used > k {
                return false;
            }
            running += need;
            ends[(i + 2 * r + 1).min(n) as usize] -= need;
        }
    }
    true
}

fn max_power(stations: &[i64], r: i64, k: i64) -> i64 {
    let n = stations.len() as i64;
    let mut prefix = vec![0i64; n as usize + 1];
    for i in 0..n as usize {
        prefix[i + 1] = prefix[i] + stations[i];
    }
    let power: Vec<i64> = (0..n).map(|i| prefix[(i + r + 1).min(n) as usize] - prefix[(i - r).max(0) as usize]).collect();
    let mut lo = *power.iter().min().unwrap();
    let mut hi = lo + k;
    while lo < hi {
        let mid = lo + (hi - lo + 1) / 2;
        if reachable(&power, r, k, mid) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2528;
    let stations: Vec<i64> = (0..100000).map(|_| next_random(&mut seed) % 100001).collect();
    let passes = 20;
    let mut check: i64 = 0;
    for p in 0..passes {
        let r = check % 100;
        let k = 1000000000 - check % 1000;
        check = (check * 31 + max_power(&stations, r, k) + p) % 1000000007;
    }
    println!("{passes} passes over 100000 cities: checksum {check}");
}
