fn is_power_of_two(n: i64) -> bool {
    if n <= 0 {
        return false;
    }
    (n & (n - 1)) == 0
}

fn main() {
    let n: i64 = 130000000;
    let mask: i64 = 1023;
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = state & mask;
        if is_power_of_two(v) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
