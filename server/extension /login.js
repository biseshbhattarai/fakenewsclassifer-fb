
//login new user 
var login = document.getElementById("login")
login.addEventListener('click', function(e){
	
	let email = document.getElementById('email')
	let password = document.getElementById('password')
	if(email.value != '' && password.value != ''){
		
		const Http = new XMLHttpRequest()
		Http.onreadystatechange = function(){

			if(this.readyState == 4 && this.status == 200){
				if(Http.responseText == 0){
					alert("Username or password incorrect.")
				}
				alert("Login success . Head over to profile")
				
		}
		}
		Http.open("post", 'http://127.0.0.1:5000/login')
		Http.setRequestHeader("Content-type", "application/json;charset=UTF-8")
		data = JSON.stringify({
			email : email.value , 
			password : password.value 
		})
		Http.send(data)
	}
})