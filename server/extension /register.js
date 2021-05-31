//register new user 
submit = document.getElementById("submit")
submit.addEventListener('click', function(e){
    fullname = document.getElementById("fullname")
    email = document.getElementById("email")
    password = document.getElementById("password")
    debug = document.getElementById("debug")
    if(fullname.value != "" && email.value != "" && password.value != ""){
      
      const Http = new XMLHttpRequest()
      Http.open("post", 'http://127.0.0.1:5000/register')
      Http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      data = JSON.stringify({
        fullname:fullname.value,
        email : email.value , 
        password : password.value
      })

      Http.send(data)
      debug.innerHTML = "Done"
    }else{
      
      debug.innerHTML = "Error"

    }

})