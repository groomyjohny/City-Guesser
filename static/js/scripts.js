//make a GET HTTP request and put response into an element. WARNING: element's HTML will be overriden by the result!
async function request(address, responseSelector, method = 'GET', paramsFunc = function(){return ''})
{
    let responseElement = document.querySelector(responseSelector);
    let dict = {};
    dict.method = method;
    if (method != 'GET') dict.body = paramsFunc(); 
    let response = await fetch(address, dict);
    if (response.ok)
    {
        responseElement.innerHTML = await response.text();
    } 
    else
    {
        let arr = [
            "Произошла ошибка при выполнении запроса.",
            method + " " + address,
            "Код ошибки:" + response.status,
        ];
        responseElement.innerHTML = arr.join('<p>');
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

function submitGuess(n)
{
    let form = document.getElementById("answer-form");
    console.log(form);

    let paramsFunc = function(){return new FormData(form);};
    request("/answer/"+ n, "#game-container", "POST", paramsFunc);  
    return false;
}