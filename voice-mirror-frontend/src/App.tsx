import "./App.css";
import AppLayout from "./layouts/AppLayout";
import HomePage from "./pages/HomePage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreatePage from "./pages/CreatePage";
import EditPage from "./pages/EditPage";
import ChatPage from "./pages/ChatPage";

function App() {
  return (
    <AppLayout>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreatePage />} />
          <Route path="/edit/:id" element={<EditPage />} />
          <Route path="/chat/:id" element={<ChatPage />} />
        </Routes>
      </Router>
    </AppLayout>
  );
}

export default App;
