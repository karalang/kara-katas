fn reverse_bits(n: i64) -> i64 {
    let mut result: i64 = 0;
    let mut x = n;
    let mut i: i64 = 0;
    while i < 32 {
        result = (result << 1) | (x & 1);
        x >>= 1;
        i += 1;
    }
    result
}

fn main() {
    let count: i64 = 8000000;
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _ in 0..count {
        state = (state * 1103515245 + 12345) & 2147483647;
        sink += reverse_bits(state);
    }
    println!("{}", sink);
}
