fn count_combos(start: i64, k: i64, remaining: i64, d_pool: i64) -> i64 {
    if k == 0 {
        return if remaining == 0 { 1 } else { 0 };
    }
    let mut total = 0i64;
    let mut d = start;
    while d <= d_pool {
        if d > remaining { return total; }
        total += count_combos(d + 1, k - 1, remaining - d, d_pool);
        d += 1;
    }
    total
}

fn main() {
    let d_pool: i64 = 36;
    let kmax: i64 = 6;
    let nmax: i64 = 150;

    let mut sink: i64 = 0;
    for k in 1..=kmax {
        for n in 1..=nmax {
            sink += count_combos(1, k, n, d_pool);
        }
    }
    println!("{}", sink);
}
