// Benchmark harness for LeetCode #242 — Valid Anagram.
// Mirrors valid_anagram.kara algorithm-for-algorithm.

fn is_anagram(s: &[u8], t: &[u8]) -> bool {
    if s.len() != t.len() {
        return false;
    }
    let mut count = [0i64; 26];
    for i in 0..s.len() {
        count[(s[i] as usize) - 97] += 1;
        count[(t[i] as usize) - 97] -= 1;
    }
    for j in 0..26 {
        if count[j] != 0 {
            return false;
        }
    }
    true
}

fn main() {
    let np: i64 = 8;
    let sl: i64 = 20000;
    let iters: i64 = 8000;

    let mut esses: Vec<Vec<u8>> = Vec::new();
    let mut tees: Vec<Vec<u8>> = Vec::new();
    for j in 0..np {
        let mut sj: Vec<u8> = Vec::new();
        for k in 0..sl {
            sj.push((97 + ((k * 7 + j) % 26)) as u8);
        }
        let mut tj: Vec<u8> = Vec::new();
        let mut m = sl - 1;
        while m >= 0 {
            let mut b = sj[m as usize] as i64;
            if j % 2 == 1 && m == 0 {
                b = 97 + ((b - 97 + 1) % 26);
            }
            tj.push(b as u8);
            m -= 1;
        }
        esses.push(sj);
        tees.push(tj);
    }

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        if is_anagram(&esses[idx], &tees[idx]) {
            sink += it + 1;
        } else {
            sink += 1;
        }
    }
    println!("{}", sink);
}
