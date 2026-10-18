// LeetCode #717: 1-bit and 2-bit Characters -- read from the start.
// Benchmark mirror of the Kara star arm: step past one bit on a 0 and
// two on a 1; the last character is one bit when a step lands on the
// last bit.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn is_one_bit_character(bits: &[i64]) -> bool {
    let n = bits.len();
    let mut i = 0;
    while i < n - 1 {
        i += bits[i] as usize + 1;
    }
    i == n - 1
}

fn main() {
    let mut seed: i64 = 717;
    let mut strings: Vec<Vec<i64>> = Vec::new();
    for s in 0..100 {
        let density = 1 + s % 3;
        let mut bits: Vec<i64> = Vec::new();
        for _ in 0..9999 {
            bits.push(if next_random(&mut seed) % 4 < density { 1 } else { 0 });
        }
        bits.push(0);
        strings.push(bits);
    }
    let mut yes = 0;
    for round in 0..400 {
        for bits in strings.iter_mut() {
            let at = (round * 997) % 9999;
            bits[at] = 1 - bits[at];
        }
        for bits in strings.iter() {
            if is_one_bit_character(bits) {
                yes += 1;
            }
        }
    }
    println!("400 rounds of 100 strings of 10000 bits: {} one-bit endings", yes);
}
