// LeetCode #2423: Remove Letter To Equalize Frequency -- the bench, the ★
// arm: the 26 letter counts, each held letter taken away once in turn and
// the counts left that are not zero compared.

fn equal_frequency(word: &[u8]) -> bool {
    let mut count = [0i64; 26];
    for &b in word {
        count[(b - b'a') as usize] += 1;
    }
    for c in 0..26 {
        if count[c] == 0 {
            continue;
        }
        count[c] -= 1;
        let mut want = 0;
        let mut equal = true;
        for k in 0..26 {
            if count[k] > 0 {
                if want == 0 {
                    want = count[k];
                } else if count[k] != want {
                    equal = false;
                }
            }
        }
        count[c] += 1;
        if equal {
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
    let mut seed = 2423;
    let mut words: Vec<Vec<u8>> = Vec::new();
    for _ in 0..10000 {
        let kinds = 1 + next_random(&mut seed) % 20;
        let times = 1 + next_random(&mut seed) % 5;
        let mut bytes: Vec<u8> = Vec::new();
        for k in 0..kinds {
            for _ in 0..times {
                bytes.push(b'a' + k as u8);
            }
        }
        if next_random(&mut seed) % 2 == 0 {
            bytes.push(b'a' + (next_random(&mut seed) % 26) as u8);
        } else {
            let at = (next_random(&mut seed) % bytes.len() as i64) as usize;
            bytes.remove(at);
        }
        for i in (1..bytes.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            bytes.swap(i, j);
        }
        while bytes.len() < 2 {
            bytes.push(b'a');
        }
        words.push(bytes);
    }
    let mut check: i64 = 0;
    for p in 0..200 {
        for w in words.iter() {
            check = (check * 3 + if equal_frequency(w) { 1 } else { 0 } + p) % 1000000007;
        }
    }
    println!("200 passes over 10^4 words: checksum {}", check);
}
