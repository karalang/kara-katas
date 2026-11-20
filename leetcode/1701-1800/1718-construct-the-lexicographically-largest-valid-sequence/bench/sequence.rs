// LeetCode #1718: Construct the Lexicographically Largest Valid Sequence
// -- the bench (sequence.kara): the first empty slot filled with the
// largest number that fits, backtracking when none does.

fn place(seq: &mut Vec<i32>, used: &mut Vec<bool>, at: usize, n: i32) -> bool {
    let mut at = at;
    while at < seq.len() && seq[at] != 0 {
        at += 1;
    }
    if at == seq.len() {
        return true;
    }
    for v in (1..=n).rev() {
        let u = v as usize;
        if used[u] {
            continue;
        }
        if v > 1 && (at + u >= seq.len() || seq[at + u] != 0) {
            continue;
        }
        used[u] = true;
        seq[at] = v;
        if v > 1 {
            seq[at + u] = v;
        }
        if place(seq, used, at + 1, n) {
            return true;
        }
        used[u] = false;
        seq[at] = 0;
        if v > 1 {
            seq[at + u] = 0;
        }
    }
    false
}

fn construct_distanced_sequence(n: i32) -> Vec<i32> {
    let mut seq = vec![0i32; (2 * n - 1) as usize];
    let mut used = vec![false; (n + 1) as usize];
    place(&mut seq, &mut used, 0, n);
    seq
}

fn main() {
    let rounds: i64 = 2000;
    let mut values: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for n in 1..=20 {
            for &v in construct_distanced_sequence(n).iter() {
                values += 1;
                check = (check * 31 + v as i64 + r) % 1000000007;
            }
        }
    }
    println!("every n from 1 to 20, {} rounds: {} values, checksum {}", rounds, values, check);
}
