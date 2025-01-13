// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function (n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}


const news_agencies_question_data = JSON.parse(document.currentScript.nextElementSibling.textContent);
const news_agencies = news_agencies_question_data["news_agencies"]
const news_agencies_comment_percentages = news_agencies_question_data["CommentAnswer"]
const news_agencies_model_comment_percentages = news_agencies_comment_percentages["model"]
const news_agencies_random_comment_percentages = news_agencies_comment_percentages["random"]
const news_agencies_point_of_view_percentages = news_agencies_question_data["PointOfViewAnswers"]

// Bar Chart Example
var ctx = document.getElementById("percentages-news-agencies-comment-questions");
var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: news_agencies,
        datasets: [{
            label: "Quality of Recommendations of single comments (Model)",
            backgroundColor: "#4e73df",
            hoverBackgroundColor: "#2e59d9",
            borderColor: "#4e73df",
            data: news_agencies_model_comment_percentages
        },
            {
                label: "Quality of Recommendations of single comments (Random)",
                backgroundColor: "#2cfc00",
                hoverBackgroundColor: "#2cfc00",
                borderColor: "#2cfc00",
                data: news_agencies_random_comment_percentages
            },
            {
                label: "Preference of model over random regarding diversity",
                backgroundColor: "#ff0000",
                hoverBackgroundColor: "#ff0000",
                borderColor: "#ff0000",
                data: news_agencies_point_of_view_percentages
            }
        ],
    },
    options: {
        maintainAspectRatio: false,
        layout: {
            padding: {
                left: 10,
                right: 25,
                top: 25,
                bottom: 0
            }
        },
        scales: {
            xAxes: [{
                time: {
                    unit: 'percent',
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Question ID'
                },
                gridLines: {
                    display: false,
                    drawBorder: false
                },
                ticks: {
                    maxTicksLimit: 14
                },
                maxBarThickness: 25,
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: 100,
                    maxTicksLimit: 5,
                    padding: 10,
                },
                scaleLabel: {
                    display: true,
                    labelString: 'percentage'
                },
                gridLines: {
                    color: "rgb(234, 236, 244)",
                    zeroLineColor: "rgb(234, 236, 244)",
                    drawBorder: false,
                    borderDash: [2],
                    zeroLineBorderDash: [2]
                }
            }],
        },
        legend: {
            display: true
        },
        tooltips: {
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
            callbacks: {
                label: function (tooltipItem, chart) {
                    return number_format(tooltipItem.yLabel) + "%";
                }
            }
        },
    }
});
