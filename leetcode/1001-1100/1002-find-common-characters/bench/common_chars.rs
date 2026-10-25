// Benchmark: LeetCode #1002 Find Common Characters -- the ★ arm, the
// least count of each letter, on lists of 100 words of 100 letters,
// LeetCode's largest. Mirrors common_chars.kara, .c, .py and go-seq/.

fn common_chars(words: &[String]) -> Vec<String> {
    let mut least = vec![1000i64; 26];
    for word in words {
        let mut count = vec![0i64; 26];
        for c in word.chars() {
            count[(c as usize) - ('a' as usize)] += 1;
        }
        for i in 0..26 {
            least[i] = least[i].min(count[i]);
        }
    }
    let mut ans = Vec::new();
    for i in 0..26 {
        for _ in 0..least[i] {
            ans.push(((i as u8 + b'a') as char).to_string());
        }
    }
    ans
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 1000;
    let mut seed: i64 = 1002;
    // 20 lists of 100 words of 100 letters, list t drawing its letters
    // from the first 2 + t % 10 of the alphabet
    let mut lists: Vec<Vec<String>> = Vec::new();
    for t in 0..20 {
        let alphabet = 2 + t % 10;
        let mut words: Vec<String> = Vec::new();
        for _ in 0..100 {
            let mut word = String::new();
            for _ in 0..100 {
                word.push((97 + next_random(&mut seed) % alphabet) as u8 as char);
            }
            words.push(word);
        }
        lists.push(words);
    }
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let ans = common_chars(&lists[(r + i) % 20]);
            found += ans.len() as i64;
            for s in &ans {
                for c in s.chars() {
                    check = (check * 31 + c as i64) % 1000000007;
                }
            }
        }
    }
    println!("{rounds} rounds over 20 lists of 100 words of 100 letters: {found} common letters, checksum {check}");
}
