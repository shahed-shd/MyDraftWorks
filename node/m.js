module.exports.fn = f

function f(x) {
    console.log(x);
}

module.exports.msg = 'I am msg 1'

module.exports.modMsg = modifyMsg

function modifyMsg(newMsg) {
    module.exports.msg1 = newMsg
}
