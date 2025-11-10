var chartSetoresInstance = null;
var chartPontosInstance = null;

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

function updateDashboardStats() {
  const dateFilter = document.getElementById("date-filter");
  const currentDate = dateFilter ? dateFilter.value : "";

  let apiUrl = "/api/dashboard_stats";
  if (currentDate) {
    apiUrl += "?date=" + currentDate;
  }

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      const cardTrabalhando = document.getElementById("card-trabalhando-agora");
      const cardEntradas = document.getElementById("card-entradas-dia");
      const cardSaidas = document.getElementById("card-saidas-dia");

      if (cardTrabalhando)
        cardTrabalhando.innerText = data.voluntarios_trabalhando_agora;
      if (cardEntradas) cardEntradas.innerText = data.entradas_do_dia;
      if (cardSaidas) cardSaidas.innerText = data.saidas_do_dia;

      if (chartPontosInstance) {
        chartPontosInstance.data.labels = data.dias_labels;
        chartPontosInstance.data.datasets[0].data = data.dias_data;
        chartPontosInstance.update();
      }
    })
    .catch((e) => console.error("Erro ao atualizar dashboard:", e));
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

      if (window.location.pathname.includes("/home")) {
        console.log("Atualizando dashboard via API...");
        showDynamicFlash(data.msg, "success");
        updateDashboardStats();
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

  const dateFilter = document.getElementById("date-filter");
  if (dateFilter) {
    dateFilter.addEventListener("change", (e) => {
      const newDate = e.target.value;
      if (newDate) {
        window.location.href = "/home?date=" + newDate;
      } else {
        window.location.href = "/home";
      }
    });
  }

  const dateFilterDia = document.getElementById("date-filter-dia");
  const downloadBtnDia = document.getElementById("btn-download-dia");
  if (dateFilterDia && downloadBtnDia) {
    dateFilterDia.addEventListener("change", (e) => {
      const newDate = e.target.value;
      let baseUrl = downloadBtnDia.href.split("?")[0];
      if (newDate) {
        downloadBtnDia.href = baseUrl + "?date=" + newDate;
      }
    });
  }

  if (typeof Chart !== "undefined" && window.chartData) {
    const ctxSetores = document.getElementById("chartSetores");
    if (ctxSetores) {
      chartSetoresInstance = new Chart(ctxSetores, {
        type: "doughnut",
        data: {
          labels: window.chartData.setores_labels,
          datasets: [
            {
              label: "Movimentações",
              data: window.chartData.setores_data,
              backgroundColor: [
                "#4F46E5",
                "#7C3AED",
                "#EC4899",
                "#F59E0B",
                "#10B981",
                "#3B82F6",
                "#6366F1",
                "#D946EF",
                "#FCD34D",
                "#34D399",
              ],
              hoverOffset: 4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "left",
            },
          },
        },
      });
    }

    const ctxPontos = document.getElementById("chartPontos");
    if (ctxPontos) {
      chartPontosInstance = new Chart(ctxPontos, {
        type: "bar",
        data: {
          labels: window.chartData.dias_labels,
          datasets: [
            {
              label: "Registros de Ponto",
              data: window.chartData.dias_data,
              backgroundColor: "rgba(79, 70, 229, 0.7)",
              borderColor: "rgba(79, 70, 229, 1)",
              borderWidth: 1,
              borderRadius: 4,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 50,
            },
          },
          plugins: {
            legend: {
              display: false,
            },
          },
        },
      });
    }
  }
});
