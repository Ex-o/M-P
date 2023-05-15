import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";

import { Container, Navbar, Nav } from "react-bootstrap";

import AboutUs from "./pages/AboutUs";
import Contacts from "./pages/ContactUs";
import Home from "./pages/Home";
import Restaurant from "./pages/Restaurant";

const App = () => (
  <div className="App">
    <Router>
      <Navbar bg="light" expand="lg">
        <Container>
          <Navbar.Brand href="/">Hitchy!</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">
                Restuarants
              </Nav.Link>
              <Nav.Link as={Link} to="/about">
                About Us
              </Nav.Link>
              <Nav.Link as={Link} to="/contacts">
                Contacts
              </Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/restaurants/:name" element={<Restaurant />} />
        </Routes>
      </Container>
    </Router>
  </div>
);

export default App;
