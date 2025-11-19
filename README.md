# Smart Notes API - worst app ever

This is a fully functional REST API for a "Smart Notes" application, built with Python and FastAPI. The API provides standard **CRUD** (Create, Read, Update, Delete) operations for managing notes.

Its core "smart" feature is an AI-powered endpoint that, given a specific note, can find and return the most semantically related notes. This was achieved using **Word Embeddings** from a pre-trained Sentence-Transformers model, which was available in the pre-configured Anaconda environment.

The entire development process was version-controlled using **Git**, and the project adheres to software engineering best practices like the **Single Responsibility Principle (SOLID)** and includes **automated unit tests** with Pytest.

**Key Technologies:**

- **Language:** Python 3.11
- **Framework:** FastAPI
- **AI/ML:** Sentence-Transformers (leveraging a base Anaconda environment)
- **Testing:** Pytest
- **Version Control:** Git & GitHub
- **IDE:** Visual Studio Code
- **Environment:** Anaconda `(base)`

---

### How to Run the Project (Efficient Anaconda Workflow)

This project leverages the power of a pre-existing Anaconda `(base)` environment, which often already includes heavy AI/ML libraries.

1.  **Open the Project in VS Code:**

    - Open the `smart-notes-api` folder directly in Visual Studio Code.

2.  **Select the Python Interpreter:**

    - Open the Command Palette (`Ctrl+Shift+P`).
    - Search for and select **"Python: Select Interpreter"**.
    - Choose your **Anaconda `(base)`** environment. VS Code will now use this environment for all operations.

3.  **Install Project-Specific Dependencies:**

    - Open the integrated terminal in VS Code (`Ctrl+` \` ``). The terminal will automatically use the selected `(base)` environment.
    - The `base` environment may already contain `torch` and `sentence-transformers`. You only need to install the packages specific to this project:
      ```bash
      pip install "fastapi[all]" pytest
      ```

4.  **Start the Server:**

    - In the same integrated terminal, run the Uvicorn server:
      ```bash
      uvicorn main:app --reload
      ```

5.  **Access the API:**
    - The server is now running. You can access the interactive documentation (and test all endpoints) by opening a web browser and navigating to: **`http://127.0.0.1:8000/docs`**
