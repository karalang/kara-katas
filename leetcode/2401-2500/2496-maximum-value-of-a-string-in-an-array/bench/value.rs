// LeetCode #2496: Maximum Value of a String in an Array -- Rust mirror of
// the benchmark (value.kara): the same lists, passes and checksum; the
// replaced string cloned out and put back, as the Kāra one is.

fn maximum_value(strs: &[String]) -> i64 {
    let mut best = 0;
    for s in strs {
        let mut number: i64 = 0;
        let mut digits = true;
        for c in s.chars() {
            if c.is_ascii_digit() {
                number = number * 10 + (c as i64 - '0' as i64);
            } else {
                digits = false;
            }
        }
        let worth = if digits { number } else { s.len() as i64 };
        best = best.max(worth);
    }
    best
}

fn main() {
    let passes: i64 = 90;
    let mut seed: i64 = 2496;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..2000 {
        let mut strs: Vec<String> = Vec::new();
        for _ in 0..100 {
            let length = next_random() % 9 + 1;
            let mut s = String::new();
            for _ in 0..length {
                let k = next_random();
                if k % 2 == 0 {
                    s.push((b'0' + (k / 2 % 10) as u8) as char);
                } else {
                    s.push((b'a' + (k / 2 % 26) as u8) as char);
                }
            }
            strs.push(s);
        }
        lists.push(strs);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for l in 0..2000 {
            let at = (check % 100) as usize;
            let was = lists[l][at].clone();
            lists[l][at] = format!("{}", check % 1000000000);
            check = (check * 31 + maximum_value(&lists[l]) + p) % 1000000007;
            lists[l][at] = was;
        }
    }
    println!("{passes} passes over 2000 lists of 100: checksum {check}");
}
