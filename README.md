# ExamGPTCloud

## 1. Project Overview

ExamGPT is a software solution designed to help users prepare for their exams by automatically generating flashcards and multiple-choice questions from their study materials (PDF files). The platform comprises a React-based frontend website and a serverless backend infrastructure on AWS. Users can upload their study materials, receive an exam_code, and practice using a Telegram bot that interfaces with the generated content.

## 2. Objectives

Automate Study Material Processing: Convert user-uploaded PDFs into digestible study aids.
Provide Interactive Learning: Enable users to practice flashcards and take quizzes via Telegram.
Ensure Scalability and Reliability: Utilize AWS services to handle varying loads and ensure uptime.
Maintain Security and Privacy: Protect user data throughout the process.

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

### 7. Data Models

7.1 ExamTable (DynamoDB)
Primary Key: exam_code (String)
Attributes:
exam_name: String
email: String
status: String (e.g., 'Processing', 'Ready')
7.2 ChunkTable (DynamoDB)
Primary Key: chunk_id (String)
Sort Key: exam_code (String)
Attributes:
chunk_data: Binary or Text
processed: Boolean
7.3 QATable (DynamoDB)
Primary Key: qa_id (String)
Attributes:
exam_code: String
chunk_id: String
flashcards: List
mcqs: List 9. API Specifications
8.1 Endpoints
POST /create_exam

Description: Initiates exam creation.
Request Body:
json
Copy code
{
"exam_name": "string",
"email": "string"
}
Response:
json
Copy code
{
"exam_code": "string",
"upload_url": "string"
}
POST /chat

Description: Handles Telegram bot webhooks.
Request Body: Telegram's message format.
Response: Depends on bot interaction.
8.2 Security
Authentication:
API Gateway should implement API keys or IAM roles as needed.
Validation:
All inputs should be sanitized and validated. 9. Security Considerations
Data Protection:
Use HTTPS for all API communications.
Encrypt sensitive data at rest and in transit.
Access Control:
Implement IAM roles with the least privilege principle.
Pre-signed URLs expire after a short duration.
User Privacy:
Comply with data protection regulations.
Provide options for users to delete their data. 10. Deployment
Frontend:
Build React app and deploy to S3 bucket configured for static website hosting.
Backend:
Deploy Lambda functions via AWS SAM or Serverless Framework.
Set up API Gateway routes and integrations.
Configure DynamoDB tables and indexes.
Set up SNS topics and subscriptions.
Configure SES for verified email sending.
Environment Configuration:
Use AWS Parameter Store or Secrets Manager for sensitive configurations. 11. Testing
Unit Tests:
Write tests for each Lambda function using frameworks like Jest or Mocha.
Integration Tests:
Test interactions between components (e.g., Lambda triggering SNS).
End-to-End Tests:
Simulate user flows from frontend submission to Telegram bot interaction.
Load Testing:
Use tools like Artillery or JMeter to simulate high traffic. 12. Monitoring and Logging
AWS CloudWatch:
Monitor Lambda executions, API Gateway access logs, and errors.
Alerts:
Set up CloudWatch alarms for failures or performance thresholds.
Logging:
Implement structured logging within Lambda functions. 13. Scalability and Performance
Serverless Architecture:
Leverage AWS Lambda's auto-scaling capabilities.
Optimizations:
Optimize Lambda function memory and timeout settings.
Use efficient algorithms for PDF chunking and content generation.
Caching:
Consider caching frequent reads from DynamoDB if necessary. 14. Future Enhancements
Multi-language Support:
Extend content generation to support multiple languages.
Analytics Dashboard:
Provide users with insights into their practice sessions.
Additional Integrations:
Expand to other messaging platforms like WhatsApp or Slack.
AI Improvements:
Implement advanced NLP models for better content generation. 15. Project Timeline
Week 1-2: Set up the project environment, AWS services, and initial frontend.
Week 3-4: Develop Lambda functions (create_exam, Chunker).
Week 5-6: Implement Generate and Validate Lambdas.
Week 7: Integrate Telegram bot and ChatServer Lambda.
Week 8: Testing and debugging.
Week 9: Deployment and final optimizations.
Week 10: Documentation and project handover. 16. Documentation
Code Documentation:
Comment code and provide README files for repositories.
User Guides:
Create guides for users on how to use the platform.
Developer Guides:
Provide setup instructions and contribution guidelines for developers. 17. Risks and Mitigations
Risk: High volume of users may cause Lambda throttling.
Mitigation: Request AWS for higher concurrency limits.
Risk: Delays in email delivery via SES.
Mitigation: Monitor SES send rates and handle retries. 18. Conclusion
This specification outlines the development plan for ExamGPT, detailing each component and its role in the system. By leveraging AWS's serverless services and integrating with popular platforms like Telegram, ExamGPT aims to provide an efficient and scalable solution for exam preparation.
