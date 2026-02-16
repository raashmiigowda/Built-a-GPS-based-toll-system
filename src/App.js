import React, { useEffect, useState } from "react";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState(0);

  const fetchTransactions = () => {
    fetch("http://localhost:5000/transactions")
      .then(res => res.json())
      .then(data => setTransactions(data));
  };

  const fetchBalance = () => {
    fetch("http://localhost:5000/balance/vehicle_1")
      .then(res => res.json())
      .then(data => setBalance(data.balance));
  };

  useEffect(() => {
    fetchTransactions();
    fetchBalance();
    const interval = setInterval(() => {
      fetchTransactions();
      fetchBalance();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🚗 GPS Toll System</h1>

      <h2>Balance: ₹{balance}</h2>

      <h2>Transactions</h2>
      {transactions.map((t, i) => (
        <div key={i}>
          Vehicle: {t.vehicle_id} | ₹{t.amount}
        </div>
      ))}
    </div>
  );
}

export default App;
