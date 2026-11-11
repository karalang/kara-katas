// LeetCode #2117: Abbreviating the Product of a Range -- the benchmark,
// the same algorithm as abbreviate.kara: the factors of 2 and 5 pulled
// out, the rest modulo 100000 and capped at 10^11, and an f64 of the
// leading digits.

fn abbreviate_product(left: i64, right: i64) -> String {
    let cap: i64 = 100000000000;
    let mut twos = 0i64;
    let mut fives = 0i64;
    let mut last = 1i64;
    let mut exact = 1i64;
    let mut lead = 1.0f64;
    for i in left..=right {
        let mut x = i;
        while x % 2 == 0 {
            x /= 2;
            twos += 1;
        }
        while x % 5 == 0 {
            x /= 5;
            fives += 1;
        }
        last = last * x % 100000;
        exact = if exact > cap / x { cap } else { exact * x };
        lead *= i as f64;
        while lead >= 1e12 {
            lead /= 10.0;
        }
    }
    let zeros = twos.min(fives);
    for _ in 0..twos - zeros {
        last = last * 2 % 100000;
        exact = if exact > cap / 2 { cap } else { exact * 2 };
    }
    for _ in 0..fives - zeros {
        last = last * 5 % 100000;
        exact = if exact > cap / 5 { cap } else { exact * 5 };
    }
    if exact < 10000000000 {
        return format!("{}e{}", exact, zeros);
    }
    while lead >= 1e5 {
        lead /= 10.0;
    }
    format!("{}...{:05}e{}", lead as i64, last, zeros)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2117i64;
    let mut long = 0i64;
    let mut check = 0i64;
    for _ in 0..40000 {
        let left = next_random(&mut seed) % 10000 + 1;
        let right = (left + next_random(&mut seed) % 3000).min(10000);
        let got = abbreviate_product(left, right);
        if got.contains("...") {
            long += 1;
        }
        for &b in got.as_bytes() {
            check = (check * 31 + b as i64) % 1000000007;
        }
    }
    println!("40000 solves: {} long answers, checksum {}", long, check);
}
