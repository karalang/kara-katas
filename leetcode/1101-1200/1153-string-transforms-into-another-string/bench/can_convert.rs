// LeetCode #1153 bench -- mirrors can_convert.kara: the same 64 pairs,
// the same rounds, the ★ arm's arrays.

fn can_convert(str1: &str, str2: &str) -> bool {
    if str1 == str2 {
        return true;
    }
    let a = str1.as_bytes();
    let b = str2.as_bytes();
    let mut to: Vec<i64> = vec![-1; 26];
    let mut used: Vec<bool> = vec![false; 26];
    let mut letters = 0;
    for i in 0..a.len() {
        let x = (a[i] - b'a') as usize;
        let y = (b[i] - b'a') as i64;
        if to[x] == -1 {
            to[x] = y;
        } else if to[x] != y {
            return false;
        }
        if !used[y as usize] {
            used[y as usize] = true;
            letters += 1;
        }
    }
    letters < 26
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 100000;
    let mut seed = 1153;
    let mut pairs: Vec<(String, String)> = Vec::new();
    for p in 0..64 {
        let a: Vec<u8> = (0..10000).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
        let mut map: Vec<u8> = (0..26).map(|i| b'a' + i as u8).collect();
        for j in (1..26usize).rev() {
            let k = (next_random(&mut seed) % (j as i64 + 1)) as usize;
            map.swap(j, k);
        }
        if p % 4 < 2 {
            let at = (next_random(&mut seed) % 26) as usize;
            map[at] = map[25];
        }
        let mut b: Vec<u8> = if p % 4 == 3 { a.clone() } else { a.iter().map(|&x| map[(x - b'a') as usize]).collect() };
        if p % 4 == 1 {
            let at = (next_random(&mut seed) % 10000) as usize;
            b[at] = if b[at] == b'z' { b'a' } else { b[at] + 1 };
        }
        pairs.push((String::from_utf8(a).unwrap(), String::from_utf8(b).unwrap()));
    }
    let mut yes = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let (a, b) = &pairs[r % 64];
        let ok = can_convert(a, b);
        if ok {
            yes += 1;
        }
        check = (check * 31 + if ok { 2 } else { 1 } + (r % 64) as i64) % 1000000007;
    }
    println!("{} rounds over 64 pairs of 10000 letters: {} convertible, checksum {}", rounds, yes, check);
}
