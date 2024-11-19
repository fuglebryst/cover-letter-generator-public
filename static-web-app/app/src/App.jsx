// frontend/src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import Terms from './pages/Terms';
import JobMatcher from './pages/JobMatcher';
import CoverLetterGenerator from './pages/CoverLetterGenerator'; // Import the new page

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/om-oss" element={<About />} />
        <Route path="/kontakt" element={<Contact />} />
        <Route path="/betingelser" element={<Terms />} />
        <Route path="/jobb-matcher" element={<JobMatcher />} />
        <Route path="/cover-letter-generator" element={<CoverLetterGenerator />} /> {/* New Route */}
      </Routes>
    </Router>
  );
}

export default App;
