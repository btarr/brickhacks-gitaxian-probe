import React from 'react';
import { Card } from 'semantic-ui-react'
export default function CardInfoCard({ cardInfo }) {
  return (
    <Card header={cardInfo.get('name')} description={cardInfo.get('price')} />
  )
}