// LeetCode #1482: Minimum Number of Days to Make m Bouquets -- bench, the
// Rust twin of min_days.kara.

fn bouquets(bloom_day: &[i32], k: i32, day: i32) -> i64 {
    let mut made = 0;
    let mut run = 0;
    for &d in bloom_day {
        if d <= day {
            run += 1;
            if run == k {
                made += 1;
                run = 0;
            }
        } else {
            run = 0;
        }
    }
    made
}

fn min_days(bloom_day: &[i32], m: i32, k: i32) -> i32 {
    if (m as i64) * (k as i64) > bloom_day.len() as i64 {
        return -1;
    }
    let mut lo = *bloom_day.iter().min().unwrap();
    let mut hi = *bloom_day.iter().max().unwrap();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if bouquets(bloom_day, k, mid) >= m as i64 {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1482;
    let mut bloom: Vec<i32> = (0..100000)
        .map(|_| {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            (1 + (hi * 32768 + lo) % 1000000000) as i32
        })
        .collect();
    let mut check: i64 = 0;
    for pass in 0..150i64 {
        bloom[(check % 100000) as usize] = (1 + (check * 7) % 1000000000) as i32;
        let k = 1 + check % 10;
        let m = 1 + (check / 10) % (100000 / k + 100);
        check = (check * 31 + min_days(&bloom, m as i32, k as i32) as i64 + 1 + pass) % 1000000007;
    }
    println!("150 passes over 100000 flowers: checksum {}", check);
}
