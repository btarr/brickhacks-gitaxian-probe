import React, { PureComponent } from 'react';
import { Button, Modal } from 'semantic-ui-react'
import StreamOutput from "./StreamOutput";

export default class CaptureVideoModal extends PureComponent {
  constructor() {
    super()
    this.state = {
      open: false,
    };
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleOpen() {
    this.setState({ open: true });
  };

  handleClose() {
    this.setState({ open: false });
  };

  renderOpenModalButton() {
    return (
      <Button onClick={this.handleOpen}>Read Cards Via Webcam</Button>
    );
  }

  render() {
    return (
      <>
        <Modal
          open={this.state.open}
          onClose={this.handleClose}
          trigger={this.renderOpenModalButton()}
        >
          <Modal.Content>
            <StreamOutput />
          </Modal.Content>
        </Modal>
      </>
    )
  }
}