//logica websocket
function showDynamicFlash(message, category) {
  var container = document.getElementById("dynamic-flash-container");
  if (!container) return;
  var alert = document.createElement("div");

  var bgColor = "bg-blue-100 text-blue-700 border-blue-300";
  if (category === "error") {
    bgColor = "bg-red-100 text-red-700 border-red-300";
  } else if (category === "success") {
    bgColor = "bg-green-100 text-green-700 border-green-300";
  }

  alert.className =
    "flash-message p-3 text-sm rounded-md transition duration-300 " + bgColor;
  alert.style.border = "1px solid";
  alert.innerText = message;

  container.appendChild(alert);

  setTimeout(() => {
    alert.style.opacity = "0";
    setTimeout(() => alert.remove(), 500);
  }, 5000);
}

document.addEventListener("DOMContentLoaded", (event) => {
  try {
    var socket = io.connect(
      window.location.protocol + "//" + document.domain + ":" + location.port
    );

    socket.on("connect", function () {
      console.log("Conectado ao servidor (Socket.IO)");
    });

    socket.on("update_ponto", function (data) {
      console.log("Evento recebido:", data.msg);
      if (window.location.pathname.includes("/ponto")) {
        showDynamicFlash(data.msg, "success");
        setTimeout(() => window.location.reload(), 1000);
      }
    });

    socket.on("update_voluntario", function (data) {
      console.log("Evento recebido:", data.msg);
      if (window.location.pathname.includes("/editar_voluntario")) {
        showDynamicFlash(data.msg, "success");
        setTimeout(() => window.location.reload(), 1000);
      }
    });

    socket.on("show_flash_message", function (data) {
      console.log("Evento recebido:", data.msg);
      showDynamicFlash(data.msg, data.category || "info");
    });
  } catch (e) {
    console.error("Falha ao conectar o Socket.IO. O servidor está rodando?", e);
  }

  setTimeout(() => {
    document.querySelectorAll(".flash-message").forEach((el) => {
      el.style.transition = "opacity 0.5s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    });
  }, 5000);
});
//fim logica websocket