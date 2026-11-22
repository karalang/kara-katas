// LeetCode #2839: Check if Strings Can be Made Equal With Operations I --
// the bench, mirrored from equal.kara: the even pair and the odd pair,
// each either way round.

fn can_be_equal(s1: &str, s2: &str) -> bool {
    let a: Vec<char> = s1.chars().collect();
    let b: Vec<char> = s2.chars().collect();
    let pair = |x: char, y: char, p: char, q: char| (x == p && y == q) || (x == q && y == p);
    pair(a[0], a[2], b[0], b[2]) && pair(a[1], a[3], b[1], b[3])
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn word(seed: &mut i64) -> Vec<u8> {
    (0..4).map(|_| (97 + next_random(seed) % 4) as u8).collect()
}

fn main() {
    let count = 1000000;
    let rounds = 20;
    let mut seed = 2839;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for _ in 0..count {
        let a = word(&mut seed);
        let b = if next_random(&mut seed) % 2 == 0 {
            let mut c = a.clone();
            c.swap(0, 2);
            c
        } else {
            word(&mut seed)
        };
        pairs.push((String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap()));
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (s1, s2) in pairs.iter() {
            let same = can_be_equal(s1, s2);
            if same {
                yes += 1;
            }
            check = (check * 31 + if same { 2 } else { 1 } + r) % 1000000007;
        }
    }
    println!("{count} pairs, {rounds} rounds: {yes} true, checksum {check}");
}
