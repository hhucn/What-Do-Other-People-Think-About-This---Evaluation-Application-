// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


let gender_dict = JSON.parse(document.currentScript.nextElementSibling.textContent);

// Pie Chart Example
var ctx = document.getElementById("genderPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["Male", "Female", "Divers", "None"],
        datasets: [{
            data: [gender_dict['male'] || 0, gender_dict['female'] || 0, gender_dict['divers'] || 0, gender_dict['none'] || 0],
            backgroundColor: ['#008000', '#FF0000', '#FFFF00', '#0000FF'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});
