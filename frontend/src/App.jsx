import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header"; 
import Footer from "./components/Footer";
import Teams from "./pages/Teams";
import Profile from "./pages/Profile";
import Home from "./pages/Home";
import "./App.css";


const About = () => {
  return <div>About Page</div>;
};

function App() {
  return (
    <>
      <Router>
        <Header className = "header"/>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/About" element={<About />} />
            <Route path = "/Teams" element = {<Teams />} />
            <Route path = "/Profile" element = {<Profile />} />
          </Routes>
        </main>
        <Footer className = "footer"/>
    </Router>
  </>
  );
}

export default App
