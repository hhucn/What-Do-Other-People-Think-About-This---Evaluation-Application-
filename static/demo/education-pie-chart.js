// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


let education_dict = JSON.parse(document.currentScript.nextElementSibling.textContent);

// Pie Chart Example
var ctx = document.getElementById("educationPieChart");
var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ["abitur", "Bachelor", "Master", "PHD"],
        datasets: [{
            data: [education_dict['abitur'] || 0, education_dict['bachelor'] || 0, education_dict['master'] || 0, education_dict['phd'] || 0],
            backgroundColor: ['#008000', '#FF0000', '#FFFF00', '#001eff'],
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
