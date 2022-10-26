function signupRegister(){   

    // register에 POST 방식으로 회원 생성요청 (ajax사용불가)
    const data = {
        "user_id"    : document.getElementById('signup_id'   ).value,
        "user_pw1"   : document.getElementById('signup_pw1'  ).value,
        "user_pw2"   : document.getElementById('signup_pw2'  ).value,
        "user_name"  : document.getElementById('signup_name' ).value,
        "user_room"  : document.getElementById('signup_room' ).value,
        "user_phone" : document.getElementById('signup_phone').value
    }
    console.log(JSON.stringify(data))
    // 회원가입 data POST

    // })
    
    fetch('/signup/register',{
        method : 'POST',
        body : JSON.stringify(data),
        headers : {
            "Content-Type" : "application/json"
        },  
    })

        
    .then(()=>{
        window.location.href = '/signup'; // 새로고침
    })
    .catch((error) => {
        console.log(error)
    });
    
}