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
    })
}


add = document.getElementById('add')

add.onclick = async function(){

    fetch("http://localhost:3001/?id=" + current.toString(), {
    method: "POST"
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
}
