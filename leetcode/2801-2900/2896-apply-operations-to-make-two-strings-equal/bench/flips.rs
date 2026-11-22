// LeetCode #2896: Apply Operations to Make Two Strings Equal -- the bench, as
// flips.kara: 5000 pairs of 500 characters, each answered 20 times by
// the pairing arm.

fn min_operations(s1: &str, s2: &str, x: i64) -> i64 {
    let a: Vec<char> = s1.chars().collect();
    let b: Vec<char> = s2.chars().collect();
    let places: Vec<i64> = (0..a.len())
        .filter(|&i| a[i] != b[i])
        .map(|i| i as i64)
        .collect();
    let m = places.len();
    if m % 2 == 1 {
        return -1;
    }
    let mut doubled = vec![0i64; m + 1];
    for i in 1..m + 1 {
        doubled[i] = doubled[i - 1] + x;
        if i >= 2 {
            doubled[i] = doubled[i].min(doubled[i - 2] + 2 * (places[i - 1] - places[i - 2]));
        }
    }
    doubled[m] / 2
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn bits(n: usize, seed: &mut i64) -> String {
    (0..n)
        .map(|_| if next_random(seed) % 2 == 0 { '0' } else { '1' })
        .collect()
}

fn main() {
    let (count, rounds, n) = (5000, 20i64, 500usize);
    let mut seed = 2896;
    let mut cases: Vec<(String, String, i64)> = Vec::new();
    for c in 0..count {
        let x = next_random(&mut seed) % 500 + 1;
        let s1 = bits(n, &mut seed);
        let s2 = if c % 2 == 0 {
            bits(n, &mut seed)
        } else {
            let mut chars: Vec<char> = s1.chars().collect();
            for _ in 0..next_random(&mut seed) % 20 {
                let at = (next_random(&mut seed) % n as i64) as usize;
                chars[at] = if chars[at] == '0' { '1' } else { '0' };
            }
            chars.iter().collect()
        };
        cases.push((s1, s2, x));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s1, s2, x) in cases.iter() {
            let cost = min_operations(s1, s2, *x);
            total += cost;
            check = (check * 31 + cost + 1 + r) % 1000000007;
        }
    }
    println!("{count} pairs of {n}, {rounds} rounds: costs total {total}, checksum {check}");
}
