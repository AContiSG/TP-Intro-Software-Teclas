const loginSubmit = (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const formProps = Object.fromEntries(formData);

  fetch("http://localhost:5000/usuarios/nombre/" + formProps.userName)
    .then((Result) => Result.json())
    .then((data) => {
      if (data.id) {
        localStorage.setItem("userId", data.id);
        localStorage.setItem("userNombre", data.nombre);
        localStorage.setItem("userEdad", data.edad);
        localStorage.setItem("userGenero", data.genero);
        window.location.replace("http://localhost:8000/");
      }
    })
    .catch((errorMsg) => {
      console.log(errorMsg);
    });
};

const registerSubmit = (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const formProps = Object.fromEntries(formData);

  fetch("http://localhost:5000/usuarios", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formProps),
  })
    .then((Result) => Result.json())
    .then((data) => {
      if (data.id) {
        localStorage.setItem("userId", data.id);
        localStorage.setItem("userNombre", data.nombre);
        localStorage.setItem("userEdad", data.edad);
        localStorage.setItem("userGenero", data.genero);
        window.location.replace("http://localhost:8000/");
      }
    })
    .catch((errorMsg) => {
      console.log(errorMsg);
    });
};

async function getUsers() {
  try {
    const response = await fetch("http://localhost:5000/usuarios");

    const json = response.json();
    console.log(json);
  } catch (error) {
    console.error(error.message);
  }
}

function openRegister(e) {
  e.preventDefault();
  document.getElementById("registrarse").classList.add("active");
  document.getElementById("iniciar-sesion").classList.remove("active");
}

function openLogin(e) {
  e.preventDefault();
  document.getElementById("iniciar-sesion").classList.add("active");
  document.getElementById("registrarse").classList.remove("active");
}
