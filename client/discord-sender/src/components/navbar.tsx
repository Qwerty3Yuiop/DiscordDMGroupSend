import React, { useState } from 'react';
import { Menu, X, Home, Info, Mail, Settings } from 'lucide-react'; // Icons are still useful and lightweight
import DiscordIcon from "../assets/discord-icon.svg"
import "./navbar.css"
const Navbar: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <a href="#" className="navbar-logo-link">
          <a className="navbar-logo-icon"><img src={DiscordIcon} className="discord-logo"/>Discord Sender</a>
        </a>
      </div>
      <div className="gap"></div>
      <div className="navbar-container">
        <div className="navbar-links">
          <a href="#" className="navbar-link">
            <Home size={20} />
            <span>Home</span>
          </a>
          <a href="#" className="navbar-link">
            <Info size={20} />
            <span>Automatic Send</span>
          </a>
          <a href="#" className="navbar-link">
            <Mail size={20} />
            <span>Manual Send</span>
          </a>
          <a href="#" className="navbar-link">
            <Settings size={20} />
            <span>Settings</span>
          </a>
        </div>

        {/* Mobile Menu Button (Hamburger Icon) */}
        <div className="navbar-toggle">
          <button onClick={toggleMobileMenu} className="navbar-toggle-button">
            {isMobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation Links (conditionally rendered) */}
      {isMobileMenuOpen && (
        <div className="mobile-menu">
          <a href="#" className="mobile-menu-link">
            <Home size={20} />
            <span>Home</span>
          </a>
          <a href="#" className="mobile-menu-link">
            <Info size={20} />
            <span>About</span>
          </a>
          <a href="#" className="mobile-menu-link">
            <Mail size={20} />
            <span>Contact</span>
          </a>
          <a href="#" className="mobile-menu-link">
            <Settings size={20} />
            <span>Settings</span>
          </a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
