const buttonform = document.getElementById("button-container");
const parametersalertform = document.getElementById("parametersalertform");
const parameterssendform = document.getElementById("parameterssendform");
const resum = document.getElementById("resumen");

buttonform.addEventListener("click", (event) => {
    event.preventDefault();
    const campaign = parametersalertform.elements["campaign"].value;
    const metric = parametersalertform.elements["metric"].value;
    const target = parametersalertform.elements["target"].value;
    const frequency = parameterssendform.elements["frequency"].value;
    const whatssapp = parameterssendform.elements["whatssapp"].value;
    const email = parameterssendform.elements["email"].value;

    if (campaign) {
        resum.append(createSpanTitle());
        resum.append(createSpanElement(campaign, metric, target, frequency, whatssapp, email))
    }
});

function createSpanElement(campaign, metric, target, frequency, whatssapp, email) {
    const span = document.createElement("span");
    span.innerHTML = `Va a crear una alerta para la campaña <strong>${campaign}</strong>, métrica <strong>${metric}</strong>, objetivo <strong>${target}</strong>, frecuencia <strong>${frequency}</strong>, WhatsApp <strong>${whatssapp}</strong>, y correo electrónico <strong>${email}</strong>.`;
    return span;
};
function createSpanTitle() {
    const span = document.createElement("span");
    span.innerHTML = `Resumen: `;
    return span;
};

