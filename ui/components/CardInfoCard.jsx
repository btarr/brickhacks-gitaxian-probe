import React from 'react';
import { Card, Button } from 'semantic-ui-react'

const renderRemoveButton = (onRemove, cardName) => {
  return (
    <Button
      onClick={() => onRemove(cardName)}
    >
      Remove from Trade
    </Button>
  )
}

export default function CardInfoCard({ cardInfo, onRemove }) {
  const cardName = cardInfo.get('name');
  return (
    <Card header={cardName} description={`$${cardInfo.get('price')}`} extra={renderRemoveButton(onRemove, cardName)}/>
  )
}