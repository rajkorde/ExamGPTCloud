import React, { useState } from 'react';

import Message from './Message';

const Form = () => {

  const stage = process.env.REACT_APP_STAGE;
  const backendUrl = `${process.env.REACT_APP_BACKEND_URL}/${stage}/create_exam`;
  const [examName, setExamName] = useState("");
  const [email, setEmail] = useState("");
  const [filename, setFilename] = useState(null);
  const [examCode, setExamCode] = useState("");
  const [message, setMessage] = useState("");
  const [fontClass, setFontClass] = useState("text-dark");

  const uploadFileToS3 = async (apiUrl, fields) => {
    const formData = new FormData();
    for (const key in fields) {
      formData.append(key, fields[key]);
    }
    formData.append("file", filename);

    try {
      const response = await fetch(apiUrl, { method: "POST", body: formData })

      if (response.ok) {
        setMessage("File uploaded.");
        setFontClass("text-muted");
        return true;
      } else {
        setMessage("File upload failed!");
        setFontClass("text-danger");
        return false;
      }

    } catch (error) {
      console.error("File upload error:" + error);
      setMessage("File upload failed!");
      setFontClass("text-danger");
      return false;
    }
  }

  const handleSubmit = async (event) => {
    setMessage("Processing...")
    setFontClass("text-muted");

    if (!examName) {
      setMessage("Please enter an exam name!");
      setFontClass("text-danger");
      return
    }
    if (!email) {
      setMessage("Please enter an email!");
      setFontClass("text-danger");
      return
    }
    if (!filename) {
      setMessage("Please choose a file!");
      setFontClass("text-danger");
      return
    }

    const requestBody = JSON.stringify({
      exam_name: examName,
      filenames: [filename.name],
      email: email,
      ...(examCode != null && { exam_code: examCode })
    });

    try {
      const response = await fetch(backendUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: requestBody,
        mode: "cors",
      });

      if (!response.ok) {
        throw new Error("Form submission failed!");
      }

      const data = await response.json();
      const apiUrl = data.urls[0].api_url;
      const fields = data.urls[0].fields;
      console.log("Exam code: ", data.exam_code);

      setMessage("Exam created. Please wait...");
      setFontClass("text-muted");

      const result = await uploadFileToS3(apiUrl, fields);

      if (result) {
        console.log("Success!");
        const msg = "Your study material has been successfully submitted! Your exam code is <span class='fw-bold'>" + data.exam_code + "</span>. " +
          "You will receive an email shortly once your study material is processed. " +
          "The email will guide you through downloading the Telegram app and starting your practice with the bot. Happy studying!";
        setMessage(msg);
        setFontClass("alert alert-success");
      } else {
        console.error("Form submission failed!");
        setMessage("Form submission failed!");
        setFontClass("text-danger");
      }

    } catch (error) {
      console.error("Form submission failed " + error);
      setMessage("Form submission failed!");
      setFontClass("text-danger");
    }
  }

  return (
    <>
      <div className="row justify-content-center">
        <div className="col-10 col-md-10 col-lg-8 text-center mt-3">
          <p style={{ textAlign: "justify" }}>Simplify your exam prep with AI. Upload your study material and let <span className="fw-bold text-primary">ExamGPT</span> transform it into flashcards and practice multiple-choice questions.
            Once the study material is processed, you'll get an email letting you know that you're ready to start practicing for your exam using our Telegram bot with
            personalized flashcards and quizzes. <span className="fw-bold text-primary">ExamGPT</span> helps you study smarter, not harder!</p>
        </div>
      </div>
      <div className="row justify-content-center">
        <div className="col-10 col-md-8 col-lg-6 text-start">
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
            <input type="file" className="form-control" id="filename" accept=".pdf" onChange={(e) => setFilename(e.target.files[0])} required />
            <div id="filenameHelp" className="form-text">
              Only single pdf file uploads are supported at this point.
            </div>
          </div>
          {/* <div className="mb-3">
            <label htmlFor="examCode" className="form-label fs-6 fw-bold">Exam code (optional)</label>
            <input type="text" className="form-control" id="examCode" value={examCode} onChange={(e) => setExamCode(e.target.value)} />
          </div> */}
          <button type="button" onClick={handleSubmit} className="btn btn-primary">Submit</button>
          <div className="row">
            <Message message={message} fontClass={fontClass} />
          </div>
        </div>
      </div>
    </>
  );
}

export default Form;

