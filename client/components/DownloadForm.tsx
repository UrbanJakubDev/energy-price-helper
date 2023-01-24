interface Props {
  fileName: string
  label: string
  description: string
}

const DownloadForm = ({ fileName, label, description }: Props) => {
  // Function will execute on click of button
  const onButtonClick = () => {
    // using Java Script method to get PDF file
    fetch(fileName).then((response) => {
      response.blob().then((blob) => {
        // Creating new object of PDF file
        const fileURL = window.URL.createObjectURL(blob)
        // Setting various property values
        let alink = document.createElement('a')
        alink.href = fileURL
        alink.download = fileName
        alink.click()
      })
    })
  }
  return (
    <div className="container mt-3 flex content-end justify-between text-right">
      <div>{description}</div>
      <button onClick={onButtonClick} className="btn btn-purple group">
        <span className="btn-label">{label}</span>
      </button>
    </div>
  )
}

export default DownloadForm
