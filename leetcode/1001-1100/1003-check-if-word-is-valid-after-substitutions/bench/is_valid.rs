// Benchmark: LeetCode #1003 Check If Word Is Valid After Substitutions --
// the ★ arm, a stack, on strings of 19998 letters, LeetCode's longest.
// Mirrors is_valid.kara, .c, .py and go-seq/.

fn is_valid(s: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();
    for c in s.chars() {
        stack.push(c);
        let k = stack.len();
        if k >= 3 && stack[k - 3] == 'a' && stack[k - 2] == 'b' && stack[k - 1] == 'c' {
            stack.truncate(k - 3);
        }
    }
    stack.is_empty()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a valid string of `pieces` pieces, made left to right: each step
// either begins a new piece with its a or writes the next letter of the
// latest piece begun, at random
fn random_valid(pieces: i64, seed: &mut i64) -> Vec<char> {
    let mut xs: Vec<char> = Vec::new();
    let mut waiting: Vec<char> = Vec::new();
    let mut left = pieces;
    while left > 0 || !waiting.is_empty() {
        if left > 0 && (waiting.is_empty() || next_random(seed) % 2 == 0) {
            xs.push('a');
            waiting.push('b');
            left -= 1;
        } else {
            let top = waiting.len() - 1;
            let c = waiting[top];
            xs.push(c);
            if c == 'b' {
                waiting[top] = 'c';
            } else {
                waiting.pop();
            }
        }
    }
    xs
}

fn main() {
    let rounds = 250;
    let mut seed: i64 = 1003;
    // 20 strings of 6666 pieces, 19998 letters; the odd ones with one
    // letter changed
    let letters = ['a', 'b', 'c'];
    let mut strings: Vec<String> = Vec::new();
    for t in 0..20 {
        let mut xs = random_valid(6666, &mut seed);
        if t % 2 == 1 {
            let at = (next_random(&mut seed) % xs.len() as i64) as usize;
            xs[at] = letters[((next_random(&mut seed) % 2 + 1 + xs[at] as i64 - 97) % 3) as usize];
        }
        strings.push(xs.iter().collect());
    }
    let mut valid: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let v = if is_valid(&strings[(r + i) % 20]) { 1 } else { 0 };
            valid += v;
            check = (check * 31 + v + i as i64 + 1) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 strings of 19998 letters: {valid} valid, checksum {check}");
}
