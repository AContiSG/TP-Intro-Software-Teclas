let params = new URLSearchParams(document.location.search);
let id = params.get("id");
console.log(id);
if (!localStorage.getItem("userId")) {
  window.location.replace("http://localhost:8000/login");
}
loadMoviesOptions();
let base64String = "";

function fetchReseñas() {
  fetch("http://localhost:5000/reseñas/" + id)
    .then(response_received)
    .then(loadReseñaData)
    .catch(request_error);
}

function loadReseñaData(content) {
  document.getElementById("pelicula-select").value = content.id_pelicula;
  document.getElementById("puntaje").value = content.puntaje;
  document.getElementById("reseña_corta").value = content.reseña_corta;
  document.getElementById("button_submit").value = "modificar";
}

function loadFormMovie(activeForm) {
  const selectPelicula = document.getElementById("pelicula-select");
  const container = document.getElementById("form_nueva_pelicula");
  if (activeForm) {
    selectPelicula.selectedIndex = 0;
    container.innerHTML = `
          <h2>Nueva Pelicula</h2>
          <form class="form" onsubmit="sendPelicula(event)">
            <div class="contenedor-input">
              <label>
                nombre<span class="req">*</span>
              </label>
              <input name="nombre" type="text">
            </div>
            <div class="contenedor-input">
              <label>
                director<span class="req">*</span>
              </label>
              <input name="director" type="text">
            </div>
            <div class="contenedor-input">
              <label>
                año de estreno<span class="req">*</span>
              </label>
              <input name="año_estreno" type="number">
            </div>
            <div class="contenedor-input">
              <label>
                genero<span class="req">*</span>
              </label>
              <input name="genero" type="text">
            </div>
            
            <div class="contenedor-input">
              <label>
                imagen<span class="req">*</span>
              </label>
              <input type="file" accept="image/*" name="imagen" onchange="imageUploaded()">
            </div>
            <div class="contenedor-buttons">
              <input class="button" type="submit" value="Cargar pelicula">
              <input class="button" type="button" value="Cancel"  onClick="loadFormMovie(false)">
            </div>
          </form>`;
  } else {
    container.innerHTML = "";
  }
}

function resizeImage(base64Str, maxWidth = 400, maxHeight = 350) {
  return new Promise((resolve) => {
    let img = new Image();
    img.src = base64Str;
    img.onload = () => {
      let canvas = document.createElement("canvas");
      const MAX_WIDTH = maxWidth;
      const MAX_HEIGHT = maxHeight;
      let width = img.width;
      let height = img.height;

      if (width > height) {
        if (width > MAX_WIDTH) {
          height *= MAX_WIDTH / width;
          width = MAX_WIDTH;
        }
      } else {
        if (height > MAX_HEIGHT) {
          width *= MAX_HEIGHT / height;
          height = MAX_HEIGHT;
        }
      }
      canvas.width = width;
      canvas.height = height;
      let ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, width, height);
      resolve(canvas.toDataURL());
    };
  });
}

function imageUploaded() {
  let file = document.querySelector("input[type=file]")["files"][0];

  let reader = new FileReader();

  reader.onload = function () {
    resizeImage(reader.result, 100, 100).then((result) => {
      base64String = result;
    });
  };
  reader.readAsDataURL(file);
}

function response_received(response) {
  return response.json();
}

function parse_data(content) {
  const container = document.getElementById("pelicula-select");
  for (let index = 0; index < content.length; index++) {
    console.log(content[index]);
    const item = document.createElement("option");
    item.setAttribute("value", content[index].id);
    item.innerHTML =
      content[index].año_estreno +
      " - " +
      content[index].nombre +
      " - " +
      content[index].director;

    container.append(item);
  }
}

function request_error(error) {
  console.log("ERROR");
  console.log(error);
}

function loadMoviesOptions() {
  fetch("http://localhost:5000/peliculas")
    .then(response_received)
    .then(parse_data)
    .then(id && fetchReseñas())
    .catch(request_error);
}

const sendPelicula = (e) => {
  console.log(base64String.length);
  e.preventDefault();
  const formData = new FormData(e.target);
  const formProps = Object.fromEntries(formData);
  let data = {
    ...formProps,
    imagen: base64String,
  };
  console.log(data);
  fetch("http://localhost:5000/peliculas", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((Result) => Result.json())
    .then((data) => {
      document.getElementById("pelicula-select").innerHTML =
        '<option value="">--Please choose an option--</option>';
      loadMoviesOptions();
      loadFormMovie(false);
      // your code comes here
    })
    .catch((errorMsg) => {
      console.log(errorMsg);
    });
};

const sendReseña = (e) => {
  e.preventDefault();
  e.preventDefault();
  const formData = new FormData(e.target);
  const formProps = Object.fromEntries(formData);
  let data = {
    ...formProps,
    id_usuario: localStorage.getItem("userId"),
  };
  fetch(
    id
      ? "http://localhost:5000/reseñas/" + id
      : "http://localhost:5000/reseñas",
    {
      method: id ? "PUT" : "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  )
    .then((Result) => Result.json())
    .then((data) => {
      window.location.replace("http://localhost:8000/");
    })
    .catch((errorMsg) => {
      console.log(errorMsg);
    });
};
