if (localStorage.getItem("userId")) {
  document.getElementById("nombre_user").innerHTML =
    localStorage.getItem("userNombre");
  fetchReseñas();
} else {
  window.location.replace("http://localhost:8000/login");
}

function logout() {
  localStorage.clear();
  window.location.replace("http://localhost:8000/login");
}

function response_received(response) {
  return response.json();
}

async function parse_data(content) {
  const container = document
    .getElementById("reseñas-table")
    .getElementsByTagName("tbody")[0];
  console.log(container);
  for (let index = 0; index < content.length; index++) {
    const tr = document.createElement("tr");
    const pelicula_data = await fetch(
      "http://localhost:5000/peliculas/" + content[index].id_pelicula
    )
      .then(response_received)
      .catch(request_error);

    const imagenTd = document.createElement("td");
    const nombreTd = document.createElement("td");
    const añoEstrenoTd = document.createElement("td");
    const generoTd = document.createElement("td");
    const directorTd = document.createElement("td");
    const puntajeTd = document.createElement("td");
    const reseñaTd = document.createElement("td");
    const accionTd = document.createElement("td");
    const imagenPelicula = new Image();
    imagenPelicula.src = pelicula_data.imagen;
    imagenTd.append(imagenPelicula);
    nombreTd.innerHTML = pelicula_data.nombre;
    añoEstrenoTd.innerHTML = pelicula_data.año_estreno;
    generoTd.innerHTML = pelicula_data.genero;
    directorTd.innerHTML = pelicula_data.director;
    puntajeTd.innerHTML = content[index].puntaje;
    reseñaTd.innerHTML = content[index].reseña_corta;
    accionTd.innerHTML =
      `
        <div>
          <i class="fa fa-edit" onclick='window.location.replace("http://127.0.0.1:5500/frontend/reseña/?id=` +
      content[index].id +
      `")'></i>
          <i class="fa fa-trash" onclick="deleteReseña(` +
      content[index].id +
      `)"></i>
        </div>`;

    tr.append(imagenTd);
    tr.append(nombreTd);
    tr.append(añoEstrenoTd);
    tr.append(generoTd);
    tr.append(directorTd);
    tr.append(puntajeTd);
    tr.append(reseñaTd);
    tr.append(accionTd);

    console.log(pelicula_data);
    container.append(tr);
  }
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
}

function deleteReseña(idReseña) {
  fetch("http://localhost:5000/reseñas/" + idReseña, {
    method: "DELETE",
    mode: "cors",
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  })
    .then((Result) => Result.json())
    .then((data) => {
      document
        .getElementById("reseñas-table")
        .getElementsByTagName("tbody")[0].innerHTML = "";
      fetchReseñas();
    })
    .catch((errorMsg) => {
      console.log(errorMsg);
    });
}

function fetchReseñas() {
  fetch("http://localhost:5000/reseñas")
    .then(response_received)
    .then(parse_data)
    .catch(request_error);
}
