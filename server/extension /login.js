

var login = document.getElementById("login")
login.addEventListener('click', function(e){
	alert(1)
	let email = document.getElementById('email')
	let password = document.getElementById('password')
	if(email.value != '' && password.value != ''){
		alert(1)
		const Http = new XMLHttpRequest()
		Http.onreadystatechange = function(){
			console.log('fdf')
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