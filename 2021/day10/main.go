package main

import (
	"bufio"
	"log"
	"os"
	"sort"
)

type (
	Stack struct {
		top    *node
		length int
	}
	node struct {
		value interface{}
		prev  *node
	}
)

func NewStack() *Stack {
	return &Stack{nil, 0}
}

func (stack *Stack) Len() int {
	return stack.length
}

func (stack *Stack) Peek() interface{} {
	if stack.length == 0 {
		return nil
	}
	return stack.top.value
}

func (stack *Stack) Pop() interface{} {
	if stack.length == 0 {
		return nil
	}

	n := stack.top
	stack.top = n.prev
	stack.length--
	return n.value
}

func (stack *Stack) Push(value interface{}) {
	n := &node{value, stack.top}
	stack.top = n
	stack.length++
}

func main() {

	inFile, err := os.Open("part1.txt")
	if err != nil {
		log.Fatal("cannot open input")
	} else {

		scanner := bufio.NewScanner(inFile)
		scanner.Split(bufio.ScanLines)

		lineNumber := 0
		partOneScore := 0
		partTwoScores := []int{}
		for scanner.Scan() {
			s := NewStack()
			line := scanner.Text()
			lineSyntaxPoints := 0
			for _, x := range line {
				switch x {
				case '(':
					fallthrough
				case '[':
					fallthrough
				case '{':
					fallthrough
				case '<':
					s.Push(x)
				case ')':
					if s.Peek() != '(' {
						lineSyntaxPoints = 3
					} else {
						s.Pop()
					}
				case ']':
					if s.Peek() != '[' {
						lineSyntaxPoints = 57
					} else {
						s.Pop()
					}
				case '}':
					if s.Peek() != '{' {
						lineSyntaxPoints = 1197
					} else {
						s.Pop()
					}
				case '>':
					if s.Peek() != '<' {
						lineSyntaxPoints = 25137
					} else {
						s.Pop()
					}
				}
				if lineSyntaxPoints > 0 {
					partOneScore += lineSyntaxPoints
					break
				}
			}
			lineNumber++
			if lineSyntaxPoints == 0 && s.Len() > 0 {
				lineCompletionPoints := 0
				for s.Len() > 0 {
					x := s.Pop()
					switch x {
					case '(':
						lineCompletionPoints = lineCompletionPoints*5 + 1
					case '[':
						lineCompletionPoints = lineCompletionPoints*5 + 2
					case '{':
						lineCompletionPoints = lineCompletionPoints*5 + 3
					case '<':
						lineCompletionPoints = lineCompletionPoints*5 + 4
					}
				}
				if lineCompletionPoints > 0 {
					partTwoScores = append(partTwoScores, lineCompletionPoints)
				}

			}
		}
		inFile.Close()

		log.Println(partOneScore)
		sort.Ints(sort.IntSlice(partTwoScores))
		log.Println(partTwoScores[(len(partTwoScores)-1)/2])
	}
}
