import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Book, Code, Database, Server, Award, Zap } from 'react-feather';
import '../styles/AboutPage.css';

const AboutPage = () => {
  return (
    <Container className="about-page">
      <div className="page-header text-center mb-5">
        <h1 className="display-4 mb-3">About Grid Scenario Generator</h1>
        <p className="lead">
          An advanced AI-powered platform for generating realistic power grid scenarios using 
          Physics-Informed Neural Networks and Retrieval Augmented Generation
        </p>
      </div>

      <Row className="mb-5">
        <Col lg={6} className="mb-4 mb-lg-0">
          <div className="about-section">
            <h2 className="section-title">Our Mission</h2>
            <p>
              Grid Scenario Generator aims to revolutionize power grid modeling by combining 
              state-of-the-art AI techniques with domain-specific physical constraints to create 
              realistic, physically-consistent grid scenarios for research, planning, and testing.
            </p>
            <p>
              Our platform enables power system engineers, researchers, and utility companies to 
              generate synthetic grid scenarios that reflect real-world conditions, helping them 
              to develop more robust and resilient power systems.
            </p>
          </div>
        </Col>
        <Col lg={6}>
          <div className="about-section">
            <h2 className="section-title">Core Technologies</h2>
            <p>
              Our platform leverages several cutting-edge technologies to deliver high-quality grid scenario generation:
            </p>
            <ul className="tech-list">
              <li>
                <span className="tech-icon"><Zap size={20} /></span>
                <span>Physics-Informed Neural Networks (PINNs)</span>
              </li>
              <li>
                <span className="tech-icon"><Database size={20} /></span>
                <span>Retrieval Augmented Generation (RAG)</span>
              </li>
              <li>
                <span className="tech-icon"><Server size={20} /></span>
                <span>OpenDSS Validation</span>
              </li>
              <li>
                <span className="tech-icon"><Code size={20} /></span>
                <span>Advanced Prompt Engineering</span>
              </li>
            </ul>
          </div>
        </Col>
      </Row>

      <div className="key-features mb-5">
        <h2 className="section-title text-center mb-4">Key Features</h2>
        <Row>
          <Col md={4} className="mb-4">
            <Card className="feature-card h-100">
              <Card.Body>
                <div className="feature-icon">
                  <Zap size={32} />
                </div>
                <Card.Title>Physics-Informed Generation</Card.Title>
                <Card.Text>
                  Generate scenarios that adhere to physical laws and grid constraints, ensuring realistic 
                  and valid power flow solutions.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="feature-card h-100">
              <Card.Body>
                <div className="feature-icon">
                  <Database size={32} />
                </div>
                <Card.Title>RAG-Enhanced Creation</Card.Title>
                <Card.Text>
                  Leverage existing scenarios to inform and enhance new generation, combining the best of 
                  retrieval and generative approaches.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="feature-card h-100">
              <Card.Body>
                <div className="feature-icon">
                  <Server size={32} />
                </div>
                <Card.Title>Industry-Standard Validation</Card.Title>
                <Card.Text>
                  Validate generated scenarios with OpenDSS, ensuring compatibility with industry-standard 
                  power system analysis tools.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>

      <div className="team-section mb-5">
        <h2 className="section-title text-center mb-4">Our Team</h2>
        <Row>
          <Col md={4} className="mb-4">
            <Card className="team-card text-center">
              <div className="team-avatar">
                <img src="/team-placeholder.png" alt="Team Member" className="img-fluid" />
              </div>
              <Card.Body>
                <Card.Title>Dr. Jane Smith</Card.Title>
                <Card.Subtitle className="mb-2">Lead AI Researcher</Card.Subtitle>
                <Card.Text>
                  Expert in machine learning and power systems with 10+ years of research experience.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="team-card text-center">
              <div className="team-avatar">
                <img src="/team-placeholder.png" alt="Team Member" className="img-fluid" />
              </div>
              <Card.Body>
                <Card.Title>Dr. John Davis</Card.Title>
                <Card.Subtitle className="mb-2">Power Systems Engineer</Card.Subtitle>
                <Card.Text>
                  Specialized in power flow analysis and grid modeling with experience at major utilities.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col md={4} className="mb-4">
            <Card className="team-card text-center">
              <div className="team-avatar">
                <img src="/team-placeholder.png" alt="Team Member" className="img-fluid" />
              </div>
              <Card.Body>
                <Card.Title>Dr. Sarah Johnson</Card.Title>
                <Card.Subtitle className="mb-2">Data Scientist</Card.Subtitle>
                <Card.Text>
                  Expert in data processing pipelines and RAG architectures for complex domains.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>

      <div className="publications-section">
        <h2 className="section-title text-center mb-4">Research & Publications</h2>
        <Row>
          <Col lg={10} className="mx-auto">
            <Card className="publication-card mb-3">
              <Card.Body>
                <div className="d-flex align-items-start">
                  <div className="publication-icon">
                    <Book size={24} />
                  </div>
                  <div>
                    <h5 className="publication-title">Physics-Informed Neural Networks for Power Grid Modeling</h5>
                    <p className="publication-authors">Smith, J., Davis, J., Johnson, S. (2024)</p>
                    <p className="publication-venue">IEEE Transactions on Power Systems</p>
                  </div>
                </div>
              </Card.Body>
            </Card>
            <Card className="publication-card mb-3">
              <Card.Body>
                <div className="d-flex align-items-start">
                  <div className="publication-icon">
                    <Book size={24} />
                  </div>
                  <div>
                    <h5 className="publication-title">Retrieval Augmented Generation for Enhanced Power Grid Scenario Creation</h5>
                    <p className="publication-authors">Johnson, S., Smith, J. (2023)</p>
                    <p className="publication-venue">Applied Energy, Vol. 156, pp. 45-67</p>
                  </div>
                </div>
              </Card.Body>
            </Card>
            <Card className="publication-card">
              <Card.Body>
                <div className="d-flex align-items-start">
                  <div className="publication-icon">
                    <Award size={24} />
                  </div>
                  <div>
                    <h5 className="publication-title">A Novel Approach to Synthetic Grid Scenario Validation</h5>
                    <p className="publication-authors">Davis, J., Johnson, S., Smith, J. (2023)</p>
                    <p className="publication-venue">Best Paper Award, IEEE Power & Energy Society General Meeting</p>
                  </div>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </div>
    </Container>
  );
};

export default AboutPage;