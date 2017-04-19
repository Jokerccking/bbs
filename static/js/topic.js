var timeConvert = function() {
    var ele = e("#topic-ct")
    timestamp = int(ele.innerHTML)
    t = new Date(timestamp * 1000)
    return t.toLocalTimeString()
}

var markString = function() {
    var ele = e("#markdown-text");
    b = ele.innerHTML;
    ele.innerHTML = marked(b)
}

var __main = function() {
    timeConvert();
    markString()
}

$(document).ready(function() {
    __main();
})