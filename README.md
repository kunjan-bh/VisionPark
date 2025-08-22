# VisionPark

## Project Description
VisionPark is an **online parking space booking system** designed to simplify parking management. The system integrates several advanced features:

- **OCR-based License Verification:** Automatically verifies vehicle licenses upon parking using Optical Character Recognition.  
- **Chatbot Interface:** Built using RAG (Retrieval-Augmented Generation) to assist users with queries and support during booking.  

## Note on Chatbot Libraries
The chatbot's library folders (e.g., large dependencies like Torch) are **not included in the repository** because they exceed GitHub’s file size limits. Users need to install these dependencies separately as required.

## Running the Project
1. Switch to the `registration` branch.  
2. Activate the virtual environment if needed.  
3. Run the Django server using:  
   ```bash
   python manage.py runserver
