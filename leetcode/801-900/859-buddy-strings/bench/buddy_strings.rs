// LeetCode #859: Buddy Strings -- Rust mirror of the bench program (the ★
// arm, one pass over the positions where the strings differ).

fn buddy_strings(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut first: i64 = -1;
    let mut second: i64 = -1;
    for i in 0..a.len() {
        if a[i] != b[i] {
            if first < 0 {
                first = i as i64;
            } else if second < 0 {
                second = i as i64;
            } else {
                return false;
            }
        }
    }
    if first < 0 {
        let mut seen = [false; 26];
        for &c in a {
            let k = (c - 97) as usize;
            if seen[k] {
                return true;
            }
            seen[k] = true;
        }
        return false;
    }
    let (f, s) = (first as usize, second as usize);
    second >= 0 && a[f] == b[s] && a[s] == b[f]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 20000;
    let mut seed: i64 = 859;
    let mut s: Vec<u8> = Vec::new();
    for _ in 0..n {
        s.push((97 + next_random(&mut seed) % 26) as u8);
    }
    let mut goal = s.clone();
    let mut buddies: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..40000i64 {
        let i = (next_random(&mut seed) % n) as usize;
        let j = (next_random(&mut seed) % n) as usize;
        let kind = r % 3;
        let old = goal[i];
        if kind == 1 {
            goal[i] = (97 + (old as i64 - 97 + 1 + next_random(&mut seed) % 25) % 26) as u8;
        } else {
            goal.swap(i, j);
        }
        let k = (next_random(&mut seed) % n) as usize;
        let l = (next_random(&mut seed) % n) as usize;
        if kind == 2 {
            goal.swap(k, l);
        }
        let yes = buddy_strings(&s, &goal);
        if kind == 2 {
            goal.swap(k, l);
        }
        if kind == 1 {
            goal[i] = old;
        } else {
            goal.swap(i, j);
        }
        if yes {
            buddies += 1;
        }
        check = (check * 31 + if yes { r + 2 } else { 1 }) % 1000000007;
    }
    println!("40000 rounds on 20000 letters: {} buddies, checksum {}", buddies, check);
}
