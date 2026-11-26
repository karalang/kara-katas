fn max_diff(num: i32) -> i32 {
    let s = num.to_string();
    let high = match s.chars().find(|&c| c != '9') {
        Some(c) => s.replace(c, "9"),
        None => s.clone(),
    };
    let first = s.chars().next().unwrap();
    let low = if first != '1' {
        s.replace(first, "1")
    } else {
        match s.chars().skip(1).find(|&c| c != '0' && c != '1') {
            Some(c) => s.replace(c, "0"),
            None => s.clone(),
        }
    };
    high.parse::<i32>().unwrap() - low.parse::<i32>().unwrap()
}

fn main() {
    let mut seed: i64 = 1432;
    let mut check: i64 = 0;
    for _ in 0..3000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let num = (1 + (high * 32768 + seed / 65536) % 100000000) as i32;
        check = (check * 131 + max_diff(num) as i64) % 1000000007;
    }
    println!("3 * 10^6 numbers: checksum {}", check);
}
