// LeetCode #2301: Match Substring After Replacement -- the bench, the ★
// arm in Rust. A table of which letter may stand for which, then every
// start of `sub` in `s` checked against it.

fn match_replacement(s: &str, sub: &str, mappings: &[(char, char)]) -> bool {
    let mut can = vec![false; 128 * 128];
    for c in 0..128 {
        can[c * 128 + c] = true;
    }
    for &(old, new) in mappings {
        can[old as usize * 128 + new as usize] = true;
    }
    let s = s.as_bytes();
    let sub = sub.as_bytes();
    for start in 0..=s.len() - sub.len() {
        let mut all = true;
        for j in 0..sub.len() {
            if !can[sub[j] as usize * 128 + s[start + j] as usize] {
                all = false;
                break;
            }
        }
        if all {
            return true;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2301;
    let ab = ['a', 'b'];
    let xyz = ['x', 'y', 'z'];
    let mut texts: Vec<String> = Vec::new();
    let mut subs: Vec<String> = Vec::new();
    let mut maps: Vec<Vec<(char, char)>> = Vec::new();
    for _ in 0..50 {
        let mut s = String::new();
        for _ in 0..20000 {
            s.push(ab[(next_random(&mut seed) % 2) as usize]);
        }
        let mut sub = String::new();
        for _ in 0..40 {
            let r = next_random(&mut seed) % 4;
            sub.push(if r < 2 { 'c' } else { ab[(r - 2) as usize] });
        }
        let mut mappings = vec![('c', 'a'), ('c', 'b')];
        for _ in 0..998 {
            let old = xyz[(next_random(&mut seed) % 3) as usize];
            let new = ab[(next_random(&mut seed) % 2) as usize];
            mappings.push((old, new));
        }
        texts.push(s);
        subs.push(sub);
        maps.push(mappings);
    }
    let mut check: i64 = 0;
    for pass in 0..20 {
        for c in 0..50 {
            let ok = match_replacement(&texts[(c + pass) % 50], &subs[c], &maps[c]);
            check = (check * 31 + if ok { c as i64 + 1 } else { 0 }) % 1000000007;
        }
    }
    println!("20 passes over 50 cases of 20000 letters: checksum {}", check);
}
