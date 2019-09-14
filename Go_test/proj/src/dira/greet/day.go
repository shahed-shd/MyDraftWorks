package greet

import (
	"fmt"
)

func init() {
	fmt.Println("day.go ==> init()")
}

var morning = "Good Morning"
var Morning = "Hey, " + morning
