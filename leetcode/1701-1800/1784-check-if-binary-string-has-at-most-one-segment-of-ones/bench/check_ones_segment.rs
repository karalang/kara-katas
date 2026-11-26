// LeetCode #1784: Check if Binary String Has at Most One Segment of Ones --
// the bench in Rust, mirroring check_ones_segment.kara: a search for "01".

fn check_ones_segment(s: &str) -> bool {
    !s.contains("01")
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1784;
    let mut strings: Vec<String> = Vec::new();
    for k in 0..4000 {
        let ones = (1 + next_random(&mut seed) % 100) as usize;
        let mut s = "1".repeat(ones);
        s.push_str(&"0".repeat(100 - ones));
        if k % 2 == 1 && ones < 100 {
            let at = ones + (next_random(&mut seed) % (100 - ones as i64)) as usize;
            s = format!("{}1{}", &s[0..at], &s[at + 1..100]);
        }
        strings.push(s);
    }
    let mut check: i64 = 0;
    for call in 0..4000000i64 {
        let s = &strings[((check + call) % 4000) as usize];
        check = (check * 31 + if check_ones_segment(s) { 2 } else { 1 }) % 1000000007;
    }
    println!("4000000 calls over 4000 strings: checksum {}", check);
}
