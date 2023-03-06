import { useEffect, useState } from "react";
import {
  Button,
  Card,
  Col,
  Container,
  Form,
  InputGroup,
  Row
} from "react-bootstrap";
import Items from "./static/Items.json";
import blank from "./static/blank.jpg";

function App() {
  const [selections, setSelections] = useState(
    Object.keys(Items).reduce((acc, cur) => ({ ...acc, [cur]: 0 }), {})
  );

  useEffect(() => {});

  const changeHandler = (key, inc) => (e) => {
    setSelections({
      ...selections,
      [key]: Math.max(0, selections[key] + (inc ? 1 : -1))
    });
  };

  const submitHandler = (e) => {
    e.preventDefault();
    const searchParams = new URLSearchParams(document.location.search);
    const hash = searchParams.get("hash");
    console.log(selections);
    fetch(process.env.REACT_APP_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        hash,
        selections
      })
    });
  };

  return (
    <div className="App">
      <Container>
        <Form onSubmit={submitHandler}>
          <Row>
            {Object.entries(Items).map(
              ([key, { display, description, img }]) => (
                <Col xs={6} md={4} lg={3} className="mt-4">
                  <Card
                    className={
                      selections[key] > 0
                        ? "border border-2 border-success"
                        : ""
                    }
                  >
                    <Card.Img variant="top" src={img ? img : blank} />
                    <Card.Body>
                      <Card.Title>{display}</Card.Title>
                      <Card.Text>{description}</Card.Text>
                      <InputGroup className="mb-3">
                        <Button
                          className="btn-danger"
                          disabled={selections[key] === 0}
                          onClick={changeHandler(key, false)}
                        >
                          -
                        </Button>
                        <Form.Control value={selections[key]} />
                        <Button
                          className="btn-success"
                          onClick={changeHandler(key, true)}
                        >
                          +
                        </Button>
                      </InputGroup>
                    </Card.Body>
                  </Card>
                </Col>
              )
            )}
          </Row>
          <Button variant="primary" type="submit" className="my-4 mx-auto">
            Submit
          </Button>
        </Form>
      </Container>
    </div>
  );
}

export default App;
