function fn1() {
    function prod(aaa, bbb) {
        var k = 5;
        return aaa * bbb + 5;
    }

    var x = 123;
    document.getElementById('demo1').innerHTML = x;
    document.getElementById('demo2').innerHTML = prod(3, 4);
}