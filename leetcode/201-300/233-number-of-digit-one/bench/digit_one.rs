fn count_digit_one(n: i64) -> i64 {
    if n < 0 { return 0; }
    let mut count = 0i64;
    let mut pos = 1i64;
    while pos <= n {
        let high = n / (pos * 10);
        let cur = (n / pos) % 10;
        let low = n % pos;
        if cur == 0 {
            count += high * pos;
        } else if cur == 1 {
            count += high * pos + low + 1;
        } else {
            count += (high + 1) * pos;
        }
        pos *= 10;
    }
    count
}

fn main() {
    let limit: i64 = 6000000;
    let mut sink: i64 = 0;
    for i in 0..limit {
        sink += count_digit_one(i);
    }
    println!("{}", sink);
}
