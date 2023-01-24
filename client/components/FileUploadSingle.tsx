import axios from 'axios'
import { ChangeEvent, FormEvent, useState } from 'react'
import { useForm, SubmitHandler } from 'react-hook-form'

// Types
type Inputs = {
  ico: string
  file: FileList
}

// Props
type FileUploadProps = {
  // Callback function to set state of uploadedFile object in parent component
  onSuccesfullUpload: (fileName: string) => void
}

// Component
const FileUploadSingle = (props: FileUploadProps) => {
  // State
  const [uploadStatus, setUploadStatus] = useState(false)
  const [uploadStatusMessage, setUploadStatusMessage] = useState('')
  const [errorMessage, setErrorMessage] = useState('')

  // Form handler
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset,
  } = useForm<Inputs>()

  // File handler
  const onSubmit: SubmitHandler<Inputs> = (data) => {
    // Axios post request to backend
    const formData = new FormData()
    formData.append('file', data.file[0])
    formData.append('fileName', data.file[0].name)
    formData.append('ico', data.ico)

    // Set upload status and message
    setUploadStatus(true)
    setUploadStatusMessage('Uploading...')

    // Axios post request
    const url = 'http://localhost:8000/api/file'
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    }

    axios
      .post(url, formData, config)
      .then((response: any) => {
        console.log(response.data)
        console.log(response.status)

        if (response.status === 201) {
          setUploadStatusMessage(response.data.message)
          setUploadStatus(false)

          // Set state of uploadedFile object in parent component
          props.onSuccesfullUpload(response.data.filename)

          // Reset form
          reset()
        }
      })
      .catch((error: any) => {
        console.log(error.response)
        setUploadStatus(false)
        setErrorMessage(error.response.data.message)
      })
  }

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="input-group mb-6">
          <label htmlFor="ico">IČO</label>
          <input
            type="text"
            placeholder="2090601"
            {...(register('ico', {required: true, maxLength: 20 }))}
          />
          {errors.ico && <p className="text-red-500">This field is required</p>}
        </div>

        <div className="input-group mb-6">
          <label htmlFor="file">Upload your file...</label>
          <input type="file" {...(register('file', {required: true}))} />
          {errors.file && <p className="text-red-500">This field is required</p>}
        </div>

        <div className="container mt-3 text-right">
          <button type="submit" className="btn btn-purple group">
            <span className="relative rounded-md bg-white px-5 py-2.5 transition-all duration-75 ease-in group-hover:bg-opacity-0">
              Upload
            </span>
          </button>
        </div>

        {errorMessage.length > 0 && (
          <div className="mt-6">
            <p className="text-red-500">{errorMessage}</p>
          </div>
        )}
        {uploadStatus && <p>{uploadStatusMessage}</p>}
      </form>
    </div>
  )
}

export default FileUploadSingle
