// Benchmark for #436: mirror of right_interval.kara (sorted starts and
// binary search) on 100 random sets of 20,000 intervals.

fn find_right_interval(intervals: &[(i64, i64)]) -> Vec<i64> {
    let n = intervals.len();
    let mut order: Vec<usize> = (0..n).collect();
    order.sort_by_key(|&i| intervals[i].0);
    let mut right: Vec<i64> = Vec::new();
    for i in 0..n {
        let end = intervals[i].1;
        let mut lo = 0;
        let mut hi = n;
        while lo < hi {
            let mid = (lo + hi) / 2;
            if intervals[order[mid]].0 < end {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        right.push(if lo < n { order[lo] as i64 } else { -1 });
    }
    right
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size: i64 = 20000;
    let rounds = 100;
    let mut seed: i64 = 436;
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        // Distinct starts, one in each step of 100 across the range,
        // each interval up to 32,767 long, then shuffled.
        let mut intervals: Vec<(i64, i64)> = Vec::new();
        for i in 0..size {
            let start = -1000000 + 100 * i + next_random(&mut seed) % 100;
            let end = (start + next_random(&mut seed)).min(1000000);
            intervals.push((start, end));
        }
        for i in 0..size {
            let j = i + next_random(&mut seed) % (size - i);
            intervals.swap(i as usize, j as usize);
        }
        let right = find_right_interval(&intervals);
        for j in right {
            if j >= 0 {
                found += 1;
            }
            checksum = (checksum * 31 + j + 2) % 1000000007;
        }
    }
    println!("{} rounds of {} intervals: {} right intervals, checksum {}", rounds, size, found, checksum);
}
