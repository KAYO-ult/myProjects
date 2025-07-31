let a = 10
// a = 50
const b = 20
// b = 0
console.log(a)
console.log(b)
// console.log(a + b)

if (a > b) {
  console.log("a is greater than b")
}
else {
    console.log("b is greater than a")
}

// for (let i = 0; i <= 5; i++) {
//   console.log(i)
// }

// while (a < 10) {
//   console.log(a)
//   a++
// }

function abc() {
  console.log("This is a function")
}   

function add(a, b) {
  console.log("The sum is: " + (a + b))
//   return a + b
}

abc()
add(10, 20)

