// LeetCode #2515: Shortest Distance to Target String in a Circular Array
// -- Rust mirror of the benchmark (closest.kara): the same lists, passes,
// order and checksum.

fn closet_target(words: &[String], target: &str, start: i64) -> i64 {
    let n = words.len() as i64;
    let mut best = -1;
    for i in 0..n {
        if words[i as usize] == target {
            let d = (i - start).abs();
            let shortest = d.min(n - d);
            if best == -1 || shortest < best {
                best = shortest;
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2515;
    let mut lists: Vec<Vec<String>> = Vec::new();
    for _ in 0..2000 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100 {
            let mut w = String::new();
            let length = next_random(&mut seed) % 3 + 1;
            for _ in 0..length {
                w.push((b'a' + (next_random(&mut seed) % 3) as u8) as char);
            }
            words.push(w);
        }
        lists.push(words);
    }
    let passes = 900;
    let mut check: i64 = 0;
    for p in 0..passes {
        for words in lists.iter() {
            let target = words[(check / 100 % 100) as usize].clone();
            check = (check * 31 + closet_target(words, &target, check % 100) + p) % 1000000007;
        }
    }
    println!("{} passes over 2000 lists of 100 words: checksum {}", passes, check);
}
