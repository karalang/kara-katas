// Benchmark for #599: the ★ arm (index the first list in a HashMap, then
// walk the second); see find_restaurant.kara.

use std::collections::HashMap;

fn find_restaurant(list1: &[String], list2: &[String]) -> Vec<String> {
    let mut index: HashMap<String, usize> = HashMap::new();
    for (i, s) in list1.iter().enumerate() {
        index.insert(s.clone(), i);
    }
    let mut best = list1.len() + list2.len();
    let mut answer: Vec<String> = Vec::new();
    for (j, s) in list2.iter().enumerate() {
        if let Some(&i) = index.get(s) {
            let sum = i + j;
            if sum < best {
                best = sum;
                answer.clear();
            }
            if sum == best {
                answer.push(s.clone());
            }
        }
    }
    answer
}

// ---- benchmark ----------------------------------------------------------------

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// Spells k in lower-case letters, base 26, the last letter the units.
fn spell(k: i64) -> String {
    let mut letters: Vec<u8> = Vec::new();
    let mut n = k;
    loop {
        letters.push(b'a' + (n % 26) as u8);
        n /= 26;
        if n == 0 {
            break;
        }
    }
    letters.reverse();
    String::from_utf8(letters).unwrap()
}

fn main() {
    let count = 100;
    let rounds = 100;
    let mut seed: i64 = 599;
    let mut pool: Vec<String> = Vec::new();
    for k in 0..3000 {
        let number = step(&mut seed) * 32768 + step(&mut seed);
        pool.push(format!("restaurant {} at {}", spell(k), spell(number)));
    }
    let mut order: Vec<usize> = (0..pool.len()).collect();
    let mut pairs: Vec<(Vec<String>, Vec<String>)> = Vec::new();
    for _ in 0..count {
        let mut lists: Vec<Vec<String>> = Vec::new();
        for _ in 0..2 {
            let mut list: Vec<String> = Vec::new();
            for k in 0..1000 {
                let j = k + step(&mut seed) as usize % (pool.len() - k);
                order.swap(k, j);
                list.push(pool[order[k]].clone());
            }
            lists.push(list);
        }
        let second = lists.pop().unwrap();
        let first = lists.pop().unwrap();
        pairs.push((first, second));
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let pair = &pairs[(round * 7 + g) % count];
            let got = find_restaurant(&pair.0, &pair.1);
            total += got.len();
            for s in &got {
                checksum = (checksum * 31 + s.len() as i64) % 1000000007;
                checksum = (checksum * 31 + *s.as_bytes().last().unwrap() as i64) % 1000000007;
            }
        }
    }
    println!("{} pairs, {} rounds: total {}, checksum {}", count, rounds, total, checksum);
}
