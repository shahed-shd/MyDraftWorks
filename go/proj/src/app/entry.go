package main

import (
	"dira/greet"
	"fmt"
)

func init() {
	fmt.Println("entry.go ==> init() [1]")
}

func init() {
	fmt.Println("entry.go ==> init() [2]")
}

func main() {
	fmt.Println("Hello dear")
	fmt.Println(greet.Morning)
}
