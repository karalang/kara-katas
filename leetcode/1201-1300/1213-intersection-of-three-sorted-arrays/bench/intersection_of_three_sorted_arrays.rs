// LeetCode #1213 bench, in Rust: the ★ arm (three pointers, all three
// stepping on when the values agree and otherwise only those at the least
// value) on 1000 triples of arrays of 600 to 950 values drawn once, then
// 10 rounds over the triples, every answer's length and last value folded
// into a checksum.

fn arrays_intersection(arr1: &[i64], arr2: &[i64], arr3: &[i64]) -> Vec<i64> {
    let mut out = Vec::new();
    let (mut i, mut j, mut k) = (0, 0, 0);
    while i < arr1.len() && j < arr2.len() && k < arr3.len() {
        let (a, b, c) = (arr1[i], arr2[j], arr3[k]);
        if a == b && b == c {
            out.push(a);
            i += 1;
            j += 1;
            k += 1;
        } else {
            let least = a.min(b).min(c);
            if a == least {
                i += 1;
            }
            if b == least {
                j += 1;
            }
            if c == least {
                k += 1;
            }
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_sorted(seed: &mut i64, percent: i64) -> Vec<i64> {
    let mut out = Vec::new();
    for v in 1..=2000 {
        if next_random(seed) % 100 < percent {
            out.push(v);
        }
    }
    out
}

fn main() {
    let mut seed = 1213i64;
    let mut triples: Vec<(Vec<i64>, Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..1000 {
        let p = 33 + next_random(&mut seed) % 12;
        let a = random_sorted(&mut seed, p);
        let p = 33 + next_random(&mut seed) % 12;
        let b = random_sorted(&mut seed, p);
        let p = 33 + next_random(&mut seed) % 12;
        let c = random_sorted(&mut seed, p);
        triples.push((a, b, c));
    }
    let mut check: i64 = 0;
    for round in 0..10 {
        for (a, b, c) in &triples {
            let answer = arrays_intersection(a, b, c);
            let last = answer.last().copied().unwrap_or(0);
            check = (check * 131 + answer.len() as i64 + last + round) % 1000000007;
        }
    }
    println!("10 rounds over 1000 triples of 600 to 950 values: checksum {check}");
}
