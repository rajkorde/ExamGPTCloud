import React, { useState } from 'react';

import Message from './Message';

const Form = () => {

  const [examName, setExamName] = useState("");
  const [email, setEmail] = useState("");
  const [filename, setFilename] = useState(null);
  const [examCode, setExamCode] = useState("");
  const [message, setMessage] = useState("");
  const [fontClass, setFontClass] = useState("text-dark");

  const handleSubmit = (event) => {
    setMessage("")
    setFontClass("text-dark");
    if (!examName) {
      setMessage("Please enter an exam name");
      setFontClass("text-danger");
      return
    }
    if (!email) {
      setMessage("Please enter an email");
      setFontClass("text-danger");
      return
    }
    if (!filename) {
      setMessage("Please choose a file");
      setFontClass("text-danger");
      return
    }

    console.log(examName, email, filename, examCode)

  }

  return (
    <>
      <div className="row">
        <div className="col-2" />
        <div className="col-8 text-center mt-3">
          <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Tempore temporibus enim, in sequi nobis excepturi dignissimos laborum nostrum repudiandae totam numquam animi labore, suscipit, corporis consequatur pariatur vitae officia fugiat.</p>
        </div>
        <div className="col-2" />
      </div>
      <div className="row">
        <div className="col-4" />
        <div className="col-4 text-start">
          <div className="mb-3">
            <label htmlFor="examName" className="form-label fs-6 fw-bold">Exam name</label>
            <input type="text" className="form-control" id="examName" value={examName} onChange={(e) => setExamName(e.target.value)} placeholder="AWS Solution Architect Associate Certification" required />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label fs-6 fw-bold">Email</label>
            <input type="email" className="form-control" id="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@email.com" required />
          </div>
          <div className="mb-3">
            <label htmlFor="filename" className="form-label fs-6 fw-bold">Upload the study material</label>
            <input type="file" className="form-control" id="filename" accept=".pdf" onChange={(e) => setFilename(e.target.value)} required />
            <div id="filenameHelp" className="form-text">
              Only single pdf file uploads are supported at this point.
            </div>
          </div>
          <div className="mb-3">
            <label htmlFor="examCode" className="form-label fs-6 fw-bold">Exam code (optional)</label>
            <input type="text" className="form-control" id="examCode" value={examCode} onChange={(e) => setExamCode(e.target.value)} />
          </div>
          <button type="button" onClick={handleSubmit} className="btn btn-primary">Submit</button>
          <div className="row">
            <Message message={message} fontClass={fontClass} />
          </div>
        </div>
        <div className="col-4" />
      </div>
    </>
  );
}

export default Form;

