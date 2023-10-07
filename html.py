import json
import boto3

html = '''<!DOCTYPE html>
<html>
<head>
    <title>Transaction Total Counter</title>
    <style>
        body {
            background-color: #f0f0f0;
            text-align: center;
            font-family: Arial, sans-serif;
        }

        h1 {
            color: #333;
        }

        form {
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
        }

        input[type="text"] {
            width: 10%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        button {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        #status {
            margin-top: 10px;
            color: #333;
        }

        #transactions-total {
            margin-top: 10px;
            color: #333;
        }

        #transactions-count {
            margin-top: 10px;
            color: #333;
        }

        #transactions-category {
            margin-top: 10px;
            color: #333;
        }

        #chart-container {
            width: 50%;
            margin: 0 auto;
        }

        canvas {
            max-width: 100%;
        }
    </style>
</head>
<body>
    <h1>Transaction Total Counter</h1>
    <form id="write-form">
        <input type="text" name="content" id="content" placeholder="Enter content">
        <button type="submit">Count Transactions</button>
    </form>
    <div id="status"></div>
    <div id="transactions-total"></div>
    <div id="transactions-count"></div>
    <div id="transactions-category"></div>
    <div id="chart-container">
        <canvas id="chart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
document.getElementById('write-form').addEventListener('submit', function (e) {
    e.preventDefault();

    var content = document.getElementById('content').value;

    if (!content) {
        alert("Please enter content.");
        return;
    }

    fetch('https://518julmqj9.execute-api.us-east-1.amazonaws.com/default/create_file_s3', {
        method: 'POST',
        body: JSON.stringify({ "content": content })
    })
    .then(response => response.json())
    .then(data => {
        var statusElement = document.getElementById('status');
        statusElement.innerHTML = 'The search is working successfully!';
        statusElement.style.color = 'green';

        fetch('https://0mmcz2p1dh.execute-api.us-east-1.amazonaws.com/default/count_transactions')
        .then(response => response.json())
        .then(result => {
            var transactionsTotalElement = document.getElementById('transactions-total');
            transactionsTotalElement.innerHTML = 'Transactions Total Amount: <span style="color: red; font-weight: bold;">' + result.transactions_total_amount + '</span>';

            var transactionsCountElement = document.getElementById('transactions-count');
            transactionsCountElement.innerHTML = 'Transactions Count: ' + result.transactions_count;

            var transactionsCategoryElement = document.getElementById('transactions-category');
            transactionsCategoryElement.innerHTML = 'Transactions by Category:';
            createPieChart(result.category_totals);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching data from the second API.');
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while writing to file.');
    });
});

function createPieChart(data) {
    var ctx = document.getElementById('chart').getContext('2d');
    var myChart;

    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',    // Red
                    'rgba(54, 162, 235, 0.8)',    // Blue
                    'rgba(255, 206, 86, 0.8)',    // Yellow
                    'rgba(75, 192, 192, 0.8)',    // Turquoise
                    'rgba(153, 102, 255, 0.8)',   // Purple
                    'rgba(255, 0, 0, 0.8)',       // Red
                    'rgba(0, 255, 0, 0.8)',       // Green
                    'rgba(0, 0, 255, 0.8)',       // Blue
                    'rgba(255, 165, 0, 0.8)'      // Orange
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: 'Transaction Categories'
            },
            legend: {
                display: true,
                position: 'right',
                labels: {
                    fontSize: 10
                }
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        var dataset = data.datasets[tooltipItem.datasetIndex];
                        var total = dataset.data.reduce(function (previousValue, currentValue) {
                            return previousValue + currentValue;
                        });
                        var currentValue = dataset.data[tooltipItem.index];
                        var percentage = ((currentValue / total) * 100).toFixed(2) + '%';
                        return data.labels[tooltipItem.index] + ': ' + currentValue + ' (' + category_percentages + ')';
                    }
                }
            }
        }
    });
}

    </script>
</body>
</html>
'''

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return {
            'statusCode': 200,
            'headers': {
                "content-type": "text/html; charset=utf-8"
            },
            'body': html
        }
    elif event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        content = body.get('content', '')

        content = content.upper()

        s3 = boto3.client('s3')
        bucket_name = 'game-saves-kapalulz'

        try:
            s3.put_object(Bucket=bucket_name, Key='word.txt', Body=content.encode('utf-8'))
            return {
                'statusCode': 200,
                'body': json.dumps('Content written to file successfully')
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error: {str(e)}')
            }
