function loadSentimentChart(labels, values) {
    const ctx = document.getElementById('sentimentChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Average Sentiment",
                data: values
            }]
        },
        options: {
            scales: {
                y: {
                    min: -1,
                    max: 1
                }
            }
        }
    });
}