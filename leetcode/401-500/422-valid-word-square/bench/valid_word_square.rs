// Benchmark for #422: mirror of valid_word_square.kara (every cell
// against its mirror). A flip rebuilds the row, as the Kāra program does.

fn valid_word_square(words: &[String]) -> bool {
    let n = words.len();
    for i in 0..n {
        let row = words[i].as_bytes();
        for j in 0..row.len() {
            if j >= n {
                return false;
            }
            let mirror = words[j].as_bytes();
            if i >= mirror.len() || mirror[i] != row[j] {
                return false;
            }
        }
    }
    true
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn flip(words: &mut [String], i: usize, j: usize) {
    let bytes = words[i].as_bytes();
    let mut word = String::new();
    for k in 0..bytes.len() {
        let b = if k == j { 195 - bytes[k] } else { bytes[k] };
        word.push(b as char);
    }
    words[i] = word;
}

fn main() {
    let rounds: i64 = std::env::args().nth(1).map_or(6000, |s| s.parse().unwrap());
    let n: i64 = 500;
    let mut seed: i64 = 422;
    let mut grid = vec![0i64; (n * n) as usize];
    for i in 0..n {
        for j in i..n {
            let c = step(&mut seed) % 2;
            grid[(i * n + j) as usize] = c;
            grid[(j * n + i) as usize] = c;
        }
    }
    let mut lengths: Vec<i64> = vec![n];
    for i in 1..n as usize {
        let drop = if step(&mut seed) % 4 == 0 { 1 } else { 0 };
        lengths.push((lengths[i - 1] - drop).max(1));
    }
    let mut words: Vec<String> = Vec::new();
    for i in 0..n {
        let mut height = 0;
        while height < n && lengths[height as usize] > i {
            height += 1;
        }
        let mut word = String::new();
        for j in 0..lengths[i as usize].min(height) {
            word.push((97 + grid[(i * n + j) as usize]) as u8 as char);
        }
        words.push(word);
    }
    let cells: usize = words.iter().map(|w| w.len()).sum();
    let mut valid = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let i = (step(&mut seed) % n) as usize;
        let j = (step(&mut seed) % words[i].len() as i64) as usize;
        flip(&mut words, i, j);
        if r % 3 != 0 {
            flip(&mut words, j, i);
        }
        let answer = valid_word_square(&words);
        if answer {
            valid += 1;
        }
        checksum = (checksum * 31 + if answer { r + 1 } else { 0 }) % 1000000007;
        if r % 3 == 0 {
            flip(&mut words, i, j);
        }
    }
    println!("{rounds} rounds on {n} words, {cells} letters: {valid} valid, checksum {checksum}");
}
