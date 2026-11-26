// LeetCode #1405 bench, Rust: the same greedy, a sort of the three
// letters before each one placed, workload and checksum as
// longest_diverse_string.kara.

fn longest_diverse_string(a: i32, b: i32, c: i32) -> String {
    let mut left = [(a, 'a'), (b, 'b'), (c, 'c')];
    let mut out = String::new();
    loop {
        left.sort_by(|x, y| y.0.cmp(&x.0));
        let mut placed = false;
        for i in 0..3 {
            let (n, ch) = left[i];
            if n == 0 {
                break;
            }
            if out.ends_with(&format!("{}{}", ch, ch)) {
                continue;
            }
            out.push(ch);
            left[i] = (n - 1, ch);
            placed = true;
            break;
        }
        if !placed {
            return out;
        }
    }
}

fn main() {
    let mut seed: i64 = 1405;
    let mut check: i64 = 0;
    for _ in 0..20000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let a = (seed / 65536 % 101) as i32;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let b = (seed / 65536 % 101) as i32;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let c = (1 + seed / 65536 % 100) as i32;
        let s = longest_diverse_string(a, b, c);
        for ch in s.chars() {
            check = (check * 131 + ch as i64) % 1000000007;
        }
    }
    println!("20000 strings of up to 300 letters: checksum {}", check);
}
