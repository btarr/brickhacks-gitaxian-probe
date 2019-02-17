import React, { PureComponent } from 'react';
import { Button, Modal } from 'semantic-ui-react'
import StreamOutput from "./StreamOutput";

export default class CaptureVideoButton extends PureComponent {
  constructor() {
    super()
    this.state = {
      open: false,
    };
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(submitData) {
    this.props.onSubmit(submitData)
    this.handleClose();
  }

  handleOpen() {
    this.setState({ open: true });
  };

  handleClose() {
    this.setState({ open: false });
  };

  renderOpenModalButton() {
    return (
      <Button primary={true} onClick={this.handleOpen}>Read Cards Via Webcam</Button>
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
            <StreamOutput onSubmit={this.handleSubmit} />
          </Modal.Content>
        </Modal>
      </>
    )
  }
}