import React, { PureComponent } from 'react'
import CaptureVideoModal from './components/CaptureVideoModal';
import 'semantic-ui-css/semantic.min.css'

export default class App extends PureComponent {
  render() {
    return (
      <CaptureVideoModal />
    )
  }
}