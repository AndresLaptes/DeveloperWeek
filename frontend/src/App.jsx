import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header"; 
import Footer from "./components/Footer";
import Teams from "./pages/Teams";
import Profile from "./pages/Profile";
import "./App.css";
const Home = () => {
  return <div>Home Page!</div>;
};

const About = () => {
  return <div>About Page</div>;
};

function App() {
  return (
    <>
      <Router>
        <div className="app-container">
          <Header className = "header"/>
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path = "/Teams" element = {<Teams />} />
              <Route path = "/Profile" element = {<Profile />} />
            </Routes>
          </main>
          <Footer className = "footer"/>
        </div>
      </Router>
    </>
  );
}

export default App
