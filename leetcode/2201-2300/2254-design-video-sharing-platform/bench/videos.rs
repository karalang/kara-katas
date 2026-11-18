// LeetCode #2254: Design Video Sharing Platform -- the benchmark's Rust
// mirror of videos.kara: the videos in a `Vec<Option<Video>>` indexed by
// id and the freed ids in a `BinaryHeap<Reverse<i64>>`, smallest first.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

struct Video {
    content: String,
    views: i64,
    likes: i64,
    dislikes: i64,
}

struct Platform {
    slots: Vec<Option<Video>>,
    free: BinaryHeap<Reverse<i64>>,
}

impl Platform {
    fn new() -> Platform {
        Platform { slots: Vec::new(), free: BinaryHeap::new() }
    }

    fn upload(&mut self, video: String) -> i64 {
        let held = Some(Video { content: video, views: 0, likes: 0, dislikes: 0 });
        match self.free.pop() {
            Some(Reverse(id)) => {
                self.slots[id as usize] = held;
                id
            }
            None => {
                self.slots.push(held);
                self.slots.len() as i64 - 1
            }
        }
    }

    fn remove(&mut self, id: i64) {
        if id < self.slots.len() as i64 && self.slots[id as usize].is_some() {
            self.slots[id as usize] = None;
            self.free.push(Reverse(id));
        }
    }

    fn watch(&mut self, id: i64, start: i64, end: i64) -> String {
        if id >= self.slots.len() as i64 {
            return "-1".to_string();
        }
        match &mut self.slots[id as usize] {
            Some(video) => {
                video.views += 1;
                let last = end.min(video.content.len() as i64 - 1);
                video.content[start as usize..last as usize + 1].to_string()
            }
            None => "-1".to_string(),
        }
    }

    fn like(&mut self, id: i64) {
        if let Some(Some(video)) = self.slots.get_mut(id as usize) {
            video.likes += 1;
        }
    }

    fn dislike(&mut self, id: i64) {
        if let Some(Some(video)) = self.slots.get_mut(id as usize) {
            video.dislikes += 1;
        }
    }

    fn get_likes_and_dislikes(&self, id: i64) -> Vec<i64> {
        match self.slots.get(id as usize) {
            Some(Some(video)) => vec![video.likes, video.dislikes],
            _ => vec![-1],
        }
    }

    fn get_views(&self, id: i64) -> i64 {
        match self.slots.get(id as usize) {
            Some(Some(video)) => video.views,
            _ => -1,
        }
    }
}

fn show(v: &[i64]) -> String {
    format!("[{}]", v.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", "))
}

fn run(calls: &[(i64, Vec<i64>, String)]) -> Vec<String> {
    let mut platform = Platform::new();
    let mut answers = Vec::new();
    for (kind, args, text) in calls {
        match kind {
            0 => answers.push(platform.upload(text.clone()).to_string()),
            1 => platform.remove(args[0]),
            2 => answers.push(platform.watch(args[0], args[1], args[2])),
            3 => platform.like(args[0]),
            4 => platform.dislike(args[0]),
            5 => answers.push(show(&platform.get_likes_and_dislikes(args[0]))),
            _ => answers.push(platform.get_views(args[0]).to_string()),
        }
    }
    answers
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn calls_of(count: i64, longest: i64, seed: &mut i64) -> Vec<(i64, Vec<i64>, String)> {
    let mut calls = Vec::new();
    let mut uploads = 0;
    for _ in 0..count {
        let pick = next_random(seed) % 10;
        let id = next_random(seed) % (uploads + 2);
        if pick < 3 {
            let length = next_random(seed) % (longest - 2) + 3;
            let digits: String = (0..length).map(|_| next_random(seed).rem_euclid(10).to_string()).collect();
            calls.push((0, Vec::new(), digits));
            uploads += 1;
        } else if pick == 3 {
            calls.push((1, vec![id], String::new()));
        } else if pick < 6 {
            let start = next_random(seed) % 3;
            let end = start + next_random(seed) % 8 + 1;
            calls.push((2, vec![id, start, end], String::new()));
        } else {
            calls.push((pick - 3, vec![id], String::new()));
        }
    }
    calls
}

fn tally(answers: &[String], check: i64) -> i64 {
    let mut c = check;
    for answer in answers {
        for b in answer.bytes() {
            c = (c * 131 + b as i64) % 1000000007;
        }
        c = (c * 131 + 1) % 1000000007;
    }
    c
}

fn main() {
    let mut seed = 2254i64;
    let mut answered = 0;
    let mut check = 0;
    for _ in 0..120 {
        let answers = run(&calls_of(25000, 8, &mut seed));
        answered += answers.len();
        check = tally(&answers, check);
    }
    println!("120 platforms of 25000 calls: {} answers, checksum {}", answered, check);
}
