// Benchmark: LeetCode #941 Valid Mountain Array -- the ★ arm, a walk up
// and a walk down, on 100 arrays of 10000 values, LeetCode's longest, in
// 200 rounds. Mirrors valid_mountain_array.kara, .c, .py and go-seq/.

fn valid_mountain_array(arr: &[i64]) -> bool {
    let n = arr.len();
    let mut i = 0;
    while i + 1 < n && arr[i] < arr[i + 1] {
        i += 1;
    }
    if i == 0 || i == n - 1 {
        return false;
    }
    while i + 1 < n && arr[i] > arr[i + 1] {
        i += 1;
    }
    i == n - 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 200;
    let count = 100;
    let mut seed = 941;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..count {
        let top = 1 + next_random(&mut seed) % 9998;
        let least = if top < 10000 - top { 0 } else { 2 * top - 9999 };
        let mut arr: Vec<i64> = (0..10000)
            .map(|i| (if i <= top { i } else { 2 * top - i }) - least)
            .collect();
        if a % 2 == 1 {
            let hi = next_random(&mut seed);
            let j = ((hi * 32768 + next_random(&mut seed)) % 10000) as usize;
            arr[j] = next_random(&mut seed) % 10001;
        }
        arrays.push(arr);
    }
    let mut mountains: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let c = (r + i) % count;
            if valid_mountain_array(&arrays[c]) {
                mountains += 1;
                check = (check * 1000003 + c as i64 + 1) % 1000000007;
            }
        }
    }
    println!(
        "{} rounds over {} arrays of 10000 values: {} mountains, checksum {}",
        rounds, count, mountains, check
    );
}
