const buttonform = document.getElementById("button-container");
const parametersalertform = document.getElementById("parametersalertform");
const parameterssendform = document.getElementById("parameterssendform");

buttonform.addEventListener("click", (event) => {
    event.preventDefault();
    const campaign = parametersalertform.elements["campaign"].value;
    const metric = parametersalertform.elements["metric"].value;
    const target = parametersalertform.elements["target"].value;

    const frequency = parameterssendform.elements["frequency"].value;
    const whatssapp = parameterssendform.elements["whatssapp"].value;
    const email = parameterssendform.elements["email"].value;

    console.log(campaign);
    console.log(metric);
    console.log(target);
    console.log(frequency);
    console.log(whatssapp);
    console.log(email);
})

