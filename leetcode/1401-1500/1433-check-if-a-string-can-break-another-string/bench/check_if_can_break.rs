fn check_if_can_break(s1: &str, s2: &str) -> bool {
    let mut a = s1.as_bytes().to_vec();
    let mut b = s2.as_bytes().to_vec();
    a.sort();
    b.sort();
    a.iter().zip(b.iter()).all(|(x, y)| x >= y) || a.iter().zip(b.iter()).all(|(x, y)| x <= y)
}

fn main() {
    let mut seed: i64 = 1433;
    let mut pool = String::new();
    let mut up = String::new();
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let c = b'a' + (seed / 65536 % 25) as u8;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push(c as char);
        up.push((c + (seed / 65536 % 2) as u8) as char);
    }
    let mut breaks: i64 = 0;
    for _ in 0..400 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let one = ((high * 32768 + seed / 65536) % 900001) as usize;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let got = if seed / 65536 % 2 == 0 {
            check_if_can_break(&pool[one..one + 100000], &up[one..one + 100000])
        } else {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let two = ((high * 32768 + seed / 65536) % 900001) as usize;
            check_if_can_break(&pool[one..one + 100000], &pool[two..two + 100000])
        };
        if got {
            breaks += 1;
        }
    }
    println!("400 pairs of 10^5 letters: {} can break", breaks);
}
