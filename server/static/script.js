btn = document.getElementById('gen_btn')
let film_name = document.getElementById('name_film')
let year_film = document.getElementById('year_film')
let genre_film = document.getElementById('genre_film')
let direction_film = document.getElementById('direction_film')
let img_film = document.getElementById('img_film')

let current = 0

btn.onclick = async function() {

    fetch("http://localhost:80/").then((Response) => {
        return Response.json()
    }).then((data) => {

        img_film.src = data[0].url;
        url= data[0].url;
        localStorage.setItem('url', url);
    })
}


add = document.getElementById('add')

add.onclick = async function(){
    let t = localStorage.getItem('url')
    let urlf = {url : t}

    fetch("http://localhost:3001", {
    method: "POST",
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
    body: JSON.stringify(urlf)
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
}
