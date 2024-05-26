import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
} from "chart.js";
import "chartjs-adapter-date-fns"; // Import the adapter
import { useEffect, useState } from "react";

// Register the chart.js components we will use
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale, // Make sure to register TimeScale
);

export function Market() {
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      fetch("http://127.0.0.1:8000/stocks") // Adjust this URL to your actual API endpoint
        .then((response) => response.json())
        .then((data) => setStocks(data))
        .catch((error) => console.error("Error fetching stocks:", error));
    };

    fetchData(); // Initial fetch

    const intervalId = setInterval(fetchData, 15000); // Set up the interval to refetch every 15 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  // This will format our fetched stock data into a format that Chart.js can use

  const formatChartData = (prices) => {
    // Ensure data is sorted by timestamp
    const sortedPrices = prices.sort(
      (a, b) => new Date(a.timestamp) - new Date(b.timestamp),
    );
    const dataPoints = sortedPrices.map((price) => ({
      x: new Date(price.timestamp),
      y: price.price,
    }));

    return {
      labels: sortedPrices.map((price) => new Date(price.timestamp)),
      datasets: [
        {
          data: dataPoints,
          fill: false,
          borderColor: "rgba(75,192,192,1)", // default fallback color
          segment: {
            borderColor: (ctx) => {
              // Get indices of the current (p1) and previous (p0) data points
              const p1Index = ctx.p1DataIndex;
              const p0Index = ctx.p0DataIndex;

              // Validate indices to prevent errors
              if (
                p0Index == null ||
                p1Index == null ||
                p0Index < 0 ||
                p1Index <= 0
              ) {
                return "rgba(75,192,192,1)"; // Default color for undefined segments
              }

              // Apply color based on price change direction
              return dataPoints[p1Index].y > dataPoints[p0Index].y
                ? "rgba(0, 255, 0, 1)"
                : "rgba(255, 0, 0, 1)";
            },
          },
          backgroundColor: "rgba(75,192,192,0.2)",
        },
      ],
    };
  };

  const options = {
    scales: {
      x: {
        type: "time",
        time: {
          unit: "day",
          tooltipFormat: "MM/dd/yyyy",
        },
      },
      y: {
        title: {
          display: true,
          text: "Price ($)",
        },
      },
    },
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: "index",
        intersect: false,
      },
    },
  };

  return (
    <div className="flex flex-col w-[600px] h-[500px] bg-neutral-800 border-t-[3px] border-l-[3px] border-b-[3px] border-r-[3px] border-colors-custom">
      <div className="w-full overflow-y-scroll flex flex-col gap-5 py-3">
        {stocks.map((stock) => (
          <div
            key={stock.symbol}
            className="flex justify-between items-center px-8"
          >
            <div className="text-white">
              <h2>{stock.name}</h2>
            </div>
            <div className="w-[230px] h-[100px]">
              <Line data={formatChartData(stock.prices)} options={options} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
