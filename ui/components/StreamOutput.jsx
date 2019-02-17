import React, { PureComponent } from 'react';
import { List } from 'immutable';
import { Loader, Header } from 'semantic-ui-react';

const WEBCAM_CONSTRAINTS = { video: true }

const SEND_PICTURE_URL = 'http://localhost:5000'

export default class StreamOutput extends PureComponent {

  constructor() {
    super()
    this.videoRef = React.createRef();
    this.state = {
      videoOn: false,
      images: List(),
      stream: null,
      noWebcamAccess: false,
    }
    this.track = null;
    this.captureWebcamImage = this.captureWebcamImage.bind(this);
    this.updateVideoStream = this.updateVideoStream.bind(this);
    this.onWebcamAccess = this.onWebcamAccess.bind(this);
    this.onNoWebcamAccess = this.onNoWebcamAccess.bind(this);
    this.handleSendPictureToEndpoint = this.handleSendPictureToEndpoint.bind(this);
  }

  handleSendPictureToEndpoint(picture) {
    var fd = new FormData();
    fd.append('fname', 'checkImage.jpeg');
    fd.append('data', picture);
    return fetch(SEND_PICTURE_URL, {
      method: "POST",
      body: fd
    });
  }

  onWebcamAccess(stream) {
    if (stream) {
      this.setState({
        stream: stream
      });
    }
  }

  onNoWebcamAccess() {
    this.setState({
      noWebcamAccess: true,
    })
  }

  componentDidMount() {
    navigator.getUserMedia(WEBCAM_CONSTRAINTS, this.onWebcamAccess, this.onNoWebcamAccess);
  }

  componentDidUpdate() {
    if (this.videoRef && this.videoRef.current) {
      this.updateVideoStream();
    }
  }

  componentWillUnmount() {
    this.track.stop();
    clearTimeout(this.endpointPinger)
  }

  captureWebcamImage() {
    this.imageCapture.takePhoto().then(this.handleSendPictureToEndpoint);
    this.endpointPinger = setTimeout(this.captureWebcamImage, 500);
  }

  updateVideoStream() {
    if (this.videoRef.current.srcObject !== this.state.stream) {
      this.videoRef.current.srcObject = this.state.stream
      this.track = this.state.stream.getVideoTracks()[0];
      this.imageCapture = new ImageCapture(this.track);
      if (!this.state.videoOn) {
        this.setState({
          videoOn: true,
        })
        this.captureWebcamImage()
      }
    }
  }

  renderNoAccess() {
    return <Header as="h3">Could not access webcam</Header>;
  }

  render() {
    if (this.state.noWebcamAccess) {
      return this.renderNoAccess();
    }
    return (
      <video ref={this.videoRef} autoPlay={true} />
    );
  }
}