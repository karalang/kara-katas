// LeetCode 796 — Rotate String: the bench, in Rust. Mirrors
// rotate_string.kara: goal is a rotation when it is as long as s and in
// s written twice, made fresh for each call.

fn rotate_string(s: &str, goal: &str) -> bool {
    s.len() == goal.len() && format!("{s}{s}").contains(goal)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 796;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..4096 {
        let letters = 1 + next_random(&mut seed) % 4;
        let mut s = String::new();
        for _ in 0..100 {
            s.push((97 + next_random(&mut seed) % letters) as u8 as char);
        }
        let kind = next_random(&mut seed) % 3;
        let mut goal = String::new();
        if kind == 2 {
            for _ in 0..100 {
                goal.push((97 + next_random(&mut seed) % letters) as u8 as char);
            }
        } else {
            let k = next_random(&mut seed) % 100;
            let chars: Vec<char> = s.chars().collect();
            let change = if kind == 1 { next_random(&mut seed) % 100 } else { -1 };
            for j in 0..100 {
                let c = chars[((j + k) % 100) as usize];
                goal.push(if j == change { (97 + (c as i64 - 97 + 1) % letters) as u8 as char } else { c });
            }
        }
        pairs.push((s, goal));
    }
    let rounds = 1500000;
    let mut rotations = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let (s, goal) = &pairs[r % 4096];
        if rotate_string(s, goal) {
            rotations += 1;
            check = (check * 131 + (r % 4096) as i64) % 1000000007;
        }
    }
    println!("{rounds} pairs: {rotations} rotations, checksum {check}");
}
