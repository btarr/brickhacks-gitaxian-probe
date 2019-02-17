import React, { PureComponent } from 'react'
import StreamOutput from './components/StreamOutput';

const WEBCAM_CONSTRAINTS = { video: true }

export default class App extends PureComponent {

  constructor() {
    super()
    this.state = {
      stream: null
    }
    this.onWebcamAccess = this.onWebcamAccess.bind(this);
    this.onNoWebcamAccess = this.onNoWebcamAccess.bind(this);
  }
  
  onWebcamAccess(stream) {
    if (stream) {
      this.setState({
        stream: stream
      });
    }
  }
  
  onNoWebcamAccess() {

  }

  componentDidMount() {
    navigator.getUserMedia(WEBCAM_CONSTRAINTS, this.onWebcamAccess, this.onNoWebcamAccess);
  }

  render() {
    return (
      <StreamOutput 
        src={this.state.stream}
      />
    )
  }
}