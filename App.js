import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement);

export default function App() {
  const [tab, setTab] = useState("predict");

  const [foodKg, setFoodKg] = useState("");
  const [peopleInput, setPeopleInput] = useState("");

  const [waste, setWaste] = useState(null);
  const [peopleServed, setPeopleServed] = useState(null);

  const [nutrition, setNutrition] = useState(null);
  const [imageText, setImageText] = useState("");

  const [history, setHistory] = useState([]);

  const [stats, setStats] = useState({
    totalFood: 0,
    totalWaste: 0
  });

  const ngos = [
    "Robin Hood Army",
    "Feeding India",
    "Roti Bank",
    "No Waste Kitchen"
  ];

  // 🔮 Calculation
  function calculateAll() {
    if (!foodKg || !peopleInput) return;

    const ratio = foodKg / peopleInput;

    const wasteVal = Math.max(
      0,
      0.08 * foodKg + 0.002 * peopleInput + (ratio > 0.3 ? 0.15 * (ratio - 0.3) : 0)
    );

    const people = Math.floor(foodKg / 0.3);

    setWaste(wasteVal.toFixed(2));
    setPeopleServed(people);

    setHistory([...history, { foodKg, people }]);

    setStats(prev => ({
      totalFood: prev.totalFood + Number(foodKg),
      totalWaste: prev.totalWaste + wasteVal
    }));
  }

  // 🧬 Nutrition
  function analyzeNutrition() {
    setNutrition({
      calories: 420,
      protein: 18,
      fat: 10,
      digestion: "3-5 hours"
    });
  }

  // 📸 Image
  function handleImage(e) {
    const file = e.target.files[0];
    if (file) {
      setImageText("Detected: Food Item 🍽️");
    }
  }

  // 📊 Chart
  const chartData = {
    labels: history.map((_, i) => `Try ${i + 1}`),
    datasets: [
      {
        label: "People Served",
        data: history.map(h => h.people)
      }
    ]
  };

  // 🥗 Diet Plan
  const dietPlan = [
    "Monday: Oats + Fruits 🥣",
    "Tuesday: Rice + Dal 🍚",
    "Wednesday: Chapati + Veg 🫓",
    "Thursday: Salad + Soup 🥗",
    "Friday: Brown Rice + Chicken 🍗",
    "Saturday: Fruits + Nuts 🍎",
    "Sunday: Cheat Day 🍕🔥"
  ];

  return (
    <div style={container}>

      {/* HEADER */}
      <div style={header}>
        <h2 style={{ color: "#4ade80" }}>🌿 FoodWise AI</h2>

        <div>
          <button onClick={() => setTab("predict")} style={btn}>Predict</button>
          <button onClick={() => setTab("nutrition")} style={btn}>Nutrition</button>
          <button onClick={() => setTab("diet")} style={btn}>Diet</button>
          <button onClick={() => setTab("dashboard")} style={btn}>Dashboard</button>
          <button onClick={() => setTab("donate")} style={btn}>Donate</button>
          <button onClick={() => setTab("image")} style={btn}>Image</button>
        </div>
      </div>

      <div style={{ padding: 20 }}>

        {/* 🔮 PREDICT */}
        {tab === "predict" && (
          <div style={card}>
            <h3>🍽️ Food Analysis</h3>

            <input
              placeholder="Food (kg)"
              value={foodKg}
              onChange={(e) => setFoodKg(e.target.value)}
              style={input}
            />

            <input
              placeholder="Number of People"
              value={peopleInput}
              onChange={(e) => setPeopleInput(e.target.value)}
              style={input}
            />

            <button onClick={calculateAll} style={mainBtn}>
              Analyze
            </button>

            {waste && (
              <div style={{ marginTop: 20 }}>
                <h2>⚠️ Waste: {waste} kg</h2>
                <h3>👥 People Served: {peopleServed}</h3>
              </div>
            )}
          </div>
        )}

        {/* 🧬 NUTRITION */}
        {tab === "nutrition" && (
          <div style={card}>
            <h3>🧬 Nutrition Analyzer</h3>

            <input placeholder="Enter food name" style={input} />
            <input type="file" style={{ marginTop: 10 }} />

            <button onClick={analyzeNutrition} style={mainBtn}>
              Analyze
            </button>

            {nutrition && (
              <div style={{ marginTop: 20 }}>
                <p>🔥 Calories: {nutrition.calories}</p>
                <p>💪 Protein: {nutrition.protein}g</p>
                <p>🥑 Fat: {nutrition.fat}g</p>
                <p>⏳ Digestion: {nutrition.digestion}</p>
              </div>
            )}
          </div>
        )}

        {/* 🥗 DIET */}
        {tab === "diet" && (
          <div style={card}>
            <h3>🥗 Weekly Diet Plan</h3>
            {dietPlan.map((d, i) => <p key={i}>{d}</p>)}
          </div>
        )}

        {/* 📊 DASHBOARD */}
        {tab === "dashboard" && (
          <div style={card}>
            <h3>📊 Dashboard</h3>

            <p>Total Food: {stats.totalFood} kg</p>
            <p>Total Waste: {stats.totalWaste.toFixed(2)} kg</p>

            <Bar data={chartData} />

            <h4>History</h4>
            {history.map((h, i) => (
              <p key={i}>{h.foodKg}kg → {h.people} people</p>
            ))}
          </div>
        )}

        {/* 🤝 DONATE */}
        {tab === "donate" && (
          <div style={card}>
            <h3>🤝 NGOs</h3>
            {ngos.map((ngo, i) => (
              <div key={i} style={ngoCard}>
                {ngo}
                <button style={donateBtn}>Donate</button>
              </div>
            ))}
          </div>
        )}

        {/* 📸 IMAGE */}
        {tab === "image" && (
          <div style={card}>
            <h3>📸 Food Image</h3>
            <input type="file" onChange={handleImage} />
            <p>{imageText}</p>
          </div>
        )}

      </div>
    </div>
  );
}

// styles
const container = {
  fontFamily: "Arial",
  background: "#0a0f0d",
  minHeight: "100vh",
  color: "white"
};

const header = {
  display: "flex",
  justifyContent: "space-between",
  padding: 20,
  background: "#111814"
};

const card = {
  background: "#161e1a",
  padding: 20,
  borderRadius: 12
};

const input = {
  display: "block",
  padding: 10,
  marginTop: 10,
  borderRadius: 8,
  border: "none",
  width: "100%"
};

const mainBtn = {
  marginTop: 15,
  padding: 10,
  background: "#4ade80",
  border: "none",
  borderRadius: 8,
  fontWeight: "bold"
};

const btn = {
  marginLeft: 10,
  padding: "6px 12px",
  background: "#4ade80",
  border: "none",
  borderRadius: 6
};

const ngoCard = {
  padding: 10,
  marginTop: 10,
  background: "#1c2620",
  borderRadius: 8
};

const donateBtn = {
  float: "right",
  background: "#4ade80",
  border: "none",
  borderRadius: 6,
  padding: "5px 10px"
};
