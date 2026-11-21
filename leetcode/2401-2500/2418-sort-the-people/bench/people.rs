// LeetCode #2418: Sort the People -- the bench, the ★ arm in Rust: the
// indexes sorted by height, tallest first, and each index's name read out.

fn sort_people(names: &[String], heights: &[i64]) -> Vec<String> {
    let mut order: Vec<usize> = (0..names.len()).collect();
    order.sort_by(|&a, &b| heights[b].cmp(&heights[a]));
    let mut sorted = Vec::new();
    for &i in order.iter() {
        sorted.push(names[i].clone());
    }
    sorted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 10 groups of 1000 people, names of 1 to 20 letters, distinct heights
    // up to 10^5; each pass sorts every group and folds the first letter
    // of every name, plus the pass
    let mut seed = 2418;
    let mut groups: Vec<(Vec<String>, Vec<i64>)> = Vec::new();
    for _ in 0..10 {
        let mut names = Vec::new();
        for _ in 0..1000 {
            let len = 1 + next_random(&mut seed) % 20;
            let bytes: Vec<u8> = (0..len).map(|_| b'a' + (next_random(&mut seed) % 26) as u8).collect();
            names.push(String::from_utf8(bytes).unwrap());
        }
        let mut pool: Vec<i64> = (1..100001).collect();
        for i in 0..1000usize {
            let a = next_random(&mut seed);
            let j = i + ((a * 32768 + next_random(&mut seed)) % (100000 - i as i64)) as usize;
            pool.swap(i, j);
        }
        groups.push((names, pool[0..1000].to_vec()));
    }
    let mut check: i64 = 0;
    for p in 0..500 {
        for (names, heights) in groups.iter() {
            for name in sort_people(names, heights).iter() {
                check = (check * 31 + name.as_bytes()[0] as i64 + p) % 1000000007;
            }
        }
    }
    println!("500 passes over 10 groups of 1000 people: checksum {}", check);
}
