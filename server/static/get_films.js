let container = document.getElementById('film_container')

fetch("http://localhost:3001/").then((Response) => {
        
        return Response.json()
    })
    .then((data) => {
        console.log(data)
        data.forEach((e) => {
            console.log(e)
           
            container.innerHTML +=`<img id="img_film" class="poster" src=" `+ e + `" alt=" ">`
          })


//        for (let index = 0; index < data.length; index++) {
//            data[index] = 'q=' + data[index] + '&';
//
//        }
//        console.log(data.join(''));
//
//        fetch("http://localhost:80/list/?" + data.join('')).then((Response) => {
//                return Response.json()
//            }).then((data) => {
//                console.log(data);
//                data.forEach(element => {
//                    container.innerHTML +='<img id="img_film" class="poster" src="' + element["url"] + '" alt=" ">'
//
//                });
//            });
    })