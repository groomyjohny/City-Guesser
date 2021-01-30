//make a GET HTTP request and put response into an element. WARNING: element's HTML will be overriden by the result!
function request(address, responseSelector)
{
    let responseElement = document.querySelector(responseSelector);
    let req = new XMLHttpRequest();
    req.open('GET', address)
    req.send();
    req.onload = function() {
        if (req.status == 200)
        {
            responseElement.innerHTML = req.response;
        }
    }
}
function loadSlide(n)
{
    request('/slide/'+n,"#game-container")
}
function getHint(n)
{
    request('/hint/'+n,"#game-container")
}
window.addEventListener("load", function() {
    loadSlide(0);
});