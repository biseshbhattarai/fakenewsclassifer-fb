//view reported news as fake
const n = document.getElementById("news")
const Http = new XMLHttpRequest()
let da
Http.onreadystatechange = function(){
	if(this.readyState == 4 && this.status==200){
		let data = JSON.parse(Http.responseText)
		data.forEach(i => {
			let tag = document.createElement("li")
			var text = document.createTextNode(i.title);
			tag.style.cssText = 'color:red'
			tag.append(text)
			n.append(tag)
		})
	
	}
}
Http.open("get", 'http://127.0.0.1:5000/get_report')
Http.send()
