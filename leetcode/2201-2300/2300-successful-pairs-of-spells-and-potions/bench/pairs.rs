// LeetCode #2300: Successful Pairs of Spells and Potions -- the bench,
// the ★ arm in Rust. Sort a copy of the potions, then for each spell
// count the potions past the `partition_point` of those whose product
// with it falls short of `success`.

fn successful_pairs(spells: &[i64], potions: &[i64], success: i64) -> Vec<i64> {
    let mut sorted = potions.to_vec();
    sorted.sort();
    let m = sorted.len() as i64;
    let mut out = Vec::new();
    for &spell in spells {
        out.push(m - sorted.partition_point(|&p| spell * p < success) as i64);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2300;
    let mut spells: Vec<Vec<i64>> = Vec::new();
    let mut potions: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut s = Vec::new();
        let mut p = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            s.push((hi * 32768 + next_random(&mut seed)) % 100000 + 1);
            let hi = next_random(&mut seed);
            p.push((hi * 32768 + next_random(&mut seed)) % 100000 + 1);
        }
        spells.push(s);
        potions.push(p);
    }
    let mut check: i64 = 0;
    for pass in 0..5i64 {
        for c in 0..10usize {
            let out = successful_pairs(&spells[c], &potions[c], 1000000000 * c as i64 + 7 + pass);
            for x in out {
                check = (check * 31 + x) % 1000000007;
            }
        }
    }
    println!("5 passes over 10 cases of 10^5 spells and potions: checksum {}", check);
}
