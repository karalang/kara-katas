// LeetCode #1534: Count Good Triplets -- bench: the ★ arm over 100 random
// arrays of 100 values up to 1000, each with its own a, b and c up to
// 1000, built once and answered 10 times. Rust mirror of triplets.kara.

fn count_good_triplets(arr: &[i64], a: i64, b: i64, c: i64) -> i64 {
    let n = arr.len();
    let mut count = 0;
    for i in 0..n {
        for j in i + 1..n {
            if (arr[i] - arr[j]).abs() > a {
                continue;
            }
            for k in j + 1..n {
                if (arr[j] - arr[k]).abs() <= b && (arr[i] - arr[k]).abs() <= c {
                    count += 1;
                }
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1534i64;
    let mut cases = Vec::new();
    for _ in 0..100 {
        let arr: Vec<i64> = (0..100).map(|_| next_random(&mut seed) % 1001).collect();
        let a = next_random(&mut seed) % 1001;
        let b = next_random(&mut seed) % 1001;
        let c = next_random(&mut seed) % 1001;
        cases.push((arr, a, b, c));
    }
    let mut check = 0;
    for _ in 0..10 {
        for (arr, a, b, c) in &cases {
            check = mix(check, count_good_triplets(arr, *a, *b, *c));
        }
    }
    println!("10 passes over 100 arrays of 100 values: checksum {}", check);
}
