

function get_news(){
	news = document.getElementById("news")
	let dup_news = []
	newss = localStorage.getItem("news")

	const Http = new XMLHttpRequest()
	Http.onreadystatechange = function(){
		if(this.readyState == 4 && this.status==200){
			data = JSON.parse(Http.responseText)
			console.log(dup_news)
			data.forEach(i => {
				let similar = parseFloat(i.similarlity)
				if (similar <= 10 ){
						console.log(i.news_title)
						var tag = document.createElement("li")
						var small = document.createElement("small")
						var br = document.createElement("br")
						tag.style.cssText = 'color:red'
						var text = document.createTextNode(i.news_title);
						var text2 = document.createTextNode(i.similarlity)
						tag.appendChild(text)
						small.appendChild(text2)
						tag.appendChild(small)
						tag.appendChild(br)
						news.appendChild(tag)
					}else if(similar >= 20){
						var tag = document.createElement("li")
						tag.style.cssText = 'color:green'
						var text = document.createTextNode(i.news_title);
						tag.appendChild(text)
						news.appendChild(tag)
					}
			
		})

		}
	}

	Http.open("get", 'http://127.0.0.1:5000/get_news', true)
	Http.send()

}



function fetch(){
const Http = new XMLHttpRequest()
Http.onreadystatechange = function(){
	if(this.readyState == 4 && this.status == 200){
		document.getElementById("current_user").innerHTML = Http.responseText;
	}

}
Http.open("get", 'http://127.0.0.1:5000/current_user', true)
Http.send()

}

fetch()
// get_news()

f = document.getElementById("fetch_news")
f.addEventListener('click', function(e){
	  chrome.tabs.query({
        active: true,        
        currentWindow: true
    }, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id, {
                code: "[...document.querySelectorAll('div.stjgntxs.ni8dbmo4 > div > a > div > div > div.rq0escxv.l9j0dhe7.du4w35lb.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.g5gj957u.p8fzw8mz.pcp91wgn > div.enqfppq2.muag1w35.ni8dbmo4.stjgntxs.e5nlhep0.ecm0bbzt.rq0escxv.a5q79mjw.r9c01rrb > div > div:nth-child(1) > span > span > span')].map(n=>n.innerHTML)"
            },

            function(results) {
                console.log('results', results)
                const Http = new XMLHttpRequest();
                Http.open("post", 'http://127.0.0.1:5000/news')
                Http.setRequestHeader("Content-type", "application/json;charset=UTF-8");
                data = JSON.stringify({
                  lines : results[0]
                })
                Http.send(data)
                


                
            }
        )
    })
	get_news()  

})

function fetch_news(){

	  chrome.tabs.query({
        active: true,        
        currentWindow: true
    }, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id, {
                code: "[...document.querySelectorAll('div.stjgntxs.ni8dbmo4 > div > a > div > div > div.rq0escxv.l9j0dhe7.du4w35lb.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.g5gj957u.p8fzw8mz.pcp91wgn > div.enqfppq2.muag1w35.ni8dbmo4.stjgntxs.e5nlhep0.ecm0bbzt.rq0escxv.a5q79mjw.r9c01rrb > div > div:nth-child(1) > span > span > span')].map(n=>n.innerHTML)"
            },

            function(results) {
                // console.log('results', results)
                const Http = new XMLHttpRequest();
                Http.open("post", 'http://127.0.0.1:5000/news')
                Http.setRequestHeader("Content-type", "application/json;charset=UTF-8");
                data = JSON.stringify({
                  lines : results[0]
                })
                Http.send(data)
               


                
            }
        )
    })

	  get_news()

}



let detect = document.getElementById("detect")

detect.addEventListener('click', function(e){
	let newss = document.getElementById("direct_news")
	alert(newss.value)

	const Http = new XMLHttpRequest();
    Http.open("post", 'http://127.0.0.1:5000/direct_detect')
    Http.setRequestHeader("Content-type", "application/json;charset=UTF-8");
    data = JSON.stringify({
        lines : newss.value
    })
    Http.send(data)
})


fetch_news()