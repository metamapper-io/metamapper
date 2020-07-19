import React from "react"
import EnumDisplay from "./EnumDisplay"
import TextDisplay from "./TextDisplay"
import UserDisplay from "./UserDisplay"

export const renderDisplay = (customField, fieldValue) => {
  if (!customField || !fieldValue) return null

  const switchBoard = {
    TEXT: TextDisplay,
    ENUM: EnumDisplay,
    USER: UserDisplay,
  }

  const Component = switchBoard[customField.fieldType]

  return (
    <span data-test={`CustomProperties.Display(${customField.pk})`}>
        <Component value={fieldValue} {...customField} />
    </span>
  )
}
