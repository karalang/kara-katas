// LeetCode #1117: Building H2O -- the bench in Rust: OS threads in a
// `thread::scope`; a hydrogen hands a one-shot `sync_channel` to the
// oxygens and waits on it, and an oxygen takes the bonding lock,
// receives two hydrogens, releases itself, sends each a channel to say
// it is out on, and waits for both. The hydrogens' receiving end is
// behind a `Mutex` since `Receiver` is not `Sync`.

use std::sync::mpsc::{sync_channel, Receiver, SyncSender};
use std::sync::Mutex;
use std::thread;

type Out = SyncSender<()>;

struct H2O {
    bonding: Mutex<()>,
    hydrogens_tx: Mutex<SyncSender<SyncSender<Out>>>,
    hydrogens_rx: Mutex<Receiver<SyncSender<Out>>>,
}

impl H2O {
    fn new() -> Self {
        let (tx, rx) = sync_channel(2);
        H2O { bonding: Mutex::new(()), hydrogens_tx: Mutex::new(tx), hydrogens_rx: Mutex::new(rx) }
    }

    fn hydrogen(&self, release_hydrogen: impl Fn()) {
        let (go_tx, go_rx) = sync_channel(1);
        let tx = self.hydrogens_tx.lock().unwrap().clone();
        tx.send(go_tx).unwrap();
        let out = go_rx.recv().unwrap();
        release_hydrogen();
        out.send(()).unwrap();
    }

    fn oxygen(&self, release_oxygen: impl Fn()) {
        let _bond = self.bonding.lock().unwrap();
        let gos: Vec<SyncSender<Out>> = {
            let rx = self.hydrogens_rx.lock().unwrap();
            (0..2).map(|_| rx.recv().unwrap()).collect()
        };
        release_oxygen();
        let (out_tx, out_rx) = sync_channel(2);
        for go in &gos {
            go.send(out_tx.clone()).unwrap();
        }
        for _ in 0..2 {
            out_rx.recv().unwrap();
        }
    }
}

fn run(water: &[u8]) -> String {
    let log = Mutex::new(String::new());
    let h2o = H2O::new();
    thread::scope(|s| {
        for &c in water {
            let (h2o, log) = (&h2o, &log);
            if c == b'H' {
                s.spawn(move || h2o.hydrogen(|| log.lock().unwrap().push('H')));
            } else {
                s.spawn(move || h2o.oxygen(|| log.lock().unwrap().push('O')));
            }
        }
    });
    log.into_inner().unwrap()
}

fn main() {
    let mut seed: i64 = 1117;
    let mut whole = 0;
    let mut check: i64 = 0;
    for r in 0..500i64 {
        let mut water: Vec<u8> = Vec::new();
        for _ in 0..20 {
            water.extend_from_slice(b"OHH");
        }
        for j in 0..60usize {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let k = j + (seed / 65536) as usize % (60 - j);
            water.swap(j, k);
        }
        let out = run(&water);
        let b = out.as_bytes();
        let molecules = (0..b.len() / 3)
            .filter(|&i| b[3 * i..3 * i + 3].iter().filter(|&&c| c == b'H').count() == 2)
            .count();
        if molecules == 20 {
            whole += 1;
        }
        check = (check * 31 + out.len() as i64 + r) % 1000000007;
    }
    println!("500 runs of 20 molecules: {} with every molecule whole, checksum {}", whole, check);
}
