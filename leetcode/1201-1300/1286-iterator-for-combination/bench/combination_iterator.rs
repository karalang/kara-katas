// LeetCode #1286 bench, in Rust: the ★ arm (the masks with k bits, from the
// largest down) over every length of the 15 letters "abcdefghijklmno",
// 1000 rounds, every combination folded into a checksum.

struct CombinationIterator {
    chars: Vec<char>,
    k: u32,
    mask: i64,
}

impl CombinationIterator {
    fn new(characters: &str, combination_length: i64) -> CombinationIterator {
        let n = characters.len() as i64;
        let mask = ((1i64 << combination_length) - 1) << (n - combination_length);
        CombinationIterator { chars: characters.chars().collect(), k: combination_length as u32, mask }
    }

    fn next(&mut self) -> String {
        let n = self.chars.len();
        let mut out = String::new();
        for i in 0..n {
            if (self.mask >> (n - 1 - i)) & 1 == 1 {
                out.push(self.chars[i]);
            }
        }
        self.mask -= 1;
        while self.mask > 0 && self.mask.count_ones() != self.k {
            self.mask -= 1;
        }
        out
    }

    fn has_next(&self) -> bool {
        self.mask > 0
    }
}

fn main() {
    let mut check: i64 = 0;
    for round in 0..1000i64 {
        for k in 1..16 {
            let mut it = CombinationIterator::new("abcdefghijklmno", k);
            while it.has_next() {
                for b in it.next().bytes() {
                    check = (check * 131 + b as i64 + round) % 1000000007;
                }
            }
        }
    }
    println!("1000 rounds of every length of 15 letters: checksum {}", check);
}
