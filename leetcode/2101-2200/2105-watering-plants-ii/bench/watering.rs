// LeetCode #2105: Watering Plants II -- bench, Rust mirror of
// watering.kara.

fn minimum_refill(plants: &[i64], capacity_a: i64, capacity_b: i64) -> i64 {
    let mut i = 0usize;
    let mut j = plants.len() - 1;
    let (mut a, mut b) = (capacity_a, capacity_b);
    let mut refills = 0i64;
    while i < j {
        if a < plants[i] {
            refills += 1;
            a = capacity_a;
        }
        a -= plants[i];
        if b < plants[j] {
            refills += 1;
            b = capacity_b;
        }
        b -= plants[j];
        i += 1;
        j -= 1;
    }
    if i == j && a.max(b) < plants[i] {
        refills += 1;
    }
    refills
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
    let mut seed = 2105;
    let mut rows: Vec<(Vec<i64>, i64, i64)> = Vec::new();
    for _ in 0..200 {
        let plants: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 1000000 + 1).collect();
        let most = *plants.iter().max().unwrap();
        let a = most + wide_random(&mut seed) % (2000000 - most + 1);
        let b = most + wide_random(&mut seed) % (2000000 - most + 1);
        rows.push((plants, a, b));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..10 {
        for (plants, a, b) in &rows {
            let got = minimum_refill(plants, *a, *b);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    println!("2000 rows: {} refills, checksum {}", total, check);
}
