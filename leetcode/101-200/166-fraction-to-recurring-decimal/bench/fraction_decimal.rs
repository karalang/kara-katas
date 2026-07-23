use std::collections::HashMap;

fn frac_checksum(num: i64, den: i64) -> i64 {
    let mut rem = num % den;
    let mut checksum = 0i64;
    if rem == 0 {
        return 0;
    }
    let mut pos: HashMap<i64, i64> = HashMap::new();
    let mut count = 0i64;
    while rem != 0 {
        if pos.contains_key(&rem) {
            rem = 0; // cycle closed — stop
        } else {
            pos.insert(rem, count);
            rem *= 10;
            let digit = rem / den;
            checksum += digit;
            rem %= den;
            count += 1;
        }
    }
    checksum
}

fn main() {
    let passes: i64 = 500000;
    let mut state: i64 = 12345;
    let mut sink: i64 = 0;
    for _p in 0..passes {
        state = (state * 1103515245 + 12345) & 2147483647;
        let num = state % 1000000;
        state = (state * 1103515245 + 12345) & 2147483647;
        let den = 2 + (state % 1023);
        sink += frac_checksum(num, den);
    }
    println!("{}", sink);
}
