// LeetCode #1521: Find a Value of a Mysterious Function Closest to Target
// -- bench: the ★ arm over 2000 random arrays of 1 to 4000 numbers, built
// once and answered 3 times.

fn closest_to_target(arr: &[i64], target: i64) -> i64 {
    let mut best = (arr[0] - target).abs();
    let mut ends: Vec<i64> = Vec::new();
    for &x in arr {
        let mut next: Vec<i64> = vec![x];
        for &v in &ends {
            let w = v & x;
            if w != next[next.len() - 1] {
                next.push(w);
            }
        }
        for &v in &next {
            best = best.min((v - target).abs());
        }
        ends = next;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let count = 2000;
    let mut seed = 1521i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut targets: Vec<i64> = Vec::new();
    for _ in 0..count {
        let n = next_random(&mut seed) % 4000 + 1;
        let base = next_random(&mut seed) % 1000000 + 1;
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..n {
            let x = if next_random(&mut seed) % 2 == 0 {
                base & (next_random(&mut seed) * 32768 + next_random(&mut seed))
            } else {
                next_random(&mut seed) * 32 % 1000000
            };
            arr.push(x.max(1));
        }
        targets.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000001);
        arrays.push(arr);
    }
    let mut check = 0;
    let mut total = 0i64;
    for _ in 0..3 {
        for i in 0..count {
            let answer = closest_to_target(&arrays[i], targets[i]);
            total += answer;
            check = mix(check, answer);
        }
    }
    println!("3 passes over 2000 arrays of up to 4000 numbers: distances sum to {}, checksum {}", total, check);
}
