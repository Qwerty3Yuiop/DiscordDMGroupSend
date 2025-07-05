import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar'
import Homepage from './screens/Home'
import Settingspage from './screens/Settings';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/settings" element={<Settingspage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
