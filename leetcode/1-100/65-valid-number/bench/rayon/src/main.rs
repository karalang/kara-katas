// LeetCode #65 — rayon-parallel Rust mirror (par lane, valid).
// Same 8-state DFA is_number as ../valid.rs; the K=10M reduction runs across a
// rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches
// the kara/rust/c/go mirrors.

fn categorize(b: u8) -> i32 {
    if b.is_ascii_digit() {
        return 0;
    }
    if b == b'+' || b == b'-' {
        return 1;
    }
    if b == b'.' {
        return 2;
    }
    if b == b'e' || b == b'E' {
        return 3;
    }
    4
}

fn is_number(s: &str) -> bool {
    let bytes = s.as_bytes();
    let n = bytes.len();

    let mut state: i32 = 0;
    let mut i: usize = 0;
    while i < n {
        let cat: i32 = categorize(bytes[i]);

        if state == 0 {
            match cat {
                0 => state = 2,
                1 => state = 1,
                2 => state = 3,
                _ => return false,
            }
        } else if state == 1 {
            match cat {
                0 => state = 2,
                2 => state = 3,
                _ => return false,
            }
        } else if state == 2 {
            match cat {
                0 => state = 2,
                2 => state = 4,
                3 => state = 6,
                _ => return false,
            }
        } else if state == 3 {
            match cat {
                0 => state = 5,
                _ => return false,
            }
        } else if state == 4 {
            match cat {
                0 => state = 5,
                3 => state = 6,
                _ => return false,
            }
        } else if state == 5 {
            match cat {
                0 => state = 5,
                3 => state = 6,
                _ => return false,
            }
        } else if state == 6 {
            match cat {
                0 => state = 8,
                1 => state = 7,
                _ => return false,
            }
        } else if state == 7 {
            match cat {
                0 => state = 8,
                _ => return false,
            }
        } else if state == 8 {
            match cat {
                0 => state = 8,
                _ => return false,
            }
        } else {
            return false;
        }

        i += 1;
    }

    state == 2 || state == 4 || state == 5 || state == 8
}

fn main() {
    use rayon::prelude::*;
    let n: i64 = 8;
    let k_iters: i64 = 10_000_000;

    let inputs: Vec<&str> = vec![
        "0",
        "-.9",
        "53.5e93",
        "+6e-1",
        "abc",
        "1e",
        "99e2.5",
        "-123.456e789",
    ];

    let sum: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % n) as usize;
            if is_number(inputs[idx]) {
                1
            } else {
                0
            }
        })
        .sum();
    println!("{}", sum);
}
