import React, {PureComponent} from 'react';
import { Grid, Header } from 'semantic-ui-react'
import CaptureVideoButton from './CaptureVideoButton';
import CardInfoCard from './CardInfoCard';
import { fromJS } from 'immutable';

export default class TradingGrid extends PureComponent {
  constructor() {
    super();
    this.state = {
      yourCards: fromJS([ { name: 'test'}, {value : '$200'} ]),
      theirCards: fromJS([])
    }
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

  renderColumn(header, cardsSource) {
    return (
      <Grid.Column>
        <Grid.Row>
          <Header>{header}</Header>
        </Grid.Row>
        {this.renderTotalRow()}
        {this.renderCards(cardsSource)}
        <Grid.Row>
          <CaptureVideoButton />
        </Grid.Row>
      </Grid.Column>
    );
  }

  render() {
    return (
      <Grid columns={2} divided={true} centered={true} >
        {this.renderColumn('Your Cards', this.state.yourCards)}
        {this.renderColumn('Their Cards', this.state.theirCards)}
      </Grid>
    );
  }
}