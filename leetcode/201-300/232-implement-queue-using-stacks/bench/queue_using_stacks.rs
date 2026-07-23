struct MyQueue {
    inbox: Vec<i64>,
    outbox: Vec<i64>,
}

impl MyQueue {
    fn new() -> MyQueue {
        MyQueue {
            inbox: Vec::new(),
            outbox: Vec::new(),
        }
    }

    fn push(&mut self, x: i64) {
        self.inbox.push(x);
    }

    fn refill(&mut self) {
        if self.outbox.is_empty() {
            while let Some(v) = self.inbox.pop() {
                self.outbox.push(v);
            }
        }
    }

    fn pop(&mut self) -> i64 {
        self.refill();
        self.outbox.pop().unwrap_or(-1)
    }

    fn peek(&mut self) -> i64 {
        self.refill();
        self.outbox[self.outbox.len() - 1]
    }

    fn empty(&self) -> bool {
        self.inbox.is_empty() && self.outbox.is_empty()
    }
}

fn main() {
    let n: i64 = 75000000;
    let cap: i64 = 4096;
    let mask: i64 = 1048575;

    let mut q = MyQueue::new();
    let mut sz: i64 = 0;
    let mut sink: i64 = 0;
    let mut state: i64 = 12345;

    for _ in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        if q.empty() || (state % 2 == 0 && sz < cap) {
            q.push(state & mask);
            sz += 1;
        } else if state % 4 == 0 {
            sink += q.peek();
        } else {
            sink += q.pop();
            sz -= 1;
        }
    }
    println!("{}", sink);
}
