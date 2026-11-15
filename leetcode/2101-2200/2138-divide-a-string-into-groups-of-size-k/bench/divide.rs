// LeetCode #2138: Divide a String Into Groups of Size k -- the benchmark,
// the same algorithm as divide.kara.

fn divide_string(s: &str, k: usize, fill: char) -> Vec<String> {
    let n = s.len();
    let mut groups = Vec::new();
    let mut start = 0;
    while start < n {
        let mut group = s[start..(start + k).min(n)].to_string();
        while group.len() < k {
            group.push(fill);
        }
        groups.push(group);
        start += k;
    }
    groups
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let alphabet: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 2138;
    let mut strings: Vec<Vec<char>> = Vec::new();
    for _ in 0..1000 {
        let mut s = Vec::new();
        for _ in 0..100 {
            s.push(alphabet[(next_random(&mut seed) % 26) as usize]);
        }
        strings.push(s);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..100 {
        for i in 0..1000 {
            let at = (next_random(&mut seed) % 100) as usize;
            strings[i][at] = alphabet[(next_random(&mut seed) % 26) as usize];
            let k = (next_random(&mut seed) % 100 + 1) as usize;
            let fill = alphabet[(next_random(&mut seed) % 26) as usize];
            let s: String = strings[i].iter().collect();
            let groups = divide_string(&s, k, fill);
            total += groups.len() as i64;
            for b in groups[groups.len() - 1].bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
        }
    }
    println!("100000 solves: {} groups, checksum {}", total, check);
}
