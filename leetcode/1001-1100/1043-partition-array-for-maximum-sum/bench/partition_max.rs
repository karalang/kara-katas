// LeetCode #1043: Partition Array for Maximum Sum -- bench, Rust mirror
// of partition_max.kara (the bottom-up table).

fn max_sum_after_partitioning(arr: &[i64], k: i64) -> i64 {
    let n = arr.len();
    let mut best = vec![0i64; n + 1];
    for i in 1..=n {
        let mut largest = 0;
        let mut j = 1;
        while j <= k as usize && j <= i {
            largest = largest.max(arr[i - j]);
            best[i] = best[i].max(best[i - j] + largest * j as i64);
            j += 1;
        }
    }
    best[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 400;
    let n = 500;
    let rounds = 40;
    let mut seed = 1043;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<i64> = Vec::new();
    for _ in 0..count {
        let mut arr = Vec::new();
        for _ in 0..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            arr.push((hi * 32768 + lo) % 1000000001);
        }
        arrays.push(arr);
        ks.push(next_random(&mut seed) % 50 + 1);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for a in 0..count {
            let answer = max_sum_after_partitioning(&arrays[a], ks[a]);
            total += answer;
            check = (check * 131 + answer % 1000000007) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: total {total}, checksum {check}");
}
