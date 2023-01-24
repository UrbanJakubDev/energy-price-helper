import React from 'react'

type Props = {
  label: string
  onBtnClick: () => void
}

const Button = (props: Props) => {
   // Object destructuring
   const { label, onBtnClick } = props

  return (
    <button onClick={onBtnClick} className="btn btn-purple group">
      <span className="btn-label">{label}</span>
    </button>
  )
}

export default Button
