import axios from "axios";
import { ChangeEvent, FormEvent, useState } from "react";

function FileUploadSingle() {
  const [file, setFile] = useState<File>();

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

    e.preventDefault();
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
    });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>React File Upload</h1>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default FileUploadSingle;
