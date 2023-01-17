import axios from "axios";
import { ChangeEvent, FormEvent, useState } from "react";

function FileUploadSingle() {
  const [file, setFile] = useState<File>()
  const [flash, setFlash] = useState<String>('message')

  // File change hander
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  // Upload file handler
  const handleSubmit = (e: FormEvent) => {
    if (!file) {
      return;
    }

    e.preventDefault()
    const url = "http://localhost:8000/api/file";
    const formData = new FormData();
    formData.append("file", file);
    formData.append("fileName", file.name);
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    axios.post(url, formData, config).then((response) => {
      console.log(response.data);
      if (response.status === 201){
        setFlash(response.data.message)
      }
    });
  };

  return (
    <div>
      <p>{flash}</p>
      <form onSubmit={handleSubmit}>

        <label htmlFor="file_input">Upload file</label>
        <input
          onChange={handleFileChange}
          className="fileInput"
          aria-describedby="file_input_help"
          id="file_input"
          type="file"
          
        />

        <p
          className="mt-1 text-sm text-gray-500 dark:text-gray-300"
          id="file_input_help"
        >
          .XLSX file.
        </p>


        <div className="text-right">
          <button type="submit" className="group btn btn-purple">
            <span className="btn-label">
              Submit form
            </span>
          </button>
        </div>
      </form>
    </div>
  );
}

export default FileUploadSingle;
