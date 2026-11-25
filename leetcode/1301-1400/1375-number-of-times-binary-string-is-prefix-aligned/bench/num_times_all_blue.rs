// LeetCode #1375 bench -- Rust: the ★ arm: after step i the string is
// aligned exactly when the largest bit flipped so far is i.

fn num_times_all_blue(flips: &[i32]) -> i32 {
    let mut largest = 0;
    let mut aligned = 0;
    for (i, &f) in flips.iter().enumerate() {
        largest = largest.max(f);
        if largest == i as i32 + 1 {
            aligned += 1;
        }
    }
    aligned
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 orders of 5 * 10^4 bits, the constraints' most, 1 to n shuffled
    // within runs of 2 to 8, built once; then 1000 rounds, each trading
    // two neighbouring flips of one order, both drawn from the checksum
    // so far, and counting that order's aligned steps
    let n = 50000i64;
    let mut seed = 1375i64;
    let mut orders: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        let mut flips: Vec<i32> = (1..=n as i32).collect();
        let mut start = 0i64;
        while start < n {
            let end = (start + 2 + next_random(&mut seed) % 7).min(n);
            for i in (start + 1..end).rev() {
                let j = start + next_random(&mut seed) % (i - start + 1);
                flips.swap(i as usize, j as usize);
            }
            start = end;
        }
        orders.push(flips);
    }
    let mut check: i64 = 0;
    for r in 0..1000i64 {
        let flips = &mut orders[(check % 20) as usize];
        let k = ((check / 20) % (n - 1)) as usize;
        flips.swap(k, k + 1);
        let got = num_times_all_blue(flips) as i64;
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("1000 rounds over 20 orders of 50000 bits: checksum {check}");
}
