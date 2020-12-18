use peg;
use std::fs::File;
use std::io::{self, BufRead, Error};

// https://github.com/kevinmehall/rust-peg/blob/master/tests/run-pass/arithmetic_infix.rs

peg::parser!( grammar aoc_eighteen_a() for str {
    rule number() -> i64
        = n:$(['0'..='9']+) { n.parse().unwrap() }

    rule _()
        = " "?

    pub rule parse() -> i64 = precedence!{
        x:(@) _ "+" _ y:@ { x + y }
        x:(@) _ "*" _ y:@ { x * y }
        --
        "(" _ v:parse() _ ")" { v }
        n:number() {n}
    }
});

peg::parser!( grammar aoc_eighteen_b() for str {
    rule number() -> i64
        = n:$(['0'..='9']+) { n.parse().unwrap() }

    rule _()
        = " "?

    pub rule parse() -> i64 = precedence!{
        x:(@) _ "*" _ y:@ { x * y }
        --
        x:(@) _ "+" _ y:@ { x + y }
        --
        "(" _ v:parse() _ ")" { v }
        n:number() {n}
    }
});

const AOCDEBUG: bool = false;

type AOCResult = std::result::Result<(), Error>;

struct AOCProcessor {
    source: String,
    result_a: i64,
    result_b: i64,
}

impl AOCProcessor {
    pub fn new(source: String) -> Self {
        AOCProcessor {
            source: source,
            result_a: 0,
            result_b: 0,
        }
    }

    pub fn process(&mut self) -> AOCResult {
        self.initialize();
        let _ = match File::open(&self.source) {
            Ok(file) => {
                let mut lineno: i32 = 0;
                for line in io::BufReader::new(file).lines() {
                    if let Ok(line) = line {
                        self.process_line(&line[..], lineno);
                        lineno += 1;
                    }
                }
            }
            Err(error) => return Err(error),
        };
        self.finalize();
        Ok(())
    }

    fn initialize(&mut self) {}

    fn finalize(&mut self) {
        println!("result_a:{}", self.result_a);
        println!("result_b:{}", self.result_b);
    }

    fn process_line(&mut self, line: &str, _lineno: i32) {
        if line.len() > 0 {
            let rval_a = match aoc_eighteen_a::parse(line) {
                Ok(rval) => rval,
                Err(err) => {
                    panic!("{}", err);
                }
            };
            self.result_a += rval_a;

            let rval_b = match aoc_eighteen_b::parse(line) {
                Ok(rval) => rval,
                Err(err) => {
                    panic!("{}", err);
                }
            };
            self.result_b += rval_b;
        }
    }
}

fn main() {
    let mut processor = AOCProcessor::new(String::from("input.txt"));
    match processor.process() {
        Ok(()) => {
            println!("DONE");
        }
        Err(error) => {
            panic!("{:#?}", error);
        }
    }
}
