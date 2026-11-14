// LeetCode #1566: Detect Pattern of Length M Repeated K or More Times --
// bench: the ★ arm (a run of agreements m apart) over 20 arrays of 100000
// values of 1 to 100, built once, half with a pattern planted near the
// end, each asked for m from 1 to 50 with k of 3.
// Rust mirror of pattern.kara.

fn contains_pattern(arr: &[i64], m: i64, k: i64) -> bool {
    let mut run = 0;
    let m = m as usize;
    for i in 0..arr.len().saturating_sub(m) {
        if arr[i] == arr[i + m] {
            run += 1;
            if run == m as i64 * (k - 1) {
                return true;
            }
        } else {
            run = 0;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 100000i64;
    let mut seed = 1566;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20i64 {
        let mut arr = Vec::new();
        for _ in 0..n {
            arr.push(next_random(&mut seed) % 100 + 1);
        }
        if a % 2 == 1 {
            let m = 1 + a % 50;
            let start = n - 3 * m - next_random(&mut seed) % 100;
            for i in m..3 * m {
                arr[(start + i) as usize] = arr[(start + i % m) as usize];
            }
        }
        arrays.push(arr);
    }
    let mut check = 0;
    let mut found = 0;
    for m in 1..=50i64 {
        for (a, arr) in arrays.iter().enumerate() {
            let yes = contains_pattern(arr, m, 3);
            if yes {
                found += 1;
            }
            check = mix(check, if yes { m * 100 + a as i64 } else { 0 });
        }
    }
    println!("m from 1 to 50 over 20 arrays of 100000 values: {} with a pattern, checksum {}", found, check);
}
