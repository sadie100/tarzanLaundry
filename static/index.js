window.addEventListener('load', function () {
    fetch('/memo')
        // .then((response) => response.json())
        
})

const checkMyCookie = function() {
    fetch('/get_cookie')
    .then((response) => response.json())
}

const  chechk = function (a,b) {
    console.log(a,b)
}