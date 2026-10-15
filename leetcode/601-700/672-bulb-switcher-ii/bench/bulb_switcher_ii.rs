// Benchmark for #672: the cases worked out, as the Kara ★ arm.

fn flip_lights(n: i64, m: i64) -> i64 {
    if m == 0 {
        return 1;
    }
    if n == 1 {
        return 2;
    }
    if n == 2 {
        return if m == 1 { 3 } else { 4 };
    }
    if m == 1 {
        4
    } else if m == 2 {
        7
    } else {
        8
    }
}

fn main() {
    let count: i64 = 100000000;
    let mut sum: i64 = 0;
    for i in 0..count {
        sum = (sum * 31 + flip_lights(1 + i % 1000, i / 1000 % 1001)) % 1000000007;
    }
    println!("{} queries: checksum {}", count, sum);
}
