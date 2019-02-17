import React, { PureComponent } from 'react';

export default class StreamOutput extends PureComponent {

  constructor() {
    super()
    this.videoRef = React.createRef();
  }

  componentDidUpdate() {
    if (this.videoRef) {
      this.updateVideoStream();
    }
  }

  updateVideoStream() {
    if (this.videoRef.current.srcObject !== this.props.src) {
      this.videoRef.current.srcObject = this.props.src
    }
  }

  render() {
    const { src } = this.props;
    if (!src) {
      return null;
    }
    return (
      <video ref={this.videoRef} src={this.props.src} autoPlay={true} />
    );
  }
}