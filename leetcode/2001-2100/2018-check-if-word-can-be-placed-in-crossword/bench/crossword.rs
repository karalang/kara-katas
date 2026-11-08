// LeetCode #2018: Check if Word Can Be Placed In Crossword -- the ★ arm's
// benchmark, a mirror of crossword.kara: the lines built and each run
// collected into its own vector per call.

fn fits(segment: &[char], word: &[char]) -> bool {
    let k = word.len();
    if segment.len() != k {
        return false;
    }
    let forward = (0..k).all(|i| segment[i] == ' ' || segment[i] == word[i]);
    let backward = (0..k).all(|i| segment[i] == ' ' || segment[i] == word[k - 1 - i]);
    forward || backward
}

fn place_word_in_crossword(board: &Vec<Vec<char>>, word: &str) -> bool {
    let word: Vec<char> = word.chars().collect();
    let (m, n) = (board.len(), board[0].len());
    let mut lines: Vec<Vec<char>> = board.clone();
    for c in 0..n {
        lines.push((0..m).map(|r| board[r][c]).collect());
    }
    for line in lines.iter() {
        let mut segment: Vec<char> = Vec::new();
        for i in 0..line.len() + 1 {
            if i == line.len() || line[i] == '#' {
                if fits(&segment, &word) {
                    return true;
                }
                segment.clear();
            } else {
                segment.push(line[i]);
            }
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2018;
    let mut boards: Vec<Vec<Vec<char>>> = Vec::new();
    let mut words: Vec<String> = Vec::new();
    for b in 0..120i64 {
        let walls = b % 2 + 1;
        let mut board: Vec<Vec<char>> = Vec::new();
        for _ in 0..200 {
            let mut row: Vec<char> = Vec::new();
            for _ in 0..200 {
                if next_random(&mut seed) % 10 < walls {
                    row.push('#');
                } else if next_random(&mut seed) % 10 < 4 {
                    row.push((b'a' + (next_random(&mut seed) % 3) as u8) as char);
                } else {
                    row.push(' ');
                }
            }
            board.push(row);
        }
        let mut word = String::new();
        for _ in 0..b % 10 + 10 {
            word.push((b'a' + (next_random(&mut seed) % 3) as u8) as char);
        }
        boards.push(board);
        words.push(word);
    }
    let (mut calls, mut placed, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..40 {
        for b in 0..boards.len() {
            let answer = place_word_in_crossword(&boards[b], &words[b]);
            calls += 1;
            if answer {
                placed += 1;
            }
            check = (check * 2 + answer as i64) % 1000000007;
        }
    }
    println!("{} calls: {} placed, checksum {}", calls, placed, check);
}
