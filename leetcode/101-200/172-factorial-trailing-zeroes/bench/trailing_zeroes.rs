fn trailing_zeroes(n: i64) -> i64 {
    let mut count = 0i64;
    let mut m = n / 5;
    while m > 0 {
        count += m;
        m /= 5;
    }
    count
}

fn main() {
    let limit: i64 = 35000000;
    let mut sink: i64 = 0;
    for i in 0..limit {
        sink += trailing_zeroes(i);
    }
    println!("{}", sink);
}
