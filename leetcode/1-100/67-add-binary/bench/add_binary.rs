const W: i64 = 96;

fn add_popcount(bits: &[i64], off_a: i64, off_b: i64) -> i64 {
    let mut carry = 0i64;
    let mut pop = 0i64;
    let mut k = W - 1;
    while k >= 0 {
        let sum = carry + bits[(off_a + k) as usize] + bits[(off_b + k) as usize];
        pop += sum & 1;
        carry = sum >> 1;
        k -= 1;
    }
    pop += carry;
    pop
}

fn main() {
    let bn: i64 = 2000000;
    let passes: i64 = 2600000;

    let mut bits: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..bn {
        state = (state * 1103515245 + 12345) & 2147483647;
        bits.push((state >> 16) & 1);
    }

    let span = bn - W;
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 101 + 7) % bn) as usize;
        bits[idx] = 1 - bits[idx];
        let off_a = (p * 37) % span;
        let off_b = (p * 53 + 17) % span;
        sink += add_popcount(&bits, off_a, off_b);
    }
    println!("{}", sink);
}
