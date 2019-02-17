import React, {PureComponent} from 'react';
import { Grid, Header } from 'semantic-ui-react'
import CaptureVideoButton from './CaptureVideoButton';
import CardInfoCard from './CardInfoCard';
import { fromJS } from 'immutable';

export default class TradingGrid extends PureComponent {
  constructor() {
    super();
    this.state = {
      yourCards: fromJS([]),
      theirCards: fromJS([])
    }
    this.handleAddYourCard = this.handleAddYourCard.bind(this);
    this.handleAddTheirCard = this.handleAddTheirCard.bind(this);
    this.handleRemoveYourCard = this.handleRemoveYourCard.bind(this);
    this.handleRemoveTheirCard = this.handleRemoveTheirCard.bind(this);
  }

  handleAddYourCard(cards) {
    this.setState({
      yourCards: this.state.yourCards.concat(cards)
    })
  }

  handleAddTheirCard(cards) {
    this.setState({
      theirCards: this.state.theirCards.concat(cards)
    })
  }

  handleRemoveYourCard(cardName) {
    this.setState({
      yourCards: this.state.yourCards.filterNot(card => card.get('name') === cardName)
    })
  }

  handleRemoveTheirCard(cardName) {
    this.setState({
      theirCards: this.state.theirCards.filterNot(card => card.get('name') === cardName)
    })
  }

  renderCard(cardInfo) {
    return (
      <div key={cardInfo.get('name')}>
        <Grid.Row>
          <CardInfoCard cardInfo={cardInfo} />
        </Grid.Row>
      </div>
    )
  }

  renderCards(cardsSource) {
    return cardsSource.map(this.renderCard);
  }

  renderTotalRow(total) {
    return (
      <Header as="h3"> Total: {total} </Header>
    )
  }

  renderColumn(header, cardsSource, handleAdd) {
    return (
      <Grid.Column>
        <Grid.Row>
          <Header>{header}</Header>
        </Grid.Row>
        {this.renderTotalRow()}
        {this.renderCards(cardsSource)}
        <Grid.Row>
          <CaptureVideoButton onSubmit={handleAdd} />
        </Grid.Row>
      </Grid.Column>
    );
  }

  render() {
    return (
      <Grid columns={2} divided={true} centered={true} >
        {this.renderColumn('Your Cards', this.state.yourCards, this.handleAddYourCard)}
        {this.renderColumn('Their Cards', this.state.theirCards, this.handleAddTheirCard)}
      </Grid>
    );
  }
}