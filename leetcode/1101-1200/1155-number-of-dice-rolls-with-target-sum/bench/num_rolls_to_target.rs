// LeetCode #1155 bench -- mirrors num_rolls_to_target.kara: the same 64
// problems, the same passes, the ★ arm's rolling counts.

fn num_rolls_to_target(n: i64, k: i64, target: i64) -> i64 {
    let modulus = 1_000_000_007;
    let t = target as usize;
    let mut ways: Vec<i64> = vec![0; t + 1];
    ways[0] = 1;
    for _ in 0..n {
        let mut next: Vec<i64> = vec![0; t + 1];
        for s in 0..t + 1 {
            if ways[s] != 0 {
                for face in 1..k as usize + 1 {
                    if s + face > t {
                        break;
                    }
                    next[s + face] = (next[s + face] + ways[s]) % modulus;
                }
            }
        }
        ways = next;
    }
    ways[t]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let passes = 250;
    let mut seed = 1155;
    let mut problems: Vec<(i64, i64, i64)> = Vec::new();
    for _ in 0..64 {
        let n = 1 + next_random(&mut seed) % 30;
        let k = 1 + next_random(&mut seed) % 30;
        let most = if n * k < 1000 { n * k } else { 1000 };
        problems.push((n, k, n + next_random(&mut seed) % (most - n + 1)));
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for &(n, k, target) in problems.iter() {
            check = (check * 31 + num_rolls_to_target(n, k, target) + p) % 1000000007;
        }
    }
    println!("{passes} passes over 64 problems: checksum {check}");
}
