import React, { PureComponent } from 'react'
import CaptureVideoButton from './components/CaptureVideoButton';
import TradingGrid from './components/TradingGrid';
import 'semantic-ui-css/semantic.min.css'
import './style/app.css';
import { Container } from 'semantic-ui-react';

export default class App extends PureComponent {
  render() {
    return (
      <div className="main-page">
        <Container>
          <TradingGrid />
        </Container>
      </div>
    )
  }
}