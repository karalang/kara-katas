fn col_checksum(n: i64) -> i64 {
    let mut x = n;
    let mut acc = 0i64;
    while x > 0 {
        x -= 1; // bijective base-26: shift to 0-based digit
        acc += 65 + (x % 26); // 'A' = 65
        x /= 26;
    }
    acc
}

fn main() {
    let limit: i64 = 50000000;
    let mut sink: i64 = 0;
    let mut n: i64 = 1;
    while n <= limit {
        sink += col_checksum(n);
        n += 1;
    }
    println!("{}", sink);
}
