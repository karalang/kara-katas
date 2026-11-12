// LeetCode #1128: Number of Equivalent Domino Pairs -- the bench in Rust,
// the ★ arm over LeetCode's `Vec<Vec<i32>>` with an array of 100 counts,
// the same 16 sets and 300 rounds.

fn num_equiv_domino_pairs(dominoes: &[Vec<i32>]) -> i64 {
    let mut count = [0i64; 100];
    let mut pairs = 0;
    for d in dominoes {
        let key = (d[0].min(d[1]) * 10 + d[0].max(d[1])) as usize;
        pairs += count[key];
        count[key] += 1;
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1128;
    let mut sets: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..16 {
        let mut dominoes: Vec<Vec<i32>> = Vec::new();
        for _ in 0..40000 {
            let a = next_random(&mut seed) % 9 + 1;
            let b = next_random(&mut seed) % 9 + 1;
            dominoes.push(vec![a as i32, b as i32]);
        }
        sets.push(dominoes);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..300i64 {
        for j in 0..sets.len() {
            let at = ((round * 7919 + j as i64 * 104729) % 40000) as usize;
            let side = (round % 2) as usize;
            sets[j][at][side] = sets[j][at][side] % 9 + 1;
            let answer = num_equiv_domino_pairs(&sets[j]);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("300 rounds over 16 sets of 4 * 10^4 dominoes: pairs total {total}, checksum {check}");
}
