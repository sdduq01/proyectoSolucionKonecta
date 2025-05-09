console.log("Archivo JS cargado correctamente");

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM cargado y listo");

    const createAlertButton = document.getElementById("create-alert-button");
    const campaignSelect = document.getElementById("campaign");

    // 🟢 Cargar campañas desde la función Cloud al iniciar
    fetch("https://us-central1-kam-bi-451418.cloudfunctions.net/get_campaigns")
        .then(response => response.json())
        .then(data => {
            console.log("✅ Campañas recibidas:", data);
            data.forEach(campaign => {
                const option = document.createElement("option");
                option.value = campaign;
                option.textContent = campaign;
                campaignSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error("❌ Error al obtener campañas:", error);
            alert("⚠️ No se pudieron cargar las campañas.");
        });

    if (createAlertButton) {
        createAlertButton.addEventListener("click", function () {
            console.log("Botón clickeado");

            const campaign = campaignSelect.value.trim(); // Usar el valor seleccionado
            const metric = document.getElementById("metric").value.trim();
            const target = document.getElementById("target").value.trim();
            const frequency = document.getElementById("frequency").value.trim();
            const whatsapp = document.getElementById("whatssapp").value.trim();
            const email = document.getElementById("email").value.trim();

            if (!campaign || !metric || !target) {
                alert("❗Por favor completa los campos obligatorios: Campaign, Metric y Target.");
                return;
            }

            const message = `
🚨 Se va a crear una alerta con los siguientes parámetros:

📌 Campaign: ${campaign}
📊 Metric: ${metric}
🎯 Target: ${target}
⏱ Frecuencia: ${frequency || 'No especificada'}
📱 WhatsApp: ${whatsapp || 'No especificado'}
📧 Email: ${email || 'No especificado'}

¿Deseas continuar?`;

            if (confirm(message)) {
                const data = {
                    campaign,
                    metric,
                    target,
                    frequency,
                    whatsapp,
                    email,
                };

                const resumen = document.getElementById("resumen");
                resumen.innerHTML = `
                    <strong>Resumen:</strong><br/>
                    Va a crear una alerta para la campaña <strong>${campaign}</strong>, métrica <strong>${metric}</strong>,
                    objetivo <strong>${target}</strong>, frecuencia <strong>${frequency || 'No especificada'}</strong>,
                    WhatsApp <strong>${whatsapp || 'No especificado'}</strong> y correo <strong>${email || 'No especificado'}</strong>.
                `;

                console.log("✅ Confirmado. Alerta creada:", data);

                fetch("https://us-central1-kam-bi-451418.cloudfunctions.net/save_alert", { 
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                .then(response => {
                    if (response.ok) {
                        alert("✅ La alerta fue enviada y guardada correctamente.");
                        console.log("✅ Datos enviados al backend con éxito.");
                    } else {
                        alert("⚠️ Ocurrió un error al enviar la alerta.");
                        console.error("❌ Error en la respuesta del backend:", response.statusText);
                    }
                })
                .catch(error => {
                    alert("⚠️ No se pudo conectar con el servidor.");
                    console.error("❌ Error de conexión:", error);
                });
            } else {
                console.log("❌ Cancelado por el usuario.");
            }
        });
    } else {
        console.error("❌ No se encontró el botón de crear alerta.");
    }
});
