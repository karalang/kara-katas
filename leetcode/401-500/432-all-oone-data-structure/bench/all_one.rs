// Benchmark for #432: mirror of all_one.kara (a list of count buckets).
// A Kāra `shared struct` is reference counted, so a bucket here is an
// Rc<RefCell<Bucket>> with a strong `next` and a Weak `prev`, as in the
// Kāra program; std's HashMap and HashSet hash with SipHash-1-3 under a
// random key, as Kāra's Map and Set do.
use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::{Rc, Weak};

struct Bucket {
    count: i64,
    keys: HashSet<String>,
    prev: Weak<RefCell<Bucket>>,
    next: Option<Rc<RefCell<Bucket>>>,
}

type B = Rc<RefCell<Bucket>>;

fn bucket(count: i64) -> B {
    Rc::new(RefCell::new(Bucket { count, keys: HashSet::new(), prev: Weak::new(), next: None }))
}

fn link_after(at: &B, count: i64) -> B {
    let b = bucket(count);
    let after = at.borrow().next.clone().expect("the tail sentinel ends the list");
    b.borrow_mut().next = Some(after.clone());
    after.borrow_mut().prev = Rc::downgrade(&b);
    at.borrow_mut().next = Some(b.clone());
    b.borrow_mut().prev = Rc::downgrade(at);
    b
}

fn unlink(b: &B) {
    let before = b.borrow().prev.upgrade().expect("the head sentinel starts the list");
    let after = b.borrow().next.clone().expect("the tail sentinel ends the list");
    after.borrow_mut().prev = Rc::downgrade(&before);
    before.borrow_mut().next = Some(after);
}

fn any_key(b: &B) -> String {
    match b.borrow().keys.iter().next() {
        Some(k) => k.clone(),
        None => String::new(),
    }
}

struct AllOne {
    head: B,
    tail: B,
    bucket_of: HashMap<String, B>,
}

impl AllOne {
    fn new() -> AllOne {
        let head = bucket(0);
        let tail = bucket(-1);
        head.borrow_mut().next = Some(tail.clone());
        tail.borrow_mut().prev = Rc::downgrade(&head);
        AllOne { head, tail, bucket_of: HashMap::new() }
    }

    fn inc(&mut self, key: &str) {
        let cur = match self.bucket_of.get(key) {
            Some(b) => b.clone(),
            None => self.head.clone(),
        };
        let count = cur.borrow().count;
        let after = cur.borrow().next.clone().expect("the tail sentinel ends the list");
        let up = if after.borrow().count == count + 1 { after } else { link_after(&cur, count + 1) };
        up.borrow_mut().keys.insert(key.to_string());
        self.bucket_of.insert(key.to_string(), up);
        if count > 0 {
            cur.borrow_mut().keys.remove(key);
            if cur.borrow().keys.is_empty() {
                unlink(&cur);
            }
        }
    }

    fn dec(&mut self, key: &str) {
        let cur = self.bucket_of.get(key).expect("dec of a key that is present").clone();
        let count = cur.borrow().count;
        if count == 1 {
            self.bucket_of.remove(key);
        } else {
            let before = cur.borrow().prev.upgrade().expect("the head sentinel starts the list");
            let down = if before.borrow().count == count - 1 { before } else { link_after(&before, count - 1) };
            down.borrow_mut().keys.insert(key.to_string());
            self.bucket_of.insert(key.to_string(), down);
        }
        cur.borrow_mut().keys.remove(key);
        if cur.borrow().keys.is_empty() {
            unlink(&cur);
        }
    }

    fn get_max_key(&self) -> String {
        any_key(&self.tail.borrow().prev.upgrade().expect("the head sentinel starts the list"))
    }

    fn get_min_key(&self) -> String {
        any_key(&self.head.borrow().next.clone().expect("the tail sentinel ends the list"))
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn key_id(key: &str) -> i64 {
    if key.is_empty() {
        return -1;
    }
    let mut id = 0;
    for b in key.bytes() {
        if b != b'k' {
            id = id * 10 + (b - b'0') as i64;
        }
    }
    id
}

fn main() {
    let keys: i64 = 10000;
    let operations: i64 = std::env::args().nth(1).map_or(2000000, |a| a.parse().unwrap());
    let mut seed: i64 = 432;
    let mut ds = AllOne::new();
    let mut count = vec![0i64; keys as usize];
    let mut queries = 0;
    let mut checksum: i64 = 0;
    for _ in 0..operations {
        let roll = next_random(&mut seed) % 10;
        let hi = next_random(&mut seed);
        let id = ((hi * 32768 + next_random(&mut seed)) % keys) as usize;
        if roll < 2 {
            let answer = if roll == 0 { ds.get_max_key() } else { ds.get_min_key() };
            let a = key_id(&answer);
            let c = if a < 0 { 0 } else { count[a as usize] };
            queries += 1;
            checksum = (checksum * 31 + c + 1) % 1000000007;
        } else if roll < 5 && count[id] > 0 {
            ds.dec(&format!("k{}", id));
            count[id] -= 1;
        } else {
            ds.inc(&format!("k{}", id));
            count[id] += 1;
        }
    }
    println!("{} operations on {} keys: {} queries, checksum {}", operations, keys, queries, checksum);
}
