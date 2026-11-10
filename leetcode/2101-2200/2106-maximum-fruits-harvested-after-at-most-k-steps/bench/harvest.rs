// LeetCode #2106: Maximum Fruits Harvested After at Most K Steps --
// bench, Rust mirror of harvest.kara.

fn steps(l: i64, r: i64, start: i64) -> i64 {
    if l >= start {
        r - start
    } else if r <= start {
        start - l
    } else {
        (2 * (start - l) + (r - start)).min((start - l) + 2 * (r - start))
    }
}

fn max_total_fruits(fruits: &[Vec<i64>], start: i64, k: i64) -> i64 {
    let mut left = 0usize;
    let mut sum = 0i64;
    let mut best = 0i64;
    for right in 0..fruits.len() {
        sum += fruits[right][1];
        while left <= right && steps(fruits[left][0], fruits[right][0], start) > k {
            sum -= fruits[left][1];
            left += 1;
        }
        best = best.max(sum);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2106;
    let mut fields: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..20 {
        let mut fruits: Vec<Vec<i64>> = Vec::new();
        for p in 0..200000 {
            if next_random(&mut seed) % 2 == 0 {
                fruits.push(vec![p, wide_random(&mut seed) % 10000 + 1]);
            }
        }
        fields.push(fruits);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for fruits in &fields {
        for _ in 0..10 {
            let start = wide_random(&mut seed) % 200001;
            let k = wide_random(&mut seed) % 200001;
            let got = max_total_fruits(fruits, start, k);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("200 walks: {} fruits, checksum {}", total, check);
}
