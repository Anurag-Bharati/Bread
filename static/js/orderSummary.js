const renderChart=(data,labels)=>{
  var ctx = document.getElementById("myChart").getContext("2d");
  var myChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: labels,
          datasets: [{
              label: 'Category of Orders',
              data: data,
              backgroundColor: [
                  'rgba(255, 99, 132, 0.8)',
                  'rgba(54, 162, 235, 0.8)',
                  'rgba(255, 206, 86, 0.8)',
                  'rgba(75, 192, 192, 0.8)',
                  'rgba(153, 102, 255, 0.8)',
                  'rgba(255, 159, 64, 0.8)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 2
          }]
      },
      options: {
          title:{
              display:true,
              text:'Summary of orders',
          },
          responsive: true
      },
  });
};
const getChartData=()=>{

  fetch('../manage/order-summary')
  .then(res=>res.json())
  .then(results=>{
    console.log('results',results);
    const category_data = results.order_summary;
    const [labels, data]=[
      Object.keys(category_data),
      Object.values(category_data)
    ]
    renderChart(data,labels);
  })
}
document.onload=getChartData();

