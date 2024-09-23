# ExamGPTCloud

## 1. Project Overview

ExamGPT helps users prepare for their exams by automatically generating flashcards and multiple-choice questions from their study materials (eg. PDF files). Studying techniques like [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) and [Retreival learning](https://ctl.wustl.edu/resources/using-retrieval-practice-to-increase-student-learning/) are common among students and creating high quality flash cards is a key component of these learning methods. There are software solutions like Anki and Quizlet that let students use flash cards effectively, but creating these flash cards is a time consuming process. This project attempts to solve that problem using AI.

In ExamGPT, users goto a [website](https://myexamgpt.com/) and upload the their study material and get an exam code. Once ExamGPT is done processing the study material, it sends the user an email signalling completion and detailing next steps. Then the user can download [Telegram](https://telegram.org/) and practice using flashcards and multiple choice questions (MCQs) using their exam code and the ExamGPT telegram bot.

The infrastructure is implemented using AWS. The frontend is a simple React App hosted as a static S3 website. The backend is fully serverless and easily scalable and uses a number of AWS services.

## 3. System Architecture

_Talk about software architecture: Hexagonal Architecture as well_

_Note: Replace the link with the actual diagram link._

## 4. Components

### 4.1 Frontend

- Technology: React.js, Bootstrap
- Requirements: Works on all mobile, tablets and desktop.
- Hosting: AWS S3 (Static Website Hosting)
- Features:
  - Inform the user User about ExamGPT.
  - Get input form for Exam Name, Email, and PDF upload and send to backend.
  - Upload Study material (refered to PDF file from here on) to pre-signed URL provided by backend.
  - Displays exam_code after submission and show next steps.

### 4.2 Backend

- AWS Lambda Functions

  - create_exam:
    - Creates the initial Exam and pre-signed URL
    - Trigger: /create_exam in API Gateway
    - Inputs: Exam Name, Email, pdf File location
    - Functionality:
      - Creates an Exam object with a unique exam_code
      - Stores Exam object with all exam details in ExamTable (DynamoDB).
      - Generates a pre-signed S3 URL and sends it (and exam_code) to frontend.
    - Notes:
      - Uses pre-signed S3 URL because direct upload through API gateway has a limit of 10 MB. Upload using pre-signed S3 URL is 5 GB.
  - chunker:
    - Chunks pdf files into small chunks and triggers a series of generate lambdas that will create flashcards and multiple choices questions (refered to QA henceforth) for each of the chunks
    - Trigger: S3 ObjectCreated event.
    - Inputs: bucket_name, location (of the object), exam_code (extracted from object path)
    - Functionality:
      - Downloads study material from S3
      - Chunks PDF into smaller parts.
      - Stores chunks in ChunkTable (DynamoDB).
      - Creates ExamTracker object and saves in WorkTrackerTable (DynamoDB). This table is used for handling race conditions when various generate lambdas finish.
      - Updates Exam state to CHUNKED.
      - Breaks list of chunks in batches of CHUNK_BATCH_SIZE and publishes one SNS messages to ChunkTopic for each batch.
    - Notes:
      - Since spinning up a new lambda for each chunk would be slow and spinning up only a single lambda would not be practical (because of 15 minute execution limits of AWS lambdas), a batching approach is used. Each generate lambda would handle a batch of chunks.
      - To ensure that we can track the completion of all of the generate lamdbas, a work tracker table is used that tracks the completion of each generate lambda.
  - generate:

    - Generate a set of QA (flash cards and multiple choices) for a batch of chunks using AI.
    - Trigger: Subscribed to SNS ChunkTopic
    - Inputs: list of chunk_ids (indicating the batch), exam_code, last_chunk (indicating whether this is the last batch of chunks)
    - Functionality:

      - Get all chunk objects and exam object from DynamoDB tables (ExamTable and ChunkTable)
      - Get model keys from SSM
      - Generates flashcards and MCQs for each chunk.
      - For each chunk that generates at least one Flashcard or MCQ, sets the appropriate flags in the ChunkTable
      - Stores all Flashcards and MCQs in QATable (DynamoDB).
      - Once it is done with the work, updates the completed_worker count in WorkTrackerTable.
      - If its the last batch, publishes SNS message to ValidateTopic.

    - Notes:
      - The AI model first checks if the chunk has enough content to generate a flashcard or MCQ. Sometimes the chunk is mainly comprised on Table of Contents or copyright notices etc, so this is skipped

  - validate:

    - Validates that QA has been generated correctly for an exam. Publishes some stats on the QA generation.
    - Trigger: Subscribed to SNS ValidateTopic
    - Input: exam_code
    - Functionality
      - Gets Exam object from ExamTable (DynamoDB).
      - Waits for all generate lambdas to finish using the WorkTrackerTable (or times out).
      - Gets Chunks and QAs from DynamoDB and publishes stats on processing of the exam.
      - If most of the chunks are processed (controlled by CHUNK_PROCESSED_RATIO), considers the QA generation as complete.
      - If QA generation is complete, sends completion email to user via SES.

  - chat_server:
    - Handles Telegram bot interactions.
    - Trigger: /chat in API gateway
    - Functionality:
      - Gets telegram bot token from SSM
      - Loads chat state from S3
      - Initializes Telegram bot application with persistence initialized with chat state
      - Processes the message using CommandHandlers and ConversationHandlers
      - Saves chat state back to S3
    - Notes:
      - Chat state is stored in pickle format.

- Other AWS Services
  - API Gateway: Routes HTTP requests to Lambda functions.
  - SSM Parameter Store: Config management for app (Secrets, Config, Runtime Environment etc)
  - DynamoDB Tables:
    - ExamTable: Stores exam metadata.
    - ChunkTable: Stores chunk information.
    - QATable: Stores generated flashcards and MCQs.
    - WorkTrackerTable: Stores generate lamdbas state
- Amazon S3:
  - Stores uploaded PDFs (ContentBucket).
  - Stores the telegram chat state (ChatBucket).
  - Hosts the react frontend app (Domain Name).
- Amazon SNS (Simple Notification Service):
  - Topics: ChunkTopic, ValidateTopic.
  - Facilitates communication between Lambdas.
- Amazon SES (Simple Email Service):
  - Sends emails to users upon exam readiness.

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
