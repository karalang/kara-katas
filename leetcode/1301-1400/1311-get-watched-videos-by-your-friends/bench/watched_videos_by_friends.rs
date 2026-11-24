// LeetCode #1311 bench, Rust: the ★ arm (a breadth-first walk a level at a
// time, the videos of the people left counted in a `HashMap`, then sorted as
// (count, title) pairs) on the same 50 groups and 200 passes.
use std::collections::HashMap;

fn watched_videos_by_friends(watched_videos: &[Vec<String>], friends: &[Vec<i64>], id: i64, level: i64) -> Vec<String> {
    let n = friends.len();
    let mut seen = vec![false; n];
    seen[id as usize] = true;
    let mut people: Vec<i64> = vec![id];
    for _ in 0..level {
        let mut next: Vec<i64> = Vec::new();
        for &p in &people {
            for &f in &friends[p as usize] {
                if !seen[f as usize] {
                    seen[f as usize] = true;
                    next.push(f);
                }
            }
        }
        people = next;
    }
    let mut count: HashMap<String, i64> = HashMap::new();
    for &p in &people {
        for video in &watched_videos[p as usize] {
            *count.entry(video.clone()).or_insert(0) += 1;
        }
    }
    let mut ranked: Vec<(i64, String)> = count.into_iter().map(|(video, c)| (c, video)).collect();
    ranked.sort();
    ranked.into_iter().map(|(_, video)| video).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn fold(check: i64, title: &str) -> i64 {
    let mut c = check;
    for ch in title.chars() {
        c = (c * 31 + ch as i64) % 1000000007;
    }
    c
}

fn main() {
    let letters: Vec<char> = "abcdefghijklmnopqrstuvwxyz".chars().collect();
    let mut seed = 1311;
    let mut titles: Vec<String> = Vec::new();
    for _ in 0..400 {
        let len = 1 + next_random(&mut seed) % 8;
        let mut title = String::new();
        for _ in 0..len {
            title.push(letters[(next_random(&mut seed) % 26) as usize]);
        }
        titles.push(title);
    }
    let n: i64 = 100;
    let mut groups: Vec<Vec<Vec<String>>> = Vec::new();
    let mut links: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..50 {
        let mut friends: Vec<Vec<i64>> = vec![Vec::new(); n as usize];
        for a in 0..n {
            for b in a + 1..n {
                if next_random(&mut seed) % 25 == 0 {
                    friends[a as usize].push(b);
                    friends[b as usize].push(a);
                }
            }
        }
        let mut watched: Vec<Vec<String>> = Vec::new();
        for _ in 0..n {
            let mut videos: Vec<String> = Vec::new();
            for _ in 0..100 {
                videos.push(titles[(next_random(&mut seed) % 400) as usize].clone());
            }
            watched.push(videos);
        }
        groups.push(watched);
        links.push(friends);
    }
    let mut check: i64 = 0;
    for pass in 0..200 {
        for g in 0..50 {
            groups[g][(check % n) as usize][((check / 7) % 100) as usize] = titles[((check / 11) % 400) as usize].clone();
            let id = (check / 13) % n;
            let level = 1 + (check / 17) % 3;
            let got = watched_videos_by_friends(&groups[g], &links[g], id, level);
            check = (check * 31 + got.len() as i64) % 1000000007;
            if !got.is_empty() {
                check = fold(check, &got[0]);
                check = fold(check, &got[got.len() - 1]);
            }
            check = (check + pass) % 1000000007;
        }
    }
    println!("200 passes over 50 groups of 100: checksum {}", check);
}
