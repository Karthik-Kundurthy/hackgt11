import "./App.css";
import AppLayout from "./AppLayout";
import HomePage from "./HomePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreatePage from "./CreatePage";

function App() {
  return (
    <AppLayout>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreatePage />} />
        </Routes>
      </Router>
    </AppLayout>
  );
}

export default App;
