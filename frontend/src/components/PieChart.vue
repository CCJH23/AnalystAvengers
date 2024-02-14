<template>
    <div id="chartContainer" style="height: 300px; width: 55%; margin-left:200px;"></div>
  </template>
  
  <script>
  export default {
    mounted() {
      // Define different shades of green
      const shadesOfGreen = ["#4CAF50", "#689F38", "#8BC34A", "#CDDC39", "#AFB42B"];
  
      // Define your data points
      const dataPoints = [
        { y: 32, label: "Desktop" },
        { y: 20, label: "Mobile" },
        { y: 12, label: "Tablet" }
      ];
  
      // Compute total count
      const totalCount = dataPoints.reduce((acc, curr) => acc + curr.y, 0);
  
      // Calculate percentage for each data point and assign a shade of green
      dataPoints.forEach((dataPoint, index) => {
        dataPoint.percentage = ((dataPoint.y / totalCount) * 100).toFixed(2);
        dataPoint.color = shadesOfGreen[index % shadesOfGreen.length]; // Assign a shade of green
      });
  
      // Create the pie chart when the component is mounted
      const chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        data: [{
          type: "pie",
          startAngle: 240,
          yValueFormatString: "(##0)",
          indexLabel: "{label} {y}",
          toolTipContent: "{label}: {percentage}% {y} ",
          dataPoints: dataPoints
        }]
      });
      chart.render();
    }
  }
  </script>
  