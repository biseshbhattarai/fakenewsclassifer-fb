
function fetch(){
const Http = new XMLHttpRequest()
Http.onreadystatechange = function(){
	if(this.readyState == 4 && this.status == 200){
		if(Http.responseText == 'guest'){
			alert("Please login to report")
		}
	}

}
Http.open("get", 'http://127.0.0.1:5000/current_user', true)
Http.send()

}
fetch()

var login = document.getElementById("report")
login.addEventListener('click', function(e){
	alert(1)
	let news = document.getElementById('news')
	alert(news.value)
	
	if(news.value != ''){
		
		const Http = new XMLHttpRequest()
		Http.onreadystatechange = function(){
			console.log('fdf')
		}
		Http.open("post", 'http://127.0.0.1:5000/report')
		Http.setRequestHeader("Content-type", "application/json;charset=UTF-8")
		let data = JSON.stringify({
			news : news.value
		})
		Http.send(data)
	}
})

