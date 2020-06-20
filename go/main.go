package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

func main() {
	rand.Seed(55)
	fmt.Println("Random number is:", rand.Intn(100))

	fmt.Println("Now time is:", time.Now())

	fmt.Println("sqrt value is:", math.Sqrt(2))
}
