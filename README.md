# ExamGPTCloud

## 1. Project Overview

ExamGPT helps users prepare for their exams by automatically generating flashcards and multiple-choice questions from their study materials (eg. PDF files). Studying techniques like [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) and [Retreival learning](https://ctl.wustl.edu/resources/using-retrieval-practice-to-increase-student-learning/) are common among students and creating high quality flash cards is a key component of these learning methods. There are software solutions like Anki and Quizlet that let students use flash cards effectively, but creating these flash cards is a time consuming process. This project attempts to solve that problem using AI.

In ExamGPT, users goto a [website](https://myexamgpt.com/) and upload the their study material and get an exam code. Once ExamGPT is done processing the study material, it sends the user an email signalling completion and detailing next steps. Then the user can download [Telegram](https://telegram.org/) and practice using flashcards and multiple choice quizzes using their exam code and the ExamGPT telegram bot.

The infrastructure is implemented using AWS. The frontend is a simple React App hosted as a static S3 website. The backend is fully serverless and easily scalable and uses a number of AWS services.

## 3. System Architecture

_Talk about software architecture: Hexagonal Architecture as well_

_Note: Replace the link with the actual diagram link._

## 4. Components

### 4.1 Frontend

- Technology: React.js
- Hosting: AWS S3 (Static Website Hosting)
- Features:
  - User input form for Exam Name, Email, and PDF upload.
  - Displays exam_code after submission.
  - Handles file upload to S3 via pre-signed URL.

### 4.2 Backend

- AWS Lambda Functions
  - create_exam:
    - Generates a unique exam_code.
    - Stores exam details in ExamTable (DynamoDB).
    - Generates a pre-signed S3 URL.
  - Chunker:
    - Triggered by S3 put object event.
    - Chunks PDF into smaller parts.
    - Stores chunks in ChunkTable (DynamoDB).
    - Publishes SNS messages to ChunkTopic.
  - Generate:
    - Subscribed to ChunkTopic.
    - Generates flashcards and MCQs for each chunk.
    - Stores data in QATable (DynamoDB).
    - For the last batch, publishes to ValidateTopic.
  - Validate:
    - Subscribed to ValidateTopic.
    - Verifies all chunks are processed.
    - Sends completion email via SES.
  - ChatServer:
    - Handles Telegram bot interactions.
    - Stores chat state in S3.
    - Supports u\* ser commands for exam registration and practice sessions.
- AWS Services
  - API Gateway: Routes HTTP requests to Lambda functions.
  - SSM Parameter Store: Config management for app (Secrets, Config, Runtime Environment etc)
  - DynamoDB Tables:
    - ExamTable: Stores exam metadata.
    - ChunkTable: Stores chunk information.
    - QATable: Stores generated flashcards and MCQs.
- Amazon S3: Stores uploaded PDFs and chat states.
- Amazon SNS (Simple Notification Service):
  - Topics: ChunkTopic, ValidateTopic.
  - Facilitates communication between Lambdas.
- Amazon SES (Simple Email Service):
  Sends emails to users upon exam readiness.

### 4.3 Third-Party Services

- Telegram Bot:
  - Provides an interactive interface for users to practice.
  - Communicates with ChatServer via API Gateway.

## 5. Data Flow

1. User Submission:

   - User inputs Exam Name, Email, and uploads PDF.
   - Frontend sends data to create_exam via API Gateway.

2. Exam Creation:
   - create_exam generates exam_code, stores details, and provides a pre-signed URL.
   - Frontend uploads PDF to S3 using the pre-signed URL.
3. PDF Processing:
   - S3 triggers Chunker upon file upload.
   - Chunker splits PDF into chunks, stores them, and notifies ChunkTopic.
4. Content Generation:
   - Generate Lambdas process each chunk batch from ChunkTopic.
   - Generates flashcards and MCQs, storing them in QATable.
   - Last Generate Lambda publishes to ValidateTopic.
5. Validation and Notification:
   - Validate Lambda ensures all content is generated.
   - Sends an email to the user via SES.
6. User Practice:
   - User receives email instructions.
   - Downloads Telegram and interacts with the ExamGPT bot.
   - Bot requests are routed to ChatServer via API Gateway.

## 6. Detailed Component Specifications

### 6.1 Frontend

- User Interface:
  - Responsive design for accessibility.
  - Form fields: Exam Name (text), Email (email), PDF Upload (file).
- Functionality:
  - Validates user input before submission.
  - Handles pre-signed URL response and uploads file to S3.
  - Displays exam_code for user reference.

### 6.2 Lambda Functions

- **create_exam**
  - Inputs: Exam Name, Email.
  - Processes:
    Generate unique exam_code (e.g., UUID).
  - Store exam details in ExamTable:
    exam_code, exam_name, email, status.
    Generate pre-signed S3 URL for PDF upload.
  - Outputs:
    Return exam_code and pre-signed URL to frontend.
- **Chunker**
  - Trigger: S3 put event on PDF upload bucket.
  - Processes:
    - Retrieve PDF from S3.
    - Split PDF into manageable chunks (e.g., pages or sections).
    - Store each chunk in ChunkTable with chunk_id and exam_code.
    - Publish messages to ChunkTopic with batch of chunk_ids and exam_code.
- **Generate**
  - Subscription: ChunkTopic.
  - Processes:
    - For each batch, retrieve chunks from ChunkTable.
    - Generate flashcards and MCQs using NLP techniques.
    - Store generated content in QATable:
      - exam_code, chunk_id, flashcards, mcqs.
  - Completion:
    - The last Generate Lambda publishes to ValidateTopic.
- **Validate**
  - Subscription: ValidateTopic.
  - Processes:
    - Confirm all chunks have been processed.
    - Cross-verify entries in QATable against ChunkTable.
    - Update ExamTable status to 'Ready'.
    - Send notification email via SES.
- **ChatServer**
  Trigger: API Gateway (HTTP requests from Telegram bot).
  - Processes:
    - Authenticate and map users via exam_code.
      Handle commands:
      - /register [exam_code]
      - /practice_flashcards
      - /take_quiz
    - Fetch relevant data from QATable.
    - Store user session states in S3.

## 7. Data Models

### 7.1 ExamTable (DynamoDB)

Primary Key: exam_code (String)
Attributes:
exam_name: String
email: String
status: String (e.g., 'Processing', 'Ready')

### 7.2 ChunkTable (DynamoDB)

Primary Key: chunk_id (String)
Sort Key: exam_code (String)
Attributes:
chunk_data: Binary or Text
processed: Boolean

### 7.3 QATable (DynamoDB)

Primary Key: qa_id (String)
Attributes:
exam_code: String
chunk_id: String
flashcards: List
mcqs: List

## 8. API Specifications

### 8.1 Endpoints

- POST /create_exam

  - Description: Initiates exam creation.
  - Request body:

  ```code
      {
          "exam_name": "string",
          "email": "string"
      }
  ```

  - Response body:
    ```code
    {
        "exam_code": "string",
        "upload_url": "string"
    }
    ```

- POST /chat

  - Description: Handles Telegram bot webhooks.
  - Request Body: Telegram's message format.
  - Response: Depends on bot interaction.

## 9. Security Considerations

Data Protection:
Use HTTPS for all API communications.
Encrypt sensitive data at rest and in transit.
Access Control:
Implement IAM roles with the least privilege principle.
Pre-signed URLs expire after a short duration.
User Privacy:
Comply with data protection regulations.
Provide options for users to delete their data.

## 10. Deployment

Frontend:
Build React app and deploy to S3 bucket configured for static website hosting.
Backend:
Deploy Lambda functions via AWS SAM or Serverless Framework.
Set up API Gateway routes and integrations.
Configure DynamoDB tables and indexes.
Set up SNS topics and subscriptions.
Configure SES for verified email sending.
Environment Configuration:
Use AWS Parameter Store or Secrets Manager for sensitive configurations.

## 11. Risks and Mitigations

- Risk: Delays in email delivery via SES.

  - Mitigation: Monitor SES send rates and handle retries.

- Risk: High volume of users may cause Lambda throttling.

  - Mitigation: Request AWS for higher concurrency limits.
