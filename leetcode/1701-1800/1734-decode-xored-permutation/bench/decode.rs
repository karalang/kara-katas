// LeetCode #1734: Decode XORed Permutation -- the bench (decode.kara): the
// first value from the XOR of 1 to n less that of the codes at odd places,
// then each next value the last XORed with its code.

fn decode(encoded: &[i32]) -> Vec<i32> {
    let n = encoded.len() + 1;
    let mut all: i32 = 0;
    for v in 1..n + 1 {
        all ^= v as i32;
    }
    let mut rest: i32 = 0;
    let mut i = 1;
    while i < n - 1 {
        rest ^= encoded[i];
        i += 2;
    }
    let mut perm: Vec<i32> = Vec::with_capacity(n);
    perm.push(all ^ rest);
    for &code in encoded.iter() {
        perm.push(perm[perm.len() - 1] ^ code);
    }
    perm
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let count = 50;
    let rounds: i64 = 40;
    let n: usize = 99999;
    let mut seed: i64 = 1734;
    let mut problems: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        let mut perm: Vec<i32> = (1..n + 1).map(|v| v as i32).collect();
        for i in (1..n).rev() {
            let j = (wide(&mut seed) % (i as i64 + 1)) as usize;
            perm.swap(i, j);
        }
        let encoded: Vec<i32> = (0..n - 1).map(|i| perm[i] ^ perm[i + 1]).collect();
        problems.push(encoded);
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for encoded in problems.iter() {
            let perm = decode(encoded);
            sum += perm[0] as i64;
            check = (check * 31 + perm[0] as i64 + perm[n / 2] as i64 + perm[n - 1] as i64 + r)
                % 1000000007;
        }
    }
    println!(
        "{} permutations of {}, {} rounds: first values sum to {}, checksum {}",
        count, n, rounds, sum, check
    );
}
