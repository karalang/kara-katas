// LeetCode #2234: Maximum Total Beauty of the Gardens -- the benchmark's
// Rust mirror of beauty.kara: every split of complete gardens tried, the
// level of the rest by a binary search on the level.

fn maximum_beauty(flowers: &[i64], new_flowers: i64, target: i64, full: i64, partial: i64) -> i64 {
    let mut sorted: Vec<i64> = flowers.iter().map(|&f| f.min(target)).collect();
    sorted.sort();
    let n = sorted.len();
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + sorted[i];
    }
    let mut best = 0i64;
    let mut cost = 0i64;
    let mut c = n as i64;
    while c >= 0 {
        let cu = c as usize;
        if cu < n {
            cost += target - sorted[cu];
        }
        if cost > new_flowers {
            break;
        }
        let complete = (n as i64 - c) * full;
        if c == 0 {
            best = best.max(complete);
        } else if sorted[cu - 1] < target {
            let left = new_flowers - cost;
            let mut low = sorted[0];
            let mut high = target - 1;
            while low < high {
                let m = (low + high + 1) / 2;
                let mut a = 0usize;
                let mut b = cu;
                while a < b {
                    let mid = (a + b) / 2;
                    if sorted[mid] < m {
                        a = mid + 1;
                    } else {
                        b = mid;
                    }
                }
                if m * a as i64 - prefix[a] <= left {
                    low = m;
                } else {
                    high = m - 1;
                }
            }
            best = best.max(complete + low * partial);
        }
        c -= 1;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2234i64;
    let mut flowers: Vec<i64> = Vec::new();
    for _ in 0..20000 {
        flowers.push(wide_random(&mut seed) % 100000 + 1);
    }
    let mut check = 0i64;
    for _ in 0..20 {
        // punch: one garden drawn again before each pass, and the new
        // flowers drawn anew
        let at = (next_random(&mut seed) % 20000) as usize;
        flowers[at] = wide_random(&mut seed) % 100000 + 1;
        let new_flowers = wide_random(&mut seed) % 1200000000 + 1;
        check = (check * 31 + maximum_beauty(&flowers, new_flowers, 100000, 100000, 100000)) % 1000000007;
    }
    println!("20 passes over 20000 gardens: checksum {}", check);
}
