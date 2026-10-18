// LeetCode 753 — Cracking the Safe, bench: the ★ arm (an Euler circuit
// by Hierholzer's method), mirrored from crack_safe.kara.

fn crack_safe(n: i64, k: i64) -> String {
    let mut nodes: i64 = 1;
    for _ in 0..n - 1 {
        nodes *= k;
    }
    let mut used: Vec<i64> = vec![0; nodes as usize];
    let mut stack: Vec<(i64, i64)> = Vec::new();
    stack.push((0, -1));
    let mut digits: Vec<i64> = Vec::new();
    while !stack.is_empty() {
        let (node, digit) = stack[stack.len() - 1];
        if used[node as usize] < k {
            let d = used[node as usize];
            used[node as usize] += 1;
            stack.push(((node * k + d) % nodes, d));
        } else {
            stack.pop();
            if digit >= 0 {
                digits.push(digit);
            }
        }
    }
    let mut out = String::new();
    for _ in 0..n - 1 {
        out.push('0');
    }
    for &d in digits.iter().rev() {
        out.push((b'0' + d as u8) as char);
    }
    out
}

fn main() {
    let rounds = 2000;
    let mut safes: i64 = 0;
    let mut digits: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for n in 1..5i64 {
            for k in 1..11i64 {
                let mut total: i64 = 1;
                for _ in 0..n {
                    total *= k;
                }
                if total <= 4096 {
                    safes += 1;
                    let text = crack_safe(n, k);
                    digits += text.len() as i64;
                    for b in text.bytes() {
                        check = (check * 31 + b as i64) % 1000000007;
                    }
                }
            }
        }
    }
    println!("{} safes: {} digits in all, checksum {}", safes, digits, check);
}
