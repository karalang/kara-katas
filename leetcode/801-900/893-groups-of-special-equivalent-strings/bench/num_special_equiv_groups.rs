// LeetCode #893 bench: the union-find arm (every pair of words compared by
// their counts of letters at even and at odd positions) on 300 lists of
// 1,000 words of 20 letters. The same algorithm as
// num_special_equiv_groups.kara.

fn num_special_equiv_groups(words: &[String]) -> i64 {
    let n = words.len();
    let mut counts: Vec<Vec<i64>> = Vec::new();
    for word in words {
        let mut count = vec![0i64; 52];
        let bytes = word.as_bytes();
        for i in 0..bytes.len() {
            count[(bytes[i] - 97) as usize + 26 * (i % 2)] += 1;
        }
        counts.push(count);
    }
    let mut parent: Vec<usize> = (0..n).collect();
    for i in 0..n {
        for j in i + 1..n {
            if counts[i] == counts[j] {
                let a = find(&mut parent, i);
                let b = find(&mut parent, j);
                if a != b {
                    parent[a] = b;
                }
            }
        }
    }
    let mut groups = 0;
    for i in 0..n {
        if find(&mut parent, i) == i {
            groups += 1;
        }
    }
    groups
}

fn find(parent: &mut [usize], x: usize) -> usize {
    let mut x = x;
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_word(seed: &mut i64, len: i64, letters: i64) -> String {
    let mut w = String::new();
    for _ in 0..len {
        w.push((97 + next_random(seed) % letters) as u8 as char);
    }
    w
}

fn shuffled(seed: &mut i64, word: &str) -> String {
    let mut b = word.as_bytes().to_vec();
    let n = b.len() as i64;
    for _ in 0..n {
        let i = next_random(seed) % n;
        let j = next_random(seed) % n;
        if i % 2 == j % 2 {
            b.swap(i as usize, j as usize);
        }
    }
    String::from_utf8(b).unwrap()
}

fn main() {
    let mut seed = 893;
    let mut groups = 0;
    let mut check = 0;
    for _ in 0..300 {
        let mut words: Vec<String> = Vec::new();
        for _ in 0..1000 {
            if !words.is_empty() && next_random(&mut seed) % 2 == 0 {
                let k = (next_random(&mut seed) % words.len() as i64) as usize;
                let w = shuffled(&mut seed, &words[k]);
                words.push(w);
            } else {
                words.push(random_word(&mut seed, 20, 26));
            }
        }
        let got = num_special_equiv_groups(&words);
        groups += got;
        check = (check * 131 + got) % 1000000007;
    }
    println!("300 lists of 1000 words of 20 letters: {} groups, checksum {}", groups, check);
}
