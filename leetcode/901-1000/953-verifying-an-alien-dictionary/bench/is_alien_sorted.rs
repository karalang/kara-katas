// LeetCode #953: Verifying an Alien Dictionary -- Rust mirror of the Kara
// bench program (a rank per letter).

fn is_alien_sorted(words: &[String], order: &str) -> bool {
    let mut rank = [0i64; 26];
    let letters = order.as_bytes();
    for i in 0..26 {
        rank[(letters[i] - b'a') as usize] = i as i64;
    }
    for w in 1..words.len() {
        let a = words[w - 1].as_bytes();
        let b = words[w].as_bytes();
        let mut k = 0;
        while k < a.len() && k < b.len() && a[k] == b[k] {
            k += 1;
        }
        if k == b.len() {
            if k < a.len() {
                return false;
            }
        } else if k < a.len() && rank[(a[k] - b'a') as usize] > rank[(b[k] - b'a') as usize] {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn before(a: &str, b: &str, rank: &[i64; 26]) -> bool {
    let x = a.as_bytes();
    let y = b.as_bytes();
    let mut k = 0;
    while k < x.len() && k < y.len() && x[k] == y[k] {
        k += 1;
    }
    if k == y.len() {
        false
    } else if k == x.len() {
        true
    } else {
        rank[(x[k] - b'a') as usize] < rank[(y[k] - b'a') as usize]
    }
}

fn main() {
    let rounds = 2000;
    let count = 200;
    let n = 100;
    let mut seed = 953i64;
    let mut orders: Vec<String> = Vec::new();
    let mut sets: Vec<Vec<String>> = Vec::new();
    for s in 0..count {
        let mut letters: Vec<u8> = (0..26).map(|i| b'a' + i as u8).collect();
        for i in 0..26 {
            let j = i + (next_random(&mut seed) % (26 - i as i64)) as usize;
            letters.swap(i, j);
        }
        let mut rank = [0i64; 26];
        let mut order = String::new();
        for i in 0..26 {
            rank[(letters[i] - b'a') as usize] = i as i64;
            order.push(letters[i] as char);
        }
        let mut words: Vec<String> = Vec::new();
        for _ in 0..n {
            let m = 1 + next_random(&mut seed) % 20;
            let mut w = String::new();
            for _ in 0..m {
                w.push(letters[(next_random(&mut seed) % 3) as usize] as char);
            }
            words.push(w);
        }
        for i in 1..n {
            let mut j = i;
            while j > 0 && before(&words[j], &words[j - 1], &rank) {
                words.swap(j, j - 1);
                j -= 1;
            }
        }
        if s % 3 == 2 {
            words.swap(n - 2, n - 1);
        }
        orders.push(order);
        sets.push(words);
    }
    let mut sorted = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for i in 0..count {
            let k = (r + i) % count;
            let ok = is_alien_sorted(&sets[k], &orders[k]);
            if ok {
                sorted += 1;
            }
            check = (check * 31 + if ok { 1 } else { 2 }) % 1000000007;
        }
    }
    println!("{} rounds over {} sets of {} words: {} sorted, checksum {}", rounds, count, n, sorted, check);
}
