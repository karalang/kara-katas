// LeetCode #1221 bench, Rust mirror of the Kāra ★ arm: walk the string
// keeping L's count less R's and count the returns to zero, over 2000
// random balanced strings of 1000 letters drawn once, 20 passes; checksum
// of the answers.

fn balanced_string_split(s: &str) -> i64 {
    let mut balance: i64 = 0;
    let mut pieces: i64 = 0;
    for c in s.chars() {
        if c == 'L' {
            balance += 1;
        } else {
            balance -= 1;
        }
        if balance == 0 {
            pieces += 1;
        }
    }
    pieces
}

fn main() {
    let mut seed: i64 = 1221;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..2000 {
        let mut letters: Vec<char> = Vec::new();
        for _ in 0..500 {
            letters.push('L');
            letters.push('R');
        }
        let mut k = letters.len() - 1;
        while k > 0 {
            let j = (next_random() % (k as i64 + 1)) as usize;
            letters.swap(k, j);
            k -= 1;
        }
        strings.push(letters.iter().collect());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..20 {
        for s in strings.iter() {
            let answer = balanced_string_split(s);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    println!("2000 strings of 1000 letters, 20 passes: pieces total {}, checksum {}", total, check);
}
