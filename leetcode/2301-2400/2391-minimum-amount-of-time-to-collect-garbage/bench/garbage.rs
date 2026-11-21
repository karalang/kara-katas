// LeetCode #2391: Minimum Amount of Time to Collect Garbage -- the bench,
// the ★ arm in Rust: the units counted once, each truck driven to the
// last house holding its kind by the travel's prefix sums.

fn garbage_collection(garbage: &[String], travel: &[i64]) -> i64 {
    let mut minutes = 0i64;
    let mut last = [0usize; 3];
    for (i, house) in garbage.iter().enumerate() {
        for &b in house.as_bytes() {
            minutes += 1;
            let kind = if b == b'M' {
                0
            } else if b == b'P' {
                1
            } else {
                2
            };
            last[kind] = i;
        }
    }
    let mut prefix: Vec<i64> = vec![0];
    for &t in travel {
        prefix.push(prefix[prefix.len() - 1] + t);
    }
    for kind in 0..3 {
        minutes += prefix[last[kind]];
    }
    minutes
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2391i64;
    let mut streets: Vec<Vec<String>> = Vec::new();
    let mut roads: Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        let mut street = Vec::new();
        for _ in 0..2000 {
            let len = 1 + next_random(&mut seed) % 10;
            let b: Vec<u8> = (0..len).map(|_| b"MPG"[(next_random(&mut seed) % 3) as usize]).collect();
            street.push(String::from_utf8(b).unwrap());
        }
        streets.push(street);
        roads.push((1..2000).map(|_| 1 + next_random(&mut seed) % 100).collect());
    }
    let mut check = 0i64;
    for p in 0..500i64 {
        for s in 0..50 {
            check = (check * 31 + garbage_collection(&streets[s], &roads[s]) + p) % 1000000007;
        }
    }
    println!("500 passes over 50 streets of 2000 houses: checksum {}", check);
}
