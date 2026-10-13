// Benchmark for #533: Rust mirror of the ★ arm (count each kind of row);
// see find_black_pixel.kara. `HashMap<String, i64>` with its default
// SipHash-1-3, the hasher Kāra's `Map` uses too.
use std::collections::HashMap;

fn find_black_pixel(picture: &Vec<Vec<char>>, target: i64) -> i64 {
    let n = picture[0].len();
    let mut cols = vec![0i64; n];
    let mut rows: HashMap<String, i64> = HashMap::new();
    for row in picture.iter() {
        let mut key = String::new();
        let mut blacks = 0;
        for c in 0..n {
            key.push(row[c]);
            if row[c] == 'B' {
                cols[c] += 1;
                blacks += 1;
            }
        }
        if blacks == target {
            *rows.entry(key).or_insert(0) += 1;
        }
    }
    let mut lonely = 0;
    for (key, count) in rows.iter() {
        if *count != target {
            continue;
        }
        for (c, ch) in key.chars().enumerate() {
            if ch == 'B' && cols[c] == target {
                lonely += target;
            }
        }
    }
    lonely
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_picture(seed: &mut i64, n: i64, target: i64, planted: i64, extra: i64, percent: i64) -> Vec<Vec<char>> {
    let mut picture: Vec<Vec<char>> = Vec::new();
    for _ in 0..planted {
        let mut cols: Vec<i64> = (0..n).collect();
        let mut row = vec!['W'; n as usize];
        for i in 0..target {
            let j = i + next_random(seed) % (n - i);
            cols.swap(i as usize, j as usize);
            row[cols[i as usize] as usize] = 'B';
        }
        let copies = if next_random(seed) % 4 == 0 { target + 1 } else { target };
        for _ in 0..copies {
            picture.push(row.clone());
        }
    }
    for _ in 0..extra {
        let mut row: Vec<char> = Vec::new();
        for _ in 0..n {
            row.push(if next_random(seed) % 100 < percent { 'B' } else { 'W' });
        }
        picture.push(row);
    }
    for i in (1..picture.len()).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        picture.swap(i, j);
    }
    picture
}

fn main() {
    // 20 pictures 200 wide made once, the p-th with 20 rows planted for a
    // target of 1 + p % 8 and 80 more black with a chance of 1%; then
    // each picture is answered for every target from 1 to 8, in 100
    // rounds.
    let mut seed: i64 = 533;
    let mut pictures: Vec<Vec<Vec<char>>> = Vec::new();
    for p in 0..20 {
        pictures.push(random_picture(&mut seed, 200, 1 + p % 8, 20, 80, 1));
    }
    let mut total = 0i64;
    let mut checksum = 0i64;
    for _ in 0..100 {
        for p in 0..pictures.len() {
            for target in 1..=8 {
                let answer = find_black_pixel(&pictures[p], target);
                total += answer;
                checksum = (checksum * 31 + answer) % 1000000007;
            }
        }
    }
    println!("20 pictures 200 wide, targets 1 to 8, 100 rounds: total {}, checksum {}", total, checksum);
}
