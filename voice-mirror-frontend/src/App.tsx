import "./App.css";
import AppLayout from "./layouts/AppLayout";
import HomePage from "./pages/HomePage";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  redirect,
} from "react-router-dom";
import CreatePage from "./pages/CreatePage";
import EditPage from "./pages/EditPage";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";
import { useContext } from "react";
import { ProfileContext } from "./contexts/ProfileContext";

function App() {
  return (
    <AppLayout>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/create" element={<CreatePage />} />
          <Route path="/edit/:name" element={<EditPage />} />
          <Route path="/chat/:name" element={<ChatPage />} />
          <Route path="/login" element={<LoginPage />} />
        </Routes>
      </Router>
    </AppLayout>
  );
}

export default App;
